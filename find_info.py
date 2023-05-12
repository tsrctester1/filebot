import os
import json
import time
import openai
from token_checker import check_token_length

# Find file from summaries.
def find_relevant_info(user_prompt, max_token_length=3900):
    with open('file_summaries.json', 'r') as json_file:
        file_summaries = json.load(json_file)

    user_prompt = f"Which files possibly have relevant info to the prompt `{user_prompt}` based on the following file summaries:\n\n{file_summaries}"
    is_within_limit, user_prompt = check_token_length(user_prompt, max_token_length, 'gpt-3')

    if not is_within_limit:
        return "The content is too large to summarize."

    # Call the OpenAI GPT-3 API
    with open("openai_api_key", "r") as key_file:
        openai_api_key = key_file.read().strip()

    os.environ["OPENAI_API_KEY"] = openai_api_key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    json_response = openai.Completion.create(
      model="text-davinci-003",
      prompt=user_prompt,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    response = json_response['choices'][0]['text']

    return response