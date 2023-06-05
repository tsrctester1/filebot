from typing import Tuple
from .token_counter import num_tokens_from_string

def check_token_length(content: str, max_length: int, model: str) -> Tuple[bool, str]:
    """
    Check if the token length of the content is within the specified maximum length.
    Returns a tuple (is_within_limit, content), where is_within_limit is a boolean indicating if the content is within the limit,
    and content is the original content or truncated content if it exceeds the limit.
    """
    token_length = num_tokens_from_string(content, model)

    if token_length > max_length:
        return False, content

    return True, content