import re

import requests
from bs4 import BeautifulSoup

from dputils.utills import Browser
from dputils.utills import Tag


def extract_one(item, tags, data, errors):
    for key, tag in tags.items():
        if tag.output == 'text':
            try:
                data[key] = item.find(tag.name, tag.attrs).text
            except Exception as e:
                if errors:
                    print(f"Error for {tag=} -> {e}")
                else:
                    data[key] = None
        elif tag.output == 'href':
            try:
                data[key] = item.find(tag.name, tag.attrs)['href']
            except Exception as e:
                if errors:
                    print(f"Error for {tag=} -> {e}")
                else:
                    data[key] = None

        elif tag.output == 'src':
            try:
                data[key] = item.find(tag.name, tag.attrs)['src']
            except Exception as e:
                if errors:
                    print(f"Error for {tag=} -> {e}")
                else:
                    data[key] = None
        elif tag.output == 'object':
            try:
                data[key] = item.find(tag.name, tag.attrs)
            except Exception as e:
                if errors:
                    print(f"Error for {tag=} -> {e}")
                else:
                    data[key] = None


class Scraper:
    def __init__(self, url: str, user_agent: str = None, cookies: dict = None, clean: bool = False):
        """
        Initializes Scraper class
        Args:
            url: url of the webpage
            user_agent: user agent of the browser (Default value = None)
            cookies: cookies of the browser (Default value = None)
            clean: cleans url (Default value = True)
        """
        self.url = url
        self.soup = self.__soup__(headers=user_agent, cookies=cookies, clean=clean)

    def __validate_url__(self) -> bool:
        """
        Validates url
        Returns:
            bool: True if url is valid, else False
        """
        regex = re.compile(r'^https?://', re.IGNORECASE)
        return re.match(regex, self.url) is not None

    def __clean_url__(self):
        """
        Cleans url
        Returns:
            None
        """
        if '?' in self.url:
            self.url = self.url.split('?')[0]

    def __soup__(self, headers=None, cookies=None, clean=False) -> BeautifulSoup:
        """
        Obtains data from any website and returns data as a BeautifulSoup object

        - ``headers`` (str): default value is `None`, which then creates fake useragent
        - ``cookies`` (str): default value is `None`, which then satisfies given website's cookie policy
        - ``clean`` (bool): default value is `True`, which cleans url

        Args:
            headers:  (Default value = None)
            cookies:  (Default value = None)
            clean:  (Default value = True)
        Returns:
            BeautifulSoup
        Raises:
            Exception: If url is not valid
        """
        if clean:
            self.__clean_url__()
        if not self.__validate_url__():
            raise Exception(f"Invalid URL -> {self.url}")
        if headers is None:
            headers = {'User-Agent': Browser.any()}
        if cookies is None:
            cookies = {"session-id": "", "session-id-time": "", "session-token": ""}
        try:
            page = requests.get(self.url, headers=headers, cookies=cookies)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')
                return soup
            else:
                print(f"Error: {page.status_code}")
        except Exception as e:
            raise e

    def get(self, errors=False, **tags: Tag) -> dict:
        """
        Extracts data based on given list of Tag objects and returns a dictionary

        Args:
            errors: (Default value = 'ignore')

        """
        data = {}
        extract_one(self.soup, tags, data, errors)
        return data

    def get_all(self, target: Tag, items: Tag, errors=False, info=False, **tags: Tag) -> list:

        data_list = []
        if target is None:
            target = Tag('body')
        if items is None:
            items = Tag('div')
        try:
            section = self.soup.find(target.name, target.attrs)
            if section is None:
                raise Exception(f"Error: {target=} not found")
            items = section.find_all(items.name, items.attrs)
            if items is None or len(items) == 0:
                raise Exception(f"Error: {items=} not found")
            if info:
                print(f"Found {len(items)} items")
            if info:
                print("Extracting data...")
            for idx, item in enumerate(items):
                data = {}
                if info:
                    print(f"Extracting data for item {idx + 1}...")
                try:
                    extract_one(item, tags, data, errors)
                    data_list.append(data)
                except Exception as e:
                    if errors:
                        print(f"Error for {idx=} -> {e}")
                    else:
                        continue
        except Exception as e:
            if errors:
                print(f"Error -> {e}")
        return data_list


if __name__ == '__main__':
    url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    scraper = Scraper(url)
    out = scraper.get_all(
        target=Tag('div', cls='_1YokD2 _3Mn1Gg'),
        items=Tag('div', cls='_1AtVbE col-12-12'),
        title=Tag('div', cls='_4rR01T'),
        price=Tag('div', cls='_30jeq3 _1_WHN1'),
        link=Tag('a', cls='_1fQZEK', output='href'),
    )
    from pprint import pp
    for item in out:
        pp(item)
        print()
