import re


tag_re = re.compile(r"(<!--.*?-->|<[^>]*>)")


def remove_tags(text: str) -> str:
    text = tag_re.sub(" ", text)
    return " ".join(text.split()).strip()


def simplify_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = text.replace("\u2014", "-")
    text = text.replace("%u2013", "-")
    text = text.replace("\u2018", "'")
    text = text.replace("\u201c", '"')
    text = text.replace("%u2019", "'")
    text = text.replace("\u201d", '"')
    text = text.replace("\u2026", "...")
    text = text.replace("\u2122", "(TM)")
    text = text.replace("\u2212", "-")
    text = text.replace("\ufffd", " ")
    return text.strip()


def normalise_spaces(text: str) -> str:
    return " ".join(text.split()).strip()
