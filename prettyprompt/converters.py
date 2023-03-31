from typing import List
from bs4 import BeautifulSoup
from openai import ChatCompletion


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


def chunker(text: str, max_words_per_chunk: int, min_words_per_chunk: int) -> List[str]:
    """Splits a string into chunks of a maximum size, using GPT"""

    prompt = f"""Please split the following text into chunks of no 
more than {max_words_per_chunk} words. Start each chunk with '[[chunk]]'. 
Split the text into meaningful sections that make sense on their own. 
You can go as small as {min_words_per_chunk} words if necessary."""
    prompt_messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": text,
        },
    ]
    resp = ChatCompletion.create(
        model="gpt-3.5-turbo", messages=prompt_messages, temperature=0
    )
    answer = resp["choices"][0]["message"]["content"]
    return [chunk.strip() for chunk in answer.split("[[chunk]]") if chunk.strip()]
