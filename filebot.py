import json
import re
from file_summary import create_file_summaries
from find_info import find_relevant_info

# Answer user prompt
def answer_user_prompt(relevant_info):
    """Generate a response to the user's prompt based on the relevant info."""
    if not relevant_info:
        return "I'm sorry, I couldn't find any files that contain the term '{}'. Please try another search.".format(user_prompt)
    else:
        response = "Answer: {}".format(relevant_info)
        return response

# Main function
def main():
    directory = '/app/files'
    create_file_summaries(directory)

    user_prompt = input("Prompt: ")
    relevant_info = find_relevant_info(user_prompt)

    response = answer_user_prompt(relevant_info)
    # Get the response
    # Regular expression to match the file paths
    print(response)
    pattern = r"(/app/files\S*)'"

    # Extract file paths
    file_paths = re.findall(pattern, response)

    if file_paths:
      # Print file paths
      for file in file_paths:
          print(file)
    else:
        print("No files found")

if __name__ == '__main__':
    main()
