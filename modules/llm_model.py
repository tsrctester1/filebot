import os
import openai
import asyncio
import openai_async

# Call the OpenAI GPT-4 API
with open("openai_api_key", "r") as key_file:
    openai_api_key = key_file.read().strip()

os.environ["OPENAI_API_KEY"] = openai_api_key
openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_completion(prompt, model_name="gpt-3.5-turbo", max_tokens=256, temperature=0.9):
    model_to_use = "gpt-4" if model_name == "gpt-3.5-turbo" else "gpt-3.5-turbo"
    response = await openai_async.chat_complete(
        openai_api_key,
        timeout=60,
        payload={
            "model": model_to_use,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant and great at guessing what files may have info based on loose summaries of the files."},
                {"role": "user", "content": prompt},
            ]
        }
    )
    json_response = response.json()
    llm_content = json_response['choices'][0]['message']['content']

    return llm_content