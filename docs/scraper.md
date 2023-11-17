[homepage](index.md) | [files functions](files.md)

## Module: scraper

This module provides a `Scraper` class that allows you to scrape data from a webpage using BeautifulSoup library. It also includes supporting classes `Browser` and `Tag`.


### Class: Tag

This class represents an HTML tag that can be used to extract specific data from a webpage.

#### Properties

- `name` (str): The name of the HTML tag (default: 'div').
- `output` (str): The desired output format, which can be one of ['text', 'href', 'src', 'object'] (default: 'text').
- `cls` (str): The class attribute of the HTML tag (default: None).
- `id` (str): The id attribute of the HTML tag (default: None).
- `attrs` (dict): Additional attributes of the HTML tag (default: None).

#### Methods

- `__post_init__()` - Initializes the Tag object and performs necessary attribute assignments.
- `__str__()` - Returns a string representation of the Tag object.
- `__repr__()` - Returns a string representation of the Tag object.

### Class: Scraper

This class is used to scrape data from a webpage using BeautifulSoup library.

#### Methods

- `__init__(url: str, user_agent: str = None, cookies: dict = None, clean: bool = False)` - Initializes the Scraper object.
- `__validate_url__()` - Validates the URL of the webpage.
- `__clean_url__()` - Cleans the URL by removing query parameters.
- `__soup__(headers=None, cookies=None, clean=False)` - Obtains data from the webpage and returns a BeautifulSoup object.
- `get(errors=False, **tags: Tag) -> dict` - Extracts data based on the given list of Tag objects and returns a dictionary.
- `get_all(target: Tag, items: Tag, errors=False, info=False, **tags: Tag) -> list` - Extracts data for multiple items from the webpage and returns a list of dictionaries.

#### Example Usage

```python
url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
scraper = Scraper(url)
out = scraper.get_multiple_page_data(
    target=Tag('div', cls='_1YokD2 _3Mn1Gg'),
    items=Tag('div', cls='_1AtVbE col-12-12'),
    title=Tag('div', cls='_4rR01T'),
    price=Tag('div', cls='_30jeq3 _1_WHN1'),
    link=Tag('a', cls='_1fQZEK', output='href'),
)
```

This code creates a `Scraper` object with the specified URL and extracts data for multiple items from the webpage. The target and items are specified using `Tag` objects, and additional data to be extracted is specified as keyword arguments. The extracted data is returned as a list of dictionaries.

Note: The code provided in the question lacks indentation, which may cause syntax errors when executed. Make sure to fix the indentation before running the code.