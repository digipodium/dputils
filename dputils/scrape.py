import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

def __validate_url__(url):
    regex = re.compile(r'^(?:http)s?://', re.IGNORECASE)
    return re.match(regex, url) is not None

def __clean_url__(url):
    if '?' in url:
        url = url.split('?')[0]
    return url

def get_webpage_data(url, headers = None, cookies = None, clean = False) -> BeautifulSoup:
    """
    Obtains data from any website
    Returns data as a BeautifulSoup object
    
    Args:
    url (str): url of the website to take data from
    headers (str): default value is None, which then creates fake useragent
    cookies (str): default value is None, which then satisfies given website's cookie policy
    clean (bool): default value is True, which cleans url
    """
    if clean:
        url = __clean_url__(url)
    if not __validate_url__(url):
        print("Invalid url")
        return None
    if headers is None:
        ua = UserAgent()
        headers = {'User-Agent' : ua.random}
    if cookies is None:
        cookies = {"session-id" : "", "session-id-time" : "", "session-token" : ""}
    try:
        page = requests.get(url, headers = headers, cookies = cookies)
        if page.status_code == 404:
            return None
        elif page.status_code == 503:
            return None
        elif page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup
    except Exception as e:
        raise e

def extract_one(soup : BeautifulSoup, **selectors) -> dict:
    """
    Extracts a single data item from given BeautifulSoup object
    Output will be a dict of {title : data_stored_in_selectors}
    
    Args:
    soup (BeautifulSoup): Contains entire page data as BeautifulSoup object. Data will be extracted from this object
    **selectors (dict): dict of {key : info}
        info must be written in following manner:
           first key is 'tag' with value as tag from where data is obtained
           second key is 'attrs' with value as dict containing id or class information
           third key is the output type of data: text, href or src (for images)
        Valid Examples:
           titleDict = {'tag' : 'span', 'attrs' : {'id' : 'productTitle'}, 'output' : 'text'} (info)
           priceDict = {'tag' : 'span', 'attrs' : {'class' : 'a-price-whole'}, 'output' : 'text'}
        Valid call: 
           extract_one(soup, titleDict, priceDict) 
    """
    if not isinstance(soup, BeautifulSoup):
        print("Not a BeautifulSoup object")
        return None
    data = {}
    try:
        for key,info in selectors.items():
            tag = info.get('tag', 'div')
            attrs = info.get('attrs', None) #defaults as 2nd param
            output = info.get('output', 'text')
            if output == 'text':
                data[key] = soup.find(tag, attrs = attrs).text.strip()
            elif output == 'href':
                data[key] = soup.find(tag, attrs = attrs).attrs.get('href') 
            elif output == 'src': #for images
                data[key] = soup.find(tag, attrs = attrs).attrs.get('src')     
            else:
                print('Not suitable output')
        return data
    except Exception as e:
        print("Could not extract data")
        raise 

def extract_many(soup : BeautifulSoup, **selectors) -> list:
    """
    Extracts several data items from given BeautifulSoup object
    Output will be a list containing dicts of {title : data_stored_in_selectors}
    
    Args:
    soup (BeautifulSoup): Contains entire page data as BeautifulSoup object. Data items will be extracted from this object
    **selectors (dict): dict of {key : info}
        info must be written in following manner:
            first key is 'tag' with value as tag from where data is obtained
            second key is 'attrs' with value as dict containing id or class information
            third key is 'output': which specifies type of data recieved: text, href or src
        Valid Examples:
            title =  {'tag' : 'h2', 'attrs' : {'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-2'}, output = 'text'}
            priceDict = {'tag' : 'span', 'attrs' : {'class' : 'a-price-whole'}, output = 'text'}
        
        target is a special selector and can be added to specify which section of html code should data be extracted from
        Example of target use:
            target = {'tag' : 'div', 'attrs' : {'class':'s-main-slot s-result-list s-search-results sg-row'}, output = 'text'}
        
        items is a mandatory selector which refers to the repeating blocks of html code from soup object
        Example of item use:
            items =  {'tag' : 'div', 'attrs' : {'class':'s-result-item'}, output = 'text'}
        
        Valid call: 
            soup = get_webpage_data("https://www.amazon.com/s?k=headphones&crid=1DUUWW6PEVAJ1&sprefix=headphones%2Caps%2C161&ref=nb_sb_noss_1")
            extract_many(soup, 
                target = {'tag' : 'div', 'attrs' : {'class':'s-main-slot s-result-list s-search-results sg-row'}, output = 'text'},
                items =  {'tag' : 'div', 'attrs' : {'class':'s-result-item'}, output = 'text'},
                title =  {'tag' : 'h2', 'attrs' : {'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-2'}, output = 'text'})
    """
    if 'target' in selectors:
        tag = selectors['target'].get('tag')
        attrs = selectors['target'].get('attrs')
        if tag is None:
            print("Please give valid selectors")
            print("Example: target = {'tag' : 'div', 'attrs' : {...}")
            return None
        else:
            target = soup.find(tag, attrs)
            if target is None:
                print(f"Could not find target section with this {tag} and {attrs}")
                return None
    else:
        target = soup
    data_list = []
    if 'items' in selectors:
        items = target.find_all(selectors['items'].get('tag'), attrs = selectors['items'].get('attrs'))
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
                    for key,info in selectors.items():
                        tag = info.get('tag', 'div')
                        attrs = info.get('attrs', None) 
                        output = info.get('output', 'text')
                        if output == 'text':
                            data[key] = item.find(tag, attrs = attrs).text.strip()
                        elif output == 'href':
                            data[key] = item.find(tag, attrs = attrs).attrs.get('href') 
                        elif output == 'src': 
                            data[key] = item.find(tag, attrs = attrs).attrs.get('src')     
                        else:
                            print('Not suitable output')
                    data_list.append(data)
                except:
                    print("Item skipped at index:", idx)
            else:
                print("All items extracted")
            return data_list
    else:
        print("items is required as a parameter containing dict containing tag, attrs as keys")
        print("Example: items = {'tag' : 'div', 'attrs' : {...}, output = 'text'")

def extract_urls(soup : BeautifulSoup, target = None) -> list:
    """
    Obtains all the urls from given website
    Returns all urls in a list
    
    Args:
    soup (BeautifulSoup): Contains entire page data as BeautifulSoup object. URLs will be extracted from this object
    target (dict): target is an optional arg and can be added to specify which section of html code should urls be extracted from
    """
    if target is not None:
        tag = target.get('tag')
        attrs = target.get('attrs')
        if tag is None:
            print("Please give valid selectors")
            print("Example: target = {'tag' : 'div', 'attrs' : {...}")
            return None
        else:
            target = soup.find(tag, attrs)
            if target is None:
                print(f"Could not find target section with this {tag} and {attrs}")
                return None
    else:
        target = soup
    url_list = target.find_all('a'); links = set()
    try:
        for link in url_list:
            url = link.attrs.get('href')
            if url:
                if url != "#":
                    links.add(url)
    except Exception as e:
        print("Could not filter links")
    return list(links)