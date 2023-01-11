import re
from typing import Optional

import requests
from bs4 import BeautifulSoup

from dputils.utills import Browser


class Scraper:

    def __init__(self, url: str, user_agent: str = None, cookies: dict = None, clean: bool = True):
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

    def __soup__(self, headers=None, cookies=None, clean=False) -> Optional[BeautifulSoup]:
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
            if page.status_code == 404:
                return None
            elif page.status_code == 503:
                return None
            elif page.status_code == 200:
                soup = BeautifulSoup(page.content, 'html.parser')
                return soup
        except Exception as e:
            raise e

    def extract(self, **selectors) -> dict:
        """
        Extracts date from tags provided in a dictionary format and returns a dictionary. Selectors must be written in a dict format with following keys:

        - first key is **`'tag'`** with value as tag from where data is obtained
        - second key is **`'attrs'`** with value as dict containing id or class information
        - third key is **`'output'`**: which specifies type of data received: text, href or src
        - `output` key can be 'text' or 'href' or 'src' or 'object'. `text` is default value

        extract(my_selectors)

        Args:
            **selectors:
        Returns:
            dict[str, Any]
        Examples
        --------
        >>> my_selectors = [
            {'tag' : 'div', 'attrs' : {'id' : 'my_id'}, 'output' : 'text'},
            {'tag' : 'div', 'attrs' : {'class' : 'my_class'}, 'output' : 'href'},
            {'tag' : 'div', 'attrs' : {'id' : 'my_id'}, 'output' : 'src'}]
        >>> new_data = extract(my_selectors)
        >>> print(new_data)
        """

        data = {}
        if not isinstance(self.soup, BeautifulSoup):
            raise Exception("Soup is not a BeautifulSoup object")
        try:
            for key, info in selectors.items():
                tag = info.get('tag', 'div')
                attrs = info.get('attrs', None)  # defaults as 2nd param
                output = info.get('output', 'text')
                if output == 'text':
                    data[key] = self.soup.find(tag, attrs=attrs).text.strip()
                elif output == 'href':
                    data[key] = self.soup.find(tag, attrs=attrs).attrs.get('href')
                elif output == 'src':  # for images
                    data[key] = self.soup.find(tag, attrs=attrs).attrs.get('src')
                elif output == 'object':  # for objects
                    data[key] = self.soup.find(tag, attrs=attrs)
        finally:
            return data

    def extract_all(self, target, items, **selectors) -> list[dict]:
        """
        Extracts several data items from given BeautifulSoup object
        Output will be a list containing dicts of {title : data_stored_in_selectors}

        #### Args:
        `soup` (BeautifulSoup): Contains entire page data as BeautifulSoup object. Data items will be extracted from this object

        `**selectors` (dict): dict of {key : info}

       #### info must be written in a dict format with following keys:
        ##### A simple selector

        - first key is `'tag'` with value as tag from where data is obtained

        - second key is `'attrs'` with value as dict containing id or class information

        - third key is `'output'`: which specifies type of data recieved: text, href or src
            - `output` key can be 'text' or 'href' or 'src' or 'object'. `text` is default value
            - if output is 'text', then text will be retreived from the tag
            - if output is 'href', then href will be retreived from the tag [for <a> tags]
            - if output is 'src', then src will be retreived from the tag [for <img> tags]
            - if output is 'object', then object will be retured

        #### Valid Examples:
        ```
        title =  {'tag' : 'h2', 'attrs' : {'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-2'}, output = 'text'}
        priceDict = {'tag' : 'span', 'attrs' : {'class' : 'a-price-whole'}, output = 'text'}
        ```

        target is a special selector and can be added to specify which section of html code should data be extracted from

        #### Example of target use:
        ```
        target = {'tag' : 'div', 'attrs' : {'class':'s-main-slot s-result-list s-search-results sg-row'}, output = 'text'}
        ```
        #### items is a mandatory selector which refers to the repeating blocks of html code from soup object

        Example of item use:
        ```
        items =  {'tag' : 'div', 'attrs' : {'class':'s-result-item'}, output = 'text'}
        ```
        #### Valid call:
        ```
        soup = get_webpage_data("https://www.amazon.com/s?k=headphones&crid=1DUUWW6PEVAJ1&sprefix=headphones%2Caps%2C161&ref=nb_sb_noss_1")
        extract_many(soup,
                target = {'tag' : 'div', 'attrs' : {'class':'s-main-slot s-result-list s-search-results sg-row'}, output = 'text'},
                items =  {'tag' : 'div', 'attrs' : {'class':'s-result-item'}, output = 'text'},
                title =  {'tag' : 'h2', 'attrs' : {'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-2'}, output = 'text'})
        ```
        """
        data_list = []
        if not isinstance(self.soup, BeautifulSoup):
            raise Exception("Soup is not a BeautifulSoup object")

        tag = target.get('tag')
        attrs = target.get('attrs')
        if tag is None:
            print("Please give valid selectors")
            print("Example: target = {'tag' : 'div', 'attrs' : {...}")
            return data_list
        else:
            target = self.soup.find(tag, attrs)
            if target is None:
                print(f"Could not find target section with this {tag} and {attrs}")
                return data_list

        items = target.find_all(items.get('tag'), attrs=items.get('attrs'))
        items_count = len(items)
        if items_count == 0:
            print("No data found")
            return data_list
        else:
            print(f"{items_count} items found")
            selectors.pop('target')
            selectors.pop('items')
            for idx, item in enumerate(items):
                data = {}
                try:
                    for key, info in selectors.items():
                        tag = info.get('tag', 'div')
                        attrs = info.get('attrs', None)
                        output = info.get('output', 'text')
                        if output == 'text':
                            data[key] = item.find(tag, attrs=attrs).text.strip()
                        elif output == 'href':
                            data[key] = item.find(tag, attrs=attrs).attrs.get('href')
                        elif output == 'src':
                            data[key] = item.find(tag, attrs=attrs).attrs.get('src')
                        elif output == 'object':
                            data[key] = item.find(tag, attrs=attrs)
                        else:
                            print('Not suitable output')
                    data_list.append(data)
                except:
                    print("Item skipped at index:", idx)
            else:
                print("All items extracted")
            return data_list

    def links(self, target=None) -> set:
        """
        Returns all links from the page as a set
        Args:
            target : if target is None, then all links will be returned    
        Returns: set of links
        Raises: 
            Exception: if target is not found
        Examples:
            >>> scr = Scraper(webpage_url) 
            >>> scr.links()    
       """
        if target is not None:
            tag = target.get('tag')
            attrs = target.get('attrs')
            if tag is None:
                print("Please give valid selectors")
                print("Example: target = {'tag' : 'div', 'attrs' : {...}")
                return set()
            else:
                target = self.soup.find(tag, attrs)
                if target is None:
                    print(f"Could not find target section with this {tag} and {attrs}")
                    return set()
        else:
            target = self.soup
        url_list = target.find_all('a')
        links = set()
        try:
            for link in url_list:
                url = link.attrs.get('href')
                if url:
                    if url != "#":
                        links.add(url)
        except Exception as e:
            raise e
        return links
