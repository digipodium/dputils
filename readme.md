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

The Scraper class is a web scraping tool that uses the BeautifulSoup library to extract data from a specified URL. The
class has several methods including init, validate_url, clean_url, soup, get, and get_all. The init method takes in a
URL, a user agent, cookies, and a clean flag. The validate_url method checks if the URL is valid and the clean_url
method removes any query parameters from the URL. The soup method makes a request to the URL and returns a BeautifulSoup
object of the webpage. The get method takes in a list of Tag objects and returns a dictionary of the extracted data. The
get_all method takes in a target tag, an items tag, and a list of tags and returns a list of dictionaries of the
extracted data for each item. The class also has the ability to handle errors and provide information about the
extraction process.

These functions can used on python versions 3.8 or greater.

References for more help: https://github.com/digipodium/dputils

Thank you for using dputils!