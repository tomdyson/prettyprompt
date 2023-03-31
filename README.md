# Pretty Prompt

Simple tools for better prompts.

## Installation

`pip install prettyprompt`

## Usage

### Sniffing bad intentions

```python
from prettyprompt import sniffers

# will this SQL statement write to my database?
sniffers.is_sql_write_statement(user_supplied_sql)

# is this a prompt injection attempt? ask ChatGPT
# (needs an OpenAI API key)
sniffers.is_prompt_injection(prompt, strategy="LLM")

# uses spaCy to indicate the imperative-ness of a string
# needs a trained pipeline e.g. `python -m spacy download en_core_web_sm`
sniffers.is_imperative(prompt)
```

### Converting input

```python
from prettyprompt import converters

# convert scraped HTML into plain text, maintaining some structure
converters.html_to_text(scraped_html)

# splits text into meaningful chunks, using GPT-3.5
converters.chunker(long_text, max_words_per_chunk, min_words_per_chunk)
```

### Cleaning input

```python
from prettyprompt import cleaners

# remove tags from HTML
cleaners.remove_tags(html)

# normalise spaces
cleaners.normalise_spaces(text)

# swap common 'smart' characters with ASCII equivalents
cleaners.simplify_text(text)
```

## Tests

- `pip install pytest pytest-mock`
- `pytest`

## TODO

- [Prompt Injection](https://github.com/tomdyson/prettyprompt/issues/1)
