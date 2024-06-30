# dputils Scraper Module Documentation

## Introduction

The `dputils` library provides a powerful and easy-to-use web scraping module called `scraper`. This module allows users to extract data from web pages using a combination of Python's `httpx`, `BeautifulSoup`, and custom data classes. The scraper module can handle various scraping tasks, including fetching data from single pages, extracting repeated data from lists of items, and more.


## Data extraction from a page

Here's a basic tutorial to help you get started with the `scraper` module.

1. **Import the required classes and functions:**

```python
from dputils.scrape import Scraper, Tag
```

2. **Initialize the `Scraper` class with the URL of the webpage you want to scrape:**

```python
url = "https://www.example.com"
scraper = Scraper(url)
```

3. **Define the tags you want to scrape using the `Tag` class:**

```python
title_tag = Tag(name='h1', cls='title', output='text')
price_tag = Tag(name='span', cls='price', output='text')
```

4. **Extract data from the page:**

```python
data = scraper.get_data_from_page(title=title_tag, price=price_tag)
print(data)
```

### Advanced Tutorial - extracting list of items from a page

For more advanced usage, such as extracting repeated data from lists of items on a page, you can use the following approach:

1. **Initialize the `Scraper` class:**

```python
url = "https://www.example.com/products"
scraper = Scraper(url)
```

2. **Define the tags for the target section and the items within that section:**
For repeated data extraction, you need to define `Target` and `item` and pass it to `get_repeating_data_from_page()` method.
   - *target* - defines the `Tag()` for area of the page containing the list of items.
   - *items* - defines the `Tag()` for repeated items within the target section. Like a product-card in product grid/list.
```python
target_tag = Tag(name='div', cls='product-list')
item_tag = Tag(name='div', cls='product-item')
title_tag = Tag(name='h2', cls='product-title', output='text')
price_tag = Tag(name='span', cls='product-price', output='text')
link_tag = Tag(name='a', cls='product-link', output='href')
```

1. **Extract repeated data from the page:**

```python
products = scraper.get_repeating_data_from_page(
    target=target_tag,
    items=item_tag,
    title=title_tag,
    price=price_tag,
    link=link_tag
)
for product in products:
    print(product)
```

## Detailed Description

### Scraper Class

The `Scraper` class is the main class for initializing the scraper and handling the extraction of data from web pages.

#### Constructor

```python
def __init__(self, webpage_url: str, user_agent: str = None, cookies: dict = None, clean: bool = False):
```

- `webpage_url` (str): URL of the webpage to scrape.
- `user_agent` (str): User agent string (optional).
- `cookies` (dict): Cookies for the request (optional).
- `clean` (bool): Flag to clean the URL (optional, default is `False`).

#### Methods

- **`_validate_url(self) -> bool`**: Validates the URL.
- **`_clean_url(self)`**: Cleans the URL by removing query parameters.
- **`_get_soup(self, headers=None, cookies=None, clean=False) -> BeautifulSoup`**: Fetches the webpage content and returns a BeautifulSoup object.
- **`get_data_from_page(self, errors=False, **tags) -> dict`**: Extracts data based on given tags and returns a dictionary.
- **`get_repeating_data_from_page(self, target: Tag = None, items: Tag = None, errors=False, info=False, **tags) -> list`**: Extracts data for multiple items and returns a list of dictionaries.
- **`get_tag(self, tag: Tag, errors=False)`**: Extracts data for a single Tag object and returns a dictionary.
- **`get_all_tags(self, tags: list, errors=False)`**: Extracts data for multiple Tag objects and returns a dictionary.

### Tag Class

The `Tag` class is used to define the HTML tags and attributes to be extracted from the web page.

#### Constructor

```python
@dataclass
class Tag:
    name: str = 'div'
    output: str = 'text'
    cls: str = None
    id: str = None
    attrs: dict = None
```

- `name` (str): The name of the HTML tag (default is 'div').
- `output` (str): The type of data to extract (default is 'text').
- `cls` (str): The class attribute of the HTML tag (optional).
- `id` (str): The ID attribute of the HTML tag (optional).
- `attrs` (dict): Additional attributes for the HTML tag (optional).

#### Methods

- **`__post_init__(self)`**: Validates the output type and sets the attributes.
- **`__str__(self)`**: Returns a string representation of the Tag object.
- **`__repr__(self)`**: Returns a string representation of the Tag object.

### Helper Functions

- **`_get_random_user_agent()`**: Returns a random User-Agent string from a predefined list.

### Extract Function

The `extract` function is used to extract data from a BeautifulSoup object based on the given tags.

```python
def extract(dom_item, tags, data, errors):
```

- `dom_item`: The BeautifulSoup object to extract data from.
- `tags`: A dictionary of Tag objects.
- `data`: A dictionary to store the extracted data.
- `errors`: A flag to indicate whether to print errors.

## Example Usage

Here's a complete example of using the `scraper` module to extract data from a webpage:

```python
from dputils.scraper import Scraper, Tag

url = "https://www.example.com"
scraper = Scraper(url)

title_tag = Tag(name='h1', cls='title', output='text')
price_tag = Tag(name='span', cls='price', output='text')

data = scraper.get_data_from_page(title=title_tag, price=price_tag)
print(data)
```

This documentation provides an overview of the `scraper` module in the `dputils` library, including basic and advanced usage tutorials, detailed descriptions of classes and functions, and an example usage.