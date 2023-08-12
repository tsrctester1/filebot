import re

async def rank_files(file_paths, num_files=3):
    """
    Rank the files based on some criteria.
    Here, we'll simply return the first 'num_files' for simplicity.
    In a real-world scenario, the ranking criteria can be more complex.
    """
    return file_paths[:num_files]

async def get_file_answers(file_paths, user_prompt, answer_function):
    """
    Asynchronously get answers from a given list of files.
    """
    answers = []
    for file_path in file_paths:
        stripped_file_path = re.sub(r'\.\d+$', '', file_path)
        answer = await answer_function(stripped_file_path, user_prompt, answer_type='final_answer')
        answers.append((stripped_file_path, answer))
    return answers
