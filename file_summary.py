import os
import json
import time
import math
import openai
from token_counter import num_tokens_from_string

# Modify the summarize_file function
def summarize_file(file_path, max_token_length=4096):
    """Read a file and return a summary."""
    with open(file_path, 'r') as file:
        content = file.read()

    total_tokens = num_tokens_from_string(content, 'gpt3')

    if total_tokens <= max_token_length:
        prompt = f"My task is to summarize the document. Here is the document:\n\n{content}"
        summary = get_gpt3_summary(prompt)  # function to get the GPT-3 summary
        return [(file_path, summary)]

    # content exceeds max_token_length
    summaries = []
    for i in range(0, total_tokens, max_token_length):
        print(f"gpt summary request {i}")
        chunk = content[i: i + max_token_length]
        prompt = f"My task is to summarize the document. Here is the document:\n\n{chunk}"

        # Call the OpenAI GPT-3 API
        with open("openai_api_key", "r") as key_file:
            openai_api_key = key_file.read().strip()

        os.environ["OPENAI_API_KEY"] = openai_api_key
        openai.api_key = os.getenv("OPENAI_API_KEY")

        json_response = openai.Completion.create(
          model="text-davinci-003",
          prompt=prompt,
          temperature=0.7,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

        summary = json_response['choices'][0]['text']
        summaries.append((f"{file_path}.{i//max_token_length}", summary))

    return summaries

# Modify the create_file_summaries function
def create_file_summaries(directory):
    """Walk through a directory and generate a summary for each file."""
    # Load existing summaries
    try:
        with open('file_summaries.json', 'r') as json_file:
            file_summaries = json.load(json_file)
    except FileNotFoundError:
        file_summaries = {}

    # Set a flag to check if file_summaries.json is updated
    is_updated = False

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Check if the file is new or updated
            if file_path not in file_summaries or file_summaries[file_path]['mtime'] < os.path.getmtime(file_path):
                summaries = summarize_file(file_path)
                print(f"New or updated file detected: '{file_path}'")
                if summaries:
                    for path, summary in summaries:
                        file_summaries[path] = {
                            'summary': summary,
                            'mtime': os.path.getmtime(file_path)
                        }
                    # Set the flag to True when file_summaries.json is updated
                    is_updated = True

    with open('file_summaries.json', 'w') as json_file:
        json.dump(file_summaries, json_file, indent=4)

    # Notify the user if file_summaries.json is updated
    if is_updated:
        print("file_summaries.json has been updated.")