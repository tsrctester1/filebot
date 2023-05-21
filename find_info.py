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