import os
import openai

# Call the OpenAI GPT-4 API
with open("openai_api_key", "r") as key_file:
    openai_api_key = key_file.read().strip()

os.environ["OPENAI_API_KEY"] = openai_api_key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_completion(prompt, model_version="gpt-4", max_tokens=256, temperature=0.9):
    json_response = openai.ChatCompletion.create(
        model=model_version,
        messages=[
            {"role": "system", "content": "You are a helpful assistant and great at guessing what files may have info based on loose summaries of the files."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    llm_content = json_response['choices'][0]['message']['content']
    return llm_content
