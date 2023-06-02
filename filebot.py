import json
import re
from file_summary import create_file_summaries
from find_info import find_relevant_info
from find_info import answer_prompt

# Answer user prompt
def answer_user_prompt(relevant_info):
    """Generate a response to the user's prompt based on the relevant info."""
    if not relevant_info:
        return "I'm sorry, I couldn't find any files that contain the term '{}'. Please try another search.".format(user_prompt)
    else:
        response = "Answer: {}".format(relevant_info)
        return response

# Extract file paths from response
def extract_file_paths(response):
    """Extract file paths from the response using regular expressions."""
    pattern = r"(/app/files\S*)'"
    file_paths = re.findall(pattern, response)
    return file_paths

# Main function
def main():
    directory = '/app/files'
    create_file_summaries(directory)

    user_prompt = input("Prompt: ")
    relevant_info = find_relevant_info(user_prompt)

    response = answer_user_prompt(relevant_info)

    # Extract file paths
    print(response)
    file_paths = extract_file_paths(response)

    if file_paths:
        # Print file paths
        for file in file_paths:
            stripped_file_path = re.sub(r'\.\d+$', '', file)
            answer = answer_prompt(stripped_file_path, user_prompt)
            print(answer)
            print(f"\n\nsource: {stripped_file_path}")
            break
    else:
        print("No files found")

if __name__ == '__main__':
    main()