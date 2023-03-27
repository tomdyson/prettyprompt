from bs4 import BeautifulSoup


def find_innermost_tag(soup, tag_list):
    for tag_name in tag_list:
        if tag := soup.find(tag_name):
            return tag
    return soup


def process_tag(tag):
    if tag.name in ["p", "div", "h1", "h2", "h3", "h4", "h5", "h6"]:
        for a_tag in tag.find_all("a"):  # handle anchor tags inside the text
            a_tag.replace_with(f"{a_tag.text.strip()} ({a_tag.get('href', '')})")
        return f"{tag.get_text(strip=False)}\n\n"
    if tag.name == "li":
        for a_tag in tag.find_all("a"):  # handle anchor tags inside the list item
            a_tag.replace_with(f"{a_tag.text.strip()} ({a_tag.get('href', '')})")
        return f"- {tag.get_text(strip=False)}\n"
    return ""


def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Find the innermost tag that wraps the content
    content_tag = find_innermost_tag(soup, ["body", "section", "html"])

    formatted_text = "".join(
        process_tag(tag)
        for tag in content_tag.find_all(
            ["p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li"], recursive=True
        )
    )
    return formatted_text.strip()
