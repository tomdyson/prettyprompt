# a set of functions to test for bad intentions

from sqlparse import parse, tokens


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
