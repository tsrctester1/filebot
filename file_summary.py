import os
import json
import time
import math
from token_counter import num_tokens_from_string
from llm_model import generate_completion

# Modify the summarize_file function
def summarize_file(file_path, max_token_length=3000):
    """Read a file and return a summary."""
    with open(file_path, 'r') as file:
        content = file.read()

    total_tokens = num_tokens_from_string(content, 'gpt-3')

    if total_tokens <= max_token_length:
        prompt = f"My task is to summarize the document. Here is the document:\n\n{content}"

        summary = generate_completion(prompt)
        return [(file_path, summary)]

    # content exceeds max_token_length
    summaries = []
    for i in range(0, total_tokens, max_token_length):
        print(f"llm summary request {i}")
        chunk = content[i: i + max_token_length]
        prompt = f"My task is to summarize the document. Here is the document:\n\n{chunk}"

        summary = generate_completion(prompt)
        summaries.append((f"{file_path}.{i//max_token_length}", summary))

    return summaries

# Modify the create_file_summaries function
# Modify the create_file_summaries function
def create_file_summaries(directory, file_summaries_path):
    """Walk through a directory and generate a summary for each file."""
    # Load existing summaries
    try:
        with open(file_summaries_path, 'r') as json_file:
            file_summaries = json.load(json_file)
    except FileNotFoundError:
        file_summaries = {}

    # Set a flag to check if file_summaries.json is updated
    is_updated = False

    for root, dirs, files in os.walk(directory):
        # Skip directories named .gitignore
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            # Skip files named .gitignore
            if file == ".gitignore":
                continue

            file_path = os.path.join(root, file)
            base_file_path, _ = os.path.splitext(file_path)

            # Check if the file is new or updated
            if all(not key.startswith(base_file_path) for key in file_summaries.keys()) or \
            any(file_summaries[key]['mtime'] < os.path.getmtime(file_path) for key in file_summaries.keys() if key.startswith(base_file_path)):
                print(f"New or updated file detected: '{file_path}'")
                summaries = summarize_file(file_path)
                if summaries:
                    for path, summary in summaries:
                        file_summaries[path] = {
                            'summary': summary,
                            'mtime': os.path.getmtime(file_path)
                        }
                    # Set the flag to True when file_summaries.json is updated
                    is_updated = True

    with open(file_summaries_path, 'w') as json_file:
        json.dump(file_summaries, json_file, indent=4)

    # Notify the user if file_summaries.json is updated
    if is_updated:
        print(f"{file_summaries_path} has been updated.")