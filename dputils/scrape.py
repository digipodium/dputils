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


def extract(dom_item, tags, data, errors):
    for key, tag in tags.items():
        if tag.output == 'text':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs).text
            except Exception as e:
                if errors:
                    print(f"Error for {tag=} -> {e}")
                else:
                    data[key] = None
        elif tag.output == 'href':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs)['href']
            except Exception as e:
                if errors:
                    print(f"Error for {tag=} -> {e}")
                else:
                    data[key] = None

        elif tag.output == 'src':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs)['src']
            except Exception as e:
                if errors:
                    print(f"Error for {tag=} -> {e}")
                else:
                    data[key] = None
        elif tag.output == 'object':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs)
            except Exception as e:
                if errors:
                    print(f"Error for {tag=} -> {e}")
                else:
                    data[key] = None


class Scraper:
    def __init__(self, webpage_url: str, user_agent: str = None, cookies: dict = None, clean: bool = False):
        """
       Initializes Scraper class.

       Args:
           webpage_url (str): URL of the webpage.
           user_agent (str): User agent of the browser (Default is None).
           cookies (dict): Cookies of the browser (Default is None).
           clean (bool): Cleans URL (Default is False).
       """
        self.url = webpage_url
        self.soup = self._get_soup(headers=user_agent, cookies=cookies, clean=clean)

    def _validate_url(self) -> bool:
        """
        Validates URL.

        Returns:
            bool: True if the URL is valid, else False.
        """
        regex = re.compile(r'^https?://', re.IGNORECASE)
        return bool(re.match(regex, self.url))

    def _clean_url(self):
        """
        Cleans URL.

        Returns:
            None
        """
        if '?' in self.url:
            self.url = self.url.split('?')[0]

    def _get_soup(self, headers=None, cookies=None, clean=False) -> BeautifulSoup:
        """
        Obtains data from any website and returns data as a BeautifulSoup object.

        Args:
            headers (str): User agent string (Default is None).
            cookies (dict): Cookies for the request (Default is None).
            clean (bool): Flag to clean the URL (Default is False).

        Returns:
            BeautifulSoup: Parsed HTML content.

        Raises:
            ValueError: If the URL is invalid.
            requests.RequestException: If an error occurs while making the request.
        """
        if clean:
            self._clean_url()
        if not self._validate_url():
            raise ValueError(f"Invalid URL -> {self.url}")

        headers = headers or {'User-Agent': Browser.any()}  # Using `or` for default values
        cookies = cookies or {"session-id": "", "session-id-time": "", "session-token": ""}

        try:
            page = requests.get(self.url, headers=headers, cookies=cookies)
            page.raise_for_status()  # Raises an exception for bad status codes
            return BeautifulSoup(page.content, 'html.parser')
        except requests.RequestException as e:
            raise e

    def get_page_data(self, errors=False, **tags) -> dict:
        """
        Extracts data based on a given list of Tag objects and returns a dictionary.

        Args:
            errors (bool): Flag to print errors (Default is False).

        Returns:
            dict: Extracted data.
        """
        data = {}
        extract(self.soup, tags, data, errors)
        return data

    def get_repeating_page_data(self, target: Tag = None, items: Tag = None, errors=False, info=False, **tags) -> list:
        """
        Extracts data for multiple items based on given Tag objects and returns a list of dictionaries.

        Args:
            target (Tag): Tag object to identify the main section (Default is None).
            items (Tag): Tag object to identify items within the main section (Default is None).
            errors (bool): Flag to print errors (Default is False).
            info (bool): Flag to print information messages (Default is False).

        Returns:
            list: List of dictionaries containing extracted data for each item.
        """
        data_list = []
        target = target or Tag('body')
        items = items or Tag('div')

        try:
            section = self.soup.find(target.name, target.attrs)
            if not section:
                raise ValueError(f"Error: {target=} not found")

            items = section.find_all(items.name, items.attrs) or []
            if not items:
                raise ValueError(f"Error: {items=} not found")

            if info:
                print(f"Found {len(items)} items")
            if info:
                print("Extracting data...")

            for idx, element in enumerate(items):
                data = {}
                if info:
                    print(f"Extracting data for element {idx + 1}...")
                try:
                    extract(element, tags, data, errors)
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

    def get_tag(self, tag: Tag, errors=False):
        """
        Extracts data for a single Tag object and returns a dictionary.

        Args:
            tag (Tag): Tag object to extract data for.
            errors (bool): Flag to print errors (Default is False).

        Returns:
            dict: Extracted data.
        """
        data = {}
        extract(self.soup, {tag.name: tag}, data, errors)
        return data

    def get_all_tags(self, tags: list, errors=False):
        """
        Extracts data for multiple Tag objects and returns a dictionary.

        Args:
            tags (list): List of Tag objects to extract data for.
            errors (bool): Flag to print errors (Default is False).

        Returns:
            dict: Extracted data.
        """
        data = {}
        for tag in tags:
            extract(self.soup, {tag.name: tag}, data, errors)
        return data


if __name__ == '__main__':
    url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    scraper = Scraper(url)
    out = scraper.get_repeating_page_data(
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

    print("Single page data")
    url2 = "https://www.flipkart.com/apple-iphone-14-blue-128-gb/p/itmdb77f40da6b6d?pid=MOBGHWFHSV7GUFWA&lid=LSTMOBGHWFHSV7GUFWA3AV8J8"
    scraper2 = Scraper(url2)
    out2 = scraper2.get_page_data(
        title=Tag('span', cls='B_NuCI'),
        price=Tag('div', cls='_30jeq3 _16Jk6d'),
        description=Tag('div', cls='_2o-xpa'),
    )
    pp(out2)