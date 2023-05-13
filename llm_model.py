from llama_cpp import Llama

# Initialize Llama model
llm = Llama(model_path="/path/to/your/model.bin")

def generate_completion(prompt, max_tokens=150, stop=None, temperature=0.7):
    """
    Generate a completion using Llama model.

    Parameters:
    prompt (str): The prompt to be completed.
    max_tokens (int, optional): The maximum length of the generated text.
    stop (str or list, optional): One or more stop sequences. The generation will stop as soon as one of these sequences is encountered.
    temperature (float, optional): Controls the randomness of the generated text.

    Returns:
    str: The generated completion.
    """

    # Generate text completion
    output = llm(prompt, max_tokens=max_tokens, stop=stop, temperature=temperature, echo=True)

    # Extract the generated text from the completion
    generated_text = output["choices"][0]["text"]

    return generated_text
