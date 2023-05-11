import json
from file_summary import create_file_summaries

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
