def create_file_summary_prompt(file_name):
    """
    Create a prompt for summarizing the given file.

    Args:
    - file_name (str): Name of the file to summarize.

    Returns:
    - str: Generated prompt.
    """
    return f"Please summarize the content of {file_name} for me."

def get_model_choice(purpose="summarizing"):
    """
    Get the user's choice for the model version.

    Args:
    - purpose (str): The purpose of the model selection ("summarizing" or "answering").

    Returns:
    - str: Selected model version.
    """
    purpose_messages = {
        "summarizing": "Choose a model version for summarization: \n[a] gpt-3.5-turbo \n[b] gpt-4\n",
        "answering": "Choose a model version for answering the prompt: \n[a] gpt-3.5-turbo \n[b] gpt-4\n"
    }

    choice = ''
    while choice not in ['a', 'b']:
        choice = input(purpose_messages.get(purpose, purpose_messages["summarizing"]))
    return "gpt-3.5-turbo" if choice == 'a' else "gpt-4"
