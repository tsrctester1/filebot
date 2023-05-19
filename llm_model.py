import os
import openai

# Call the OpenAI GPT-3 API
with open("openai_api_key", "r") as key_file:
    openai_api_key = key_file.read().strip()

os.environ["OPENAI_API_KEY"] = openai_api_key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_completion(prompt, max_tokens=256, temperature=0.8):
    json_response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=temperature,
      max_tokens=max_tokens,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return json_response['choices'][0]['text']