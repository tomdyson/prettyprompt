# Pretty Prompt

Simple tools for better prompts.

## Usage

### Sniffing bad intentions

```python
from prettyprompt import sniffers

# will this SQL statement write to my database?
sniffers.is_sql_write_statement(user_supplied_sql)
```

### Converting input

```python
from prettyprompt import converters

# convert scraped HTML into plain text, maintaining some structure
converters.html_to_text(scraped_html)
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

- `pip install pytest`
- `pytest`

## TODO

- [ ] Prompt Injection
