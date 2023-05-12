import openai

def check_token_length(content, max_length=4096):
    """
    Checks the token length of a string.
    Args:
        content (str): The string to check.
        max_length (int): The maximum allowed length. Defaults to 4096 (GPT-3's limit).
    Returns:
        bool: True if the content is within the allowed length, False otherwise.
        str: The content, possibly truncated to the maximum allowed length.
    """
    token_length = len(openai.api_utils.tokens_of_string(content))

    if token_length > max_length:
        print(f"Warning: The content exceeds the maximum allowed length of {max_length} tokens. It will be truncated.")
        content = openai.api_utils.truncate_tokens(content, max_length)
        return False, content
    else:
        return True, content