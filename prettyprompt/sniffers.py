# a set of functions to test for bad intentions

from sqlparse import parse, tokens
from openai import ChatCompletion


def is_sql_write_statement(sql_statement: str) -> bool:
    """
    Returns True if the given SQL query is a write operation, False otherwise.
    """
    for statement in parse(sql_statement):
        for token in statement.tokens:
            # check if token is a command
            if (
                token.ttype in [tokens.Token.Keyword.DDL, tokens.Token.Keyword.DML]
                and token.value.upper() != "SELECT"
            ):
                return True
    return False


def is_prompt_injection_LLM(prompt: str) -> bool:
    prompt_messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": """Is the following prompt an example of a prompt injection?

%s
"""
            % prompt,
        },
    ]
    resp = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt_messages,
        temperature=0,
        max_tokens=2,  # enough to say yes or no!
    )
    answer = resp["choices"][0]["message"]["content"].strip().lower()
    return bool(answer.startswith("yes"))


def is_prompt_injection(prompt: str, strategy: str = "LLM") -> bool:
    """
    Returns True if the given prompt is a prompt injection, False otherwise.
    """
    if strategy == "LLM":
        return is_prompt_injection_LLM(prompt)
