import os
import json
import time
import openai

# Summarize file
def summarize_file(file_path, summary_length=100):
    """Read a file and return a summary."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Call the OpenAI GPT-3 API
    with open("openai_api_key", "r") as key_file:
        openai_api_key = key_file.read().strip()

    os.environ["OPENAI_API_KEY"] = openai_api_key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = "Summarize the following in less than 50 words: \
    ```{}```".format(content)

    ## Fake openai response.
    #json_response = '''
    #{
    #  "choices": [
    #    {
    #      "finish_reason": "stop",
    #      "index": 0,
    #      "logprobs": null,
    #      "text": "The provided email outlines the key terms for a non-binding Letter of Intent (LOI) regarding a chatbot project. The terms include the agreement to be signed, the creation of a custom chatbot by Osan3, licensing for Happy Org's usage rights, governance details to be discussed, IP ownership depending on data, possible termination, confidentiality maintenance, representations given, the governing law to be determined, and the LOI being considered preliminary."
    #    }
    #  ],
    #  "created": 1682805000,
    #  "id": "cmpl-7Amk4VjXv8wzZdKOyZzbyiHECtU6c",
    #  "model": "text-davinci-003",
    #  "object": "text_completion",
    #  "usage": {
    #    "completion_tokens": 251,
    #    "prompt_tokens": 400,
    #    "total_tokens": 651
    #  }
    #}
    #'''

    #json_response = json.loads(json_response)

    json_response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    # Get the generated questions and answers
    print("summary gpt response of '{}'".format(file_path))
    print("")
    print("")
    print(json_response)

    summary = json_response['choices'][0]['text']

    # Get the generated summary
    print("")
    print("parsed gpt response")
    print("")
    print("")
    print(summary)

    return summary

# Create file summaries
def create_file_summaries(directory):
    """Walk through a directory and generate a summary for each file."""
    # Load existing summaries
    try:
        with open('file_summaries.json', 'r') as json_file:
            file_summaries = json.load(json_file)
    except FileNotFoundError:
        file_summaries = {}

    # Set a flag to check if file_summaries.json is updated
    is_updated = False

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Check if the file is new or updated
            if file_path not in file_summaries or file_summaries[file_path]['mtime'] < os.path.getmtime(file_path):
                file_summaries[file_path] = {
                    'summary': summarize_file(file_path),
                    'mtime': os.path.getmtime(file_path)
                }
                # Set the flag to True when file_summaries.json is updated
                is_updated = True

    with open('file_summaries.json', 'w') as json_file:
        json.dump(file_summaries, json_file, indent=4)

    # Notify the user if file_summaries.json is updated
    if is_updated:
        print("file_summaries.json has been updated.")