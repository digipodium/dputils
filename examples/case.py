from dputils.scrape import Scraper
from fake_useragent import UserAgent

ua = UserAgent()
print(type(ua.random))

scr = Scraper(url="https://www.google.com")
print(scr.soup)
