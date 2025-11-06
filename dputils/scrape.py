import re
import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass

import random

_user_agents = {
    "Chrome": {
        "Windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "Linux": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    },
    "Firefox": {
        "Windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Linux": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
    },
    "Safari": {
        "Mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"
    },
    "Edge": {
        "Windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.50",
        "Mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.50",
        "Linux": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.50"
    },
    # Add more browsers as needed
}

def _get_random_user_agent():
    # print("Selecting a random User-Agent...")
    browsers = list(_user_agents.keys())
    random_browser = random.choice(browsers)
    # print("Randomly picked browser:", random_browser)
    operating_systems = list(_user_agents[random_browser].keys())
    random_os = random.choice(operating_systems)
    # print("Randomly picked operating system:", random_os)
    return _user_agents[random_browser][random_os]


@dataclass
class Tag:
    # available output formats
    outputs = ['text', 'href', 'src', 'object', 'title', 'alt', 'value']

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
                    print(f"Error | {tag=} -> {e}")
                else:
                    data[key] = None
        elif tag.output == 'href':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs)['href']
            except Exception as e:
                if errors:
                    print(f"Error | {tag=} -> {e}")
                else:
                    data[key] = None

        elif tag.output == 'src':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs)['src']
            except Exception as e:
                if errors:
                    print(f"Error | {tag=} -> {e}")
                else:
                    data[key] = None
        elif tag.output == 'object':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs)
            except Exception as e:
                if errors:
                    print(f"Error | {tag=} -> {e}")
                else:
                    data[key] = None
        elif tag.output == 'title':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs)['title']
            except Exception as e:
                if errors:
                    print(f"Error | {tag=} -> {e}")
                else:
                    data[key] = None

        elif tag.output == 'alt':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs)['alt']
            except Exception as e:
                if errors:
                    print(f"Error | {tag=} -> {e}")
                else:
                    data[key] = None
        elif tag.output == 'value':
            try:
                data[key] = dom_item.find(tag.name, tag.attrs)['value']
            except Exception as e:
                if errors:
                    print(f"Error | {tag=} -> {e}")
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
        if isinstance(headers, str):
            headers = {'User-Agent': headers}
        if headers is None:
            headers = {'User-Agent': _get_random_user_agent()}
        if cookies is None:
            cookies = {"session-id": "", "session-id-time": "", "session-token": ""}
        try:
            # print('🌐'*10)
            # print("User agent: ", headers)
            # print("Cookies: ", cookies)
            # print("url: ", self.url)
            # print('🌐'*10)
            with httpx.Client(headers=headers, cookies=cookies, timeout=5, http2=True) as client:
                page = client.get(self.url)
            return BeautifulSoup(page.content, 'html.parser')
        except httpx.TimeoutException as e:
            print("Timeout error: ")
            raise e
        except httpx.RequestError as e:
            print("Request error: ")
            raise e
        except httpx.HTTPError as e:
            print("HTTP error: ")
            raise e
        

        # if headers is None:
        #     headers = {'User-Agent': Browser.any()}  # Using `or` for default values
        #     cookies = cookies or {"session-id": "", "session-id-time": "", "session-token": ""}

        #     try:
        #         with httpx.Client() as client:
        #             page = client.get(self.url, headers=headers, cookies=cookies)
        #         return BeautifulSoup(page.content, 'html.parser')
        #     except requests.RequestException as e:
        #         raise e
        # elif headers == -1:
        #     cookies = cookies or {"session-id": "", "session-id-time": "", "session-token": ""}
        #     try:
        #         page = requests.get(self.url, cookies=cookies)
        #         page.raise_for_status()  # Raises an exception for bad status codes
        #         return BeautifulSoup(page.content, 'html.parser')
        #     except requests.RequestException as e:
        #         raise e

    def get_data_from_page(self, errors=False, **tags) -> dict:
        """
        Extracts data based on a given list of Tag objects and returns a dictionary, from a page.

        Args:
            errors (bool): Flag to print errors (Default is False).

        Returns:
            dict: Extracted data.
        """
        data = {}
        extract(self.soup, tags, data, errors)
        return data

    def get_repeating_data_from_page(self, target: Tag = None, items: Tag = None, errors=False, info=False, **tags) -> list:
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
    from pprint import pp

    print("Single page data")
    url2 = "https://www.flipkart.com/apple-iphone-14-blue-128-gb/p/itmdb77f40da6b6d?pid=MOBGHWFHSV7GUFWA&lid=LSTMOBGHWFHSV7GUFWA3AV8J8"
    scraper2 = Scraper(url2)
    out2 = scraper2.get_data_from_page(
        title=Tag('h1',),
        price=Tag('div', cls='Nx9bqj CxhGGd'),
        description=Tag('div', cls='yN+eNk w9jEaj'),
    )
    pp(out2)
    print("list/grid of content")
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
        pp(item)
        print()
