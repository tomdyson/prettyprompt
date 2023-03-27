from prettyprompt.sniffers import is_sql_write_statement


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
