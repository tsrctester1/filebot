import json
import re
from file_summary import create_file_summaries
from find_info import find_relevant_info
from find_info import answer_prompt

# Answer user prompt
def answer_user_prompt(relevant_info):
    """Generate a response to the user's prompt based on the relevant info."""
    if not relevant_info:
        return "I'm sorry, I couldn't find any relevant files to answer your question. Please rephrase or try another search."
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

    while True:
        user_prompt = input("\033[92mPrompt:\033[0m ")
        relevant_info = find_relevant_info(user_prompt)

        response = answer_user_prompt(relevant_info)

        # Extract file paths
        file_paths = extract_file_paths(response)

        if file_paths:
            # Print file paths
            for file in file_paths:
                stripped_file_path = re.sub(r'\.\d+$', '', file)
                answer = answer_prompt(stripped_file_path, user_prompt, answer_type='final_answer')
                print(f"\n\n{answer}")
                print(f"\033[1;97m\nsource: {stripped_file_path}\033[0m")
                print("\n\n")
                break
        else:
            print("\033[38;5;208mNo files found\033[0m")

if __name__ == '__main__':
    main()