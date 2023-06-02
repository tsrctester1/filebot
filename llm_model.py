import os
import openai

# Call the OpenAI GPT-3 API
with open("openai_api_key", "r") as key_file:
    openai_api_key = key_file.read().strip()

os.environ["OPENAI_API_KEY"] = openai_api_key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_completion(prompt, max_tokens=256, temperature=0.9):
  json_response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
  )
  llm_content = json_response['choices'][0]['message']['content']
  #  json_response = openai.Completion.create(
  #    model="text-davinci-003",
  #    prompt=prompt,
  #    temperature=temperature,
  #    max_tokens=max_tokens,
  #    top_p=1,
  #    frequency_penalty=0,
  #    presence_penalty=0
  #  )

  return llm_content
  #return json_response['choices'][0]['message']['content']
  #return json_response['choices'][0]['text']