from prettyprompt.converters import html_to_text


class TestHtmlToText:
    # Tests that the function correctly converts valid html code
    # with header and paragraph tags to plain text with appropriate
    # formatting. tags: [happy path]
    def test_valid_html_with_header_and_paragraph_tags(self):
        html = (
            "<h1>Header 1</h1><p>Paragraph 1</p>"
            + "<h2>Header 2</h2><p>Paragraph 2</p>"
        )
        expected_output = "Header 1\n\nParagraph 1\n\nHeader 2\n\nParagraph 2"
        assert html_to_text(html) == expected_output

    # Tests that the function correctly converts valid html code
    # with unordered list tags to plain text with appropriate
    # formatting. tags: [happy path]
    def test_valid_html_with_unordered_list_tags(self):
        # sourcery skip: class-extract-method
        html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        expected_output = "- Item 1\n- Item 2"
        assert html_to_text(html) == expected_output

    # Tests that the function returns an empty string when given an
    # empty html code string. tags: [edge case]
    def test_empty_html_code_string(self):
        html = ""
        expected_output = ""
        assert html_to_text(html) == expected_output

    # Tests that the function correctly converts html code with nested
    # tags to plain text with appropriate formatting. tags: [general behavior]
    def test_html_code_string_with_outer_div(self):
        html = "<div><span>Text</span></div>"
        expected_output = "Text"
        assert html_to_text(html) == expected_output

    # Tests that the function correctly converts html code with nested
    # tags to plain text with appropriate formatting. tags: [general behavior]
    def test_html_code_with_nested_tags(self):
        html = "<h1>Header 1 <span>with nested text</span></h1>"
        expected_output = "Header 1 with nested text"
        assert html_to_text(html) == expected_output
