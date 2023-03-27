from prettyprompt.cleaners import remove_tags, simplify_text, normalise_spaces


class TestRemoveTags:
    # Tests that the function preserves non-html text when there are no html tags in
    # the input text. tags: [happy path]
    def test_no_tags(self):
        assert remove_tags("This is a test") == "This is a test"

    # Tests that the function removes the html tag when there is only one html tag in
    # the input text. tags: [happy path]
    def test_one_tag(self):
        assert remove_tags("This is <b>bold</b> text") == "This is bold text"

    # Tests that the function removes all html tags when there are multiple html tags
    # in the input text. tags: [happy path]
    def test_multiple_tags(self):
        assert (
            remove_tags("This is <b>bold</b> and <i>italic</i> text")
            == "This is bold and italic text"
        )

    # Tests that the function removes all nested html tags in the input text.
    # tags: [edge case]
    def test_nested_tags(self):
        assert (
            remove_tags("This is <b><i>bold and italic</i></b> text")
            == "This is bold and italic text"
        )

    # Tests that the function removes incomplete html tags in the input text.
    # tags: [edge case]
    def test_incomplete_tags(self):
        assert remove_tags("This is <b>bold text") == "This is bold text"

    # Tests that the function removes html tags with special characters in the input
    # text. tags: [edge case]
    def test_special_characters(self):
        assert remove_tags("This is <b>@#$%^&*()</b> text") == "This is @#$%^&*() text"


class TestSimplifyText:
    # Tests that the function handles unicode characters that are not in the ascii
    # character set. tags: [happy path]
    def test_non_ascii_chars(self):
        input_text = (
            "This text contains \u00a0 non-breaking spaces "
            + "and \u201csmart quotes\u201d."
        )
        expected_output = 'This text contains   non-breaking spaces and "smart quotes".'
        assert simplify_text(input_text) == expected_output

    # Tests that the function does not modify input text that contains no unicode
    # characters to replace. tags: [happy path]
    def test_no_unicode_chars(self):  # sourcery skip: class-extract-method
        input_text = "This text contains no unicode characters to replace."
        expected_output = "This text contains no unicode characters to replace."
        assert simplify_text(input_text) == expected_output

    # Tests that the function replaces the correct unicode character when input text
    # contains only one of the unicode characters to replace. tags: [happy path]
    def test_one_unicode_char(self):
        input_text = "This text contains only one \u00a0 non-breaking space."
        expected_output = "This text contains only one   non-breaking space."
        assert simplify_text(input_text) == expected_output

    # Tests that the function returns an empty string when input text is an empty
    # string. tags: [edge case]
    def test_empty_string(self):
        input_text = ""
        expected_output = ""
        assert simplify_text(input_text) == expected_output

    # Tests that the function replaces all instances of the same unicode character when
    # input text contains multiple instances of the same unicode character to replace.
    # tags: [happy path]
    def test_multiple_unicode_chars(self):
        input_text = "This text contains multiple \u2014 dashes and \u2026 ellipses."
        expected_output = "This text contains multiple - dashes and ... ellipses."
        assert simplify_text(input_text) == expected_output


class TestNormaliseSpaces:
    # Tests that the function correctly normalizes input text with normal spaces.
    # tags: [happy path]
    def test_normal_spaces_happy(self):
        # Happy path test for normal spaces
        input_text = "This is a normal sentence."
        expected_output = "This is a normal sentence."
        assert normalise_spaces(input_text) == expected_output

    # Tests that the function correctly normalizes input text with multiple spaces
    # between words. tags: [happy path]
    def test_multiple_spaces_happy(self):
        # Happy path test for multiple spaces
        input_text = "This    is    a    sentence    with    multiple    spaces."
        expected_output = "This is a sentence with multiple spaces."
        assert normalise_spaces(input_text) == expected_output

    # Tests that the function correctly normalizes input text with leading/trailing
    # spaces. tags: [happy path]
    def test_leading_trailing_spaces_happy(self):
        # Happy path test for leading/trailing spaces
        input_text = "   This is a sentence with leading/trailing spaces.   "
        expected_output = "This is a sentence with leading/trailing spaces."
        assert normalise_spaces(input_text) == expected_output

    # Tests that the function correctly handles input text with no spaces.
    # tags: [edge case]
    def test_no_spaces_edge(self):
        # Edge case test for no spaces
        input_text = "NoSpacesHere"
        expected_output = "NoSpacesHere"
        assert normalise_spaces(input_text) == expected_output

    # Tests that the function correctly handles input text with only one word.
    # tags: [edge case]
    def test_one_word_edge(self):
        # Edge case test for one word
        input_text = "Hello"
        expected_output = "Hello"
        assert normalise_spaces(input_text) == expected_output

    # Tests that the function correctly handles input text with non-space whitespace
    # characters (e.g. tabs, newlines). tags: [general behavior]
    def test_non_space_whitespace_general(self):
        # General behavior test for non-space whitespace characters
        input_text = "This\tis\na\tsentence\nwith\tnon-space\twhitespace\tcharacters."
        expected_output = "This is a sentence with non-space whitespace characters."
        assert normalise_spaces(input_text) == expected_output
