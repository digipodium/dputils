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

def get_webpage_data(url, headers = None, cookies = None):
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
            print("Page not found")
            return None
        elif page.status_code == 503:
            print("Page unavailable")
            return None
        elif page.status_code == 200:
            print("Page found")
            soup = BeautifulSoup(page.content, 'html.parser')
            return soup
    except Exception as e:
        raise e

#WRITE DOCUMENTATION FOR WHATEVER FILES ARE THERE