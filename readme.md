A python library which can be used to extraxct data from files, pdfs, doc(x) files, as well as save data into these
files. This library can be used to scrape and extract webpage data from websites as well.

### Installation Requirements and Instructions

Python versions 3.8 or above should be installed. After that open your terminal:
For Windows users:

```shell
pip install dputils
```

For Mac/Linux users:

```shell
pip3 install dputils
```

### Files Modules

Functions from dputils.files:

1. get_data:
   - To import, use statement:
      ```python3
      from dputils.files import get_data
      ```
   - Obtains data from files of any extension given as args(supports text files, binary files, pdf, doc for now, more
   coming!)
   - sample call:
      ```python3
      content = get_data(r"sample.docx")
      print(content)
      ```

   - Returns a string or binary data depending on the output arg
   - images will not be extracted

2. save_data:
   - save_data can be used to write and save data into a file of valid extension.
   - sample call:
      ```python3
      from dputils.files import save_data
   
      pdfContent = save_data("sample.pdf", "Sample text to insert")
      print(pdfContent)
      ```
   - Returns True if file is successfully accessed and modified. Otherwise, False.

### Scrape Modules

#### Data extraction from a page

Here's a basic tutorial to help you get started with the `scraper` module.

1. **Import the required classes and functions:**

```python
from dputils.scraper import Scraper, Tag
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

#### Extracting list of items from a page
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

These functions can used on python versions 3.8 or greater.

References for more help: https://github.com/digipodium/dputils

Thank you for using dputils!