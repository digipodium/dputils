## [home](index.md)
## [files module](files.md)  
## [scrape module](scraper.md)

<img alt="Python Version" src="https://img.shields.io/badge/python-3.8+-blue"> <img alt="Contributions welcome" src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg"> <img alt="License" src="https://img.shields.io/badge/license-MIT-green"> <img alt="Build Status" src="https://img.shields.io/badge/build-passing-brightgreen.svg">

<img alt="Documentation Status" src="https://img.shields.io/badge/documentation-up%20to%20date-brightgreen.svg"> <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/dputils"> <img alt="Stars" src="https://img.shields.io/github/stars/digipodium/dputils?style=social">

# documentation for dputils

dputils is a python library which can be used to extraxct data from files, pdfs, doc(x) files, as well as save data into these files. 

This library can be used to scrape and extract webpage data from websites as well.

## Installation Requirements and Instructions

Python versions 3.8 or above should be installed. After that open your terminal:
For windows users:
```shell
pip install dputils
```
For Mac/Linux users:
```shell
pip3 install dputils
```

## extract file data in few lines of code
```python
from dputils.files import get_data
content = get_data(r"sample.docx")
print(content)
```

## Scrape data in few lines of code
```python
from dputils.scrape import Scraper, Tag

url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

scraper = Scraper(url)
out = scraper.get_repeating_date_from_page(
    target=Tag('div', cls='DOjaWF gdgoEp'),
    items=Tag('div', cls='_75nlfW'),
    title=Tag('div', cls='KzDlHZ'),
    price=Tag('div', cls='Nx9bqj _4b5DiR'),
    link=Tag('a', cls='CGtC98', output='href'),
)

for item in out:
    print(item)
```
Check out more on [library's page on pypi](https://pypi.org/project/dputils/)

