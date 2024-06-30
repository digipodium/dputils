[files functions](files.md) | [scraper functions](scraper.md)
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

