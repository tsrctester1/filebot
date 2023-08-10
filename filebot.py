import json
import re
import configparser
from modules.file_summary import create_file_summaries
from modules.find_info import find_relevant_info, answer_prompt
from modules.utils import create_file_summary_prompt, get_model_choice


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
    pattern = r"\[(.*?)\]"
    file_paths = re.findall(pattern, response)
    return file_paths

def main():
    config = configparser.ConfigParser()
    config.read('filebot.config')
    file_summaries_path = config['OPTIONS'].get('RelativeFileSummariesPath', '')
    file_store_path = config['OPTIONS'].get('RelativeFileStorePath', '')

    # Check if there's a need to summarize any files first
    need_to_summarize = create_file_summaries(file_store_path, file_summaries_path, None)

    if need_to_summarize:
        model_choice = get_model_choice(purpose="summarizing")
        create_file_summaries(file_store_path, file_summaries_path, model_choice)

    while True:
        user_prompt = input("\033[92mPrompt:\033[0m ")
        relevant_info = find_relevant_info(user_prompt)

        response = answer_user_prompt(relevant_info)

        # Extract file paths
        file_paths = extract_file_paths(response)

        if file_paths:
            # Present all file paths to the user
            print("\nFound the following relevant files:")
            for index, file in enumerate(file_paths, start=1):
                stripped_file_path = re.sub(r'\.\d+$', '', file)
                print(f"{index}. {stripped_file_path}")
            print("")

            while True:
                # Ask the user to select a file
                file_choice = input("Please select a file by typing its number or press 'Enter' to skip or select another: ")

                # If the user presses 'Enter' without choosing a file, break to outer loop
                if file_choice.strip() == '':
                    break

                selected_index = int(file_choice) - 1

                # Ensure valid selection
                if selected_index < 0 or selected_index >= len(file_paths):
                    print("\033[38;5;208mInvalid selection\033[0m")
                    continue

                # Use the selected file
                selected_file = re.sub(r'\.\d+$', '', file_paths[selected_index])
                prompt_for_file = create_file_summary_prompt(selected_file)
                answer = answer_prompt(selected_file, prompt_for_file, answer_type='final_answer')
                print(f"\n\n{answer}")
                print(f"\033[1;97m\nsource: {selected_file}\033[0m")
                print("\n\n")

        else:
            print(f"\033[38;5;208mNo files found\033[0m\n\n{response}")

if __name__ == '__main__':
    main()