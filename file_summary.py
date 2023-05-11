import os
import json
import time

# Summarize file
def summarize_file(file_path, summary_length=100):
    """Read a file and return a summary."""
    with open(file_path, 'r') as file:
        content = file.read()
    return content[:summary_length]

# Create file summaries
def create_file_summaries(directory):
    """Walk through a directory and generate a summary for each file."""
    # Load existing summaries
    try:
        with open('file_summaries.json', 'r') as json_file:
            file_summaries = json.load(json_file)
    except FileNotFoundError:
        file_summaries = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Check if the file is new or updated
            if file_path not in file_summaries or file_summaries[file_path]['mtime'] < os.path.getmtime(file_path):
                file_summaries[file_path] = {
                    'summary': summarize_file(file_path),
                    'mtime': os.path.getmtime(file_path)
                }

    with open('file_summaries.json', 'w') as json_file:
        json.dump(file_summaries, json_file, indent=4)