from prettyprompt.sniffers import is_prompt_injection_LLM, is_sql_write_statement


class TestSQLWriteSniffer:
    # Tests that a single sql write statement returns true. tags: [happy path]
    def test_single_write_sql_statement(self):
        assert (
            is_sql_write_statement("INSERT INTO users (name, age) VALUES ('John', 25);")
            is True
        )

    # Tests that a single sql read statement returns false. tags: [happy path]
    def test_single_read_sql_statement(self):
        assert is_sql_write_statement("SELECT * FROM users;") is False

    # Tests that an empty sql statement returns false. tags: [edge case]
    def test_empty_sql_statement(self):
        assert is_sql_write_statement("") is False

    # Tests that a sql statement with only whitespace returns false. tags: [edge case]
    def test_whitespace_sql_statement(self):
        assert is_sql_write_statement("   ") is False

    # Tests that a sql statement with multiple statements returns true if at least
    # one is a write operation. tags: [edge case]
    def test_multiple_sql_statements(self):
        assert (
            is_sql_write_statement(
                "SELECT * FROM users; INSERT INTO users (name, age) VALUES ('John', 25);"
            )
            is True
        )


class TestPromptInjectionSniffer:
    # Tests that the function correctly identifies a prompt injection when provided
    # with a prompt that is an example of prompt injection. tags: [happy path]
    def test_happy_path(self, mocker):
        # Mock ChatCompletion API response
        mocker.patch(
            "openai.ChatCompletion.create",
            return_value={"choices": [{"message": {"content": "yes"}}]},
        )
        prompt = "This is a prompt injection example: {{malicious_code}}"
        assert is_prompt_injection_LLM(prompt) is True
