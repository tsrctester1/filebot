import os
import json
import time

# Summarize file
def summarize_file(file_path, summary_length=100):
    """Read a file and return a summary."""
    with open(file_path, 'r') as file:
        content = file.read()
    return content[:summary_length]

import os
import json
import time

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
                print("New or modified file: " + file_path)
                file_summaries[file_path] = {
                    'summary': summarize_file(file_path),
                    'mtime': os.path.getmtime(file_path)
                }

    with open('file_summaries.json', 'w') as json_file:
        json.dump(file_summaries, json_file, indent=4)

def find_relevant_info(user_prompt):
    """Find and return relevant info from files based on user prompt."""
    relevant_info = {}

    # Load file summaries
    with open('file_summaries.json', 'r') as json_file:
        file_summaries = json.load(json_file)

    # Loop through each file summary
    for file_path, file_data in file_summaries.items():
        # Check if the user prompt is in the file summary
        if user_prompt in file_data['summary']:
            # Fetch the full file content
            with open(file_path, 'r') as file:
                content = file.read()
            relevant_info[file_path] = content

    return relevant_info

# Answer user prompt
def answer_user_prompt(user_prompt, relevant_info):
    """Generate a response to the user's prompt based on the relevant info."""
    if not relevant_info:
        return "I'm sorry, I couldn't find any files that contain the term '{}'. Please try another search.".format(user_prompt)
    else:
        response = "Here are the files that contain the term '{}':\n".format(user_prompt)
        for file_path in relevant_info.keys():
            response += "- {}\n".format(file_path)
        return response

# Main function
def main():
    directory = '/app/files'
    create_file_summaries(directory)

    user_prompt = input("Enter a search term: ")
    relevant_info = find_relevant_info(user_prompt)

    response = answer_user_prompt(user_prompt, relevant_info)
    print(response)

if __name__ == '__main__':
    main()
