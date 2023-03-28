from prettyprompt.sniffers import (
    is_prompt_injection_LLM,
    is_sql_write_statement,
    is_imperative,
)


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
                "SELECT * FROM users; INSERT INTO users (name, age) VALUES ('Sof', 25);"
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


class TestPromptImperativeness:
    # Tests that a prompt with a simple imperative sentence
    # returns true. tags: [happy path]
    def test_simple_imperative(self):
        assert is_imperative("Open the door.") is True

    # Tests that a prompt with a complex imperative sentence
    # returns true. tags: [happy path]
    def test_complex_imperative(self):
        assert is_imperative("Please open the door and close the window.") is True

    # Tests that a prompt with no verbs returns false. tags: [edge case]
    def test_no_verbs(self):
        assert is_imperative("The cat sat on the mat.") is False

    # Tests that a prompt with multiple verbs returns true if any of them
    # are imperatives. tags: [happy path]
    def test_multiple_verbs(self):
        assert is_imperative("Go to the store and buy some milk") is True
        assert is_imperative("Run, jump, and play") is True
        assert is_imperative("Eat, drink, and be merry") is True

    # Tests that a prompt with a verb that is not in its base form returns
    # false. tags: [edge case]
    def test_non_base_form_verb(self):
        assert is_imperative("He has eaten breakfast already") is False
        assert is_imperative("She'll be running in the marathon") is False
        assert is_imperative("They have been playing netball all day") is False

    # Tests that a prompt with a verb in its base form that is not an
    # imperative returns false. tags: [edge case]
    def test_non_imperative_base_form_verb(self):
        assert is_imperative("I want to eat pizza for dinner") is False
        assert is_imperative("She needs to study for her exam") is False
        assert is_imperative("He likes to play video games in his free time") is False
