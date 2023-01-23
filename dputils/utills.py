from dataclasses import dataclass
from random import choice

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


if __name__ == '__main__':
    import requests

    url = "https://www.google.com"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tag = Tag('a', cls='gb1', output='href')
    print(tag)
    print(soup.findAll(tag.name, tag.attrs))
