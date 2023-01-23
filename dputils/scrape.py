import re
from dataclasses import dataclass
from random import choice

import requests
from bs4 import BeautifulSoup


class Browser:
    user_agents = [
        'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
        'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
    ]

    @staticmethod
    def any():
        return choice(Browser.user_agents)


@dataclass
class Tag:
    # available output formats
    outputs = ['text', 'href', 'src', 'object']

    # fields
    name: str = 'div'
    output: str = 'text'
    cls: str = None
    id: str = None
    attrs: dict = None

    def __post_init__(self):
        if self.output not in self.outputs:
            raise ValueError(f"output must be one of {self.outputs}")
        if self.attrs is None:
            self.attrs = {}
        if self.cls is not None:
            self.attrs['class'] = self.cls
        if self.id is not None:
            self.attrs['id'] = self.id

    def __str__(self):
        if self.attrs is None:
            self.attrs = {}
        if self.cls is not None:
            self.attrs['class'] = self.cls
        if self.id is not None:
            self.attrs['id'] = self.id
        return f"ℹ️--[tag: {self.name} attrs: {self.attrs} output: {self.output}]--"

    def __repr__(self):
        return self.__str__()


def extract(item, tags, data, errors):
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
        extract(self.soup, tags, data, errors)
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
                    extract(item, tags, data, errors)
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
