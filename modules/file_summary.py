import os
import json
import time
import math
from .token_counter import num_tokens_from_string
from .llm_model import generate_completion

def get_summary_instruction(config_path):
    with open(config_path, 'r') as file:
        lines = file.readlines()
    try:
        start_index = lines.index("[SUMMARY]\n")
    except ValueError:
        return ""
    for line in lines[start_index:]:
        if line.startswith("PrependPrompt = "):
            return line.replace("PrependPrompt = ", "").strip().strip('"')
    return ""

summary_instruction = get_summary_instruction("./filebot.config")

def summarize_file(file_path, model_choice=None, max_token_length=3000):
    if not model_choice:  # If no model choice is provided, return without summarizing
        return None
    with open(file_path, 'r') as file:
        content = file.read()

    total_tokens = num_tokens_from_string(content, 'gpt-3')

    if total_tokens <= max_token_length:
        prompt = f"{summary_instruction} Here is the document:\n\n{content}"
        summary = generate_completion(prompt, model_version=model_choice)
        return [(file_path, summary)]

    summaries = []
    for i in range(0, total_tokens, max_token_length):
        print(f"llm summary request {i}")
        chunk = content[i: i + max_token_length]
        prompt = f"{summary_instruction} Here is the document:\n\n{chunk}"
        summary = generate_completion(prompt, model_version=model_choice)
        summaries.append((f"{file_path}.{i//max_token_length}", summary))

    return summaries

def create_file_summaries(directory, file_summaries_path, model_choice):
    try:
        with open(file_summaries_path, 'r') as json_file:
            file_summaries = json.load(json_file)
    except FileNotFoundError:
        file_summaries = {}

    is_updated = False

    for root, dirs, files in os.walk(directory):
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            if file == ".gitignore":
                continue

            file_path = os.path.join(root, file)
            base_file_path, _ = os.path.splitext(file_path)

            if all(not key.startswith(base_file_path) for key in file_summaries.keys()) or \
            any(file_summaries[key]['mtime'] < os.path.getmtime(file_path) for key in file_summaries.keys() if key.startswith(base_file_path)):
                print(f"New or updated file detected: '{file_path}'")
                summaries = summarize_file(file_path, model_choice)
                if summaries:
                    for path, summary in summaries:
                        file_summaries[path] = {
                            'summary': summary,
                            'mtime': os.path.getmtime(file_path)
                        }
                    is_updated = True

    with open(file_summaries_path, 'w') as json_file:
        json.dump(file_summaries, json_file, indent=4)

    if is_updated:
        print(f"{file_summaries_path} has been updated.")

    return is_updated  # Return whether there was an update or not