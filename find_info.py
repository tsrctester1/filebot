import os
import json
import configparser
from token_checker import check_token_length
from llm_model import generate_completion

def find_relevant_info(user_prompt, max_token_length=3900):
    with open('file_summaries.json', 'r') as json_file:
        file_summaries = json.load(json_file)

    # Read configuration file
    config = configparser.ConfigParser()
    config.read('filebot.config')

    # Get prepend text
    prepend_prompt = config['DEFAULT'].get('PrependPrompt', '')


    user_prompt = f"{prepend_prompt}. Which files possibly have relevant info to the prompt `{user_prompt}` based on the following file summaries:\n\n{file_summaries}"
    is_within_limit, user_prompt = check_token_length(user_prompt, max_token_length, 'gpt-3')

    if not is_within_limit:
        return "The content is too large to summarize."

    response = generate_completion(user_prompt)

    return response

def get_file_content(file_path):
    """Fetch the content of a file at a given file path."""
    with open(file_path, 'r') as file:
        content = file.read()

    return content

def answer_prompt(file_path, user_prompt, max_token_length=3900):
    content = get_file_content(file_path)

    config = configparser.ConfigParser()
    config.read('filebot.config')

    # Get prepend text
    prepend_prompt = config['DEFAULT'].get('PrependPrompt', '')

    #user_prompt = f"{prepend_prompt} {user_prompt}"
    is_within_limit, user_prompt = check_token_length(user_prompt, max_token_length, 'gpt-3')

    if not is_within_limit:
        return "The content is too large to summarize."

    final_prompt = f"{prepend_prompt}. Answer this prompt ```{user_prompt}```, based on the following info: ```{content}```"
    print(final_prompt)
    print("\n\n")
    response = generate_completion(final_prompt, max_tokens=2500, temperature=0.8)

    return response