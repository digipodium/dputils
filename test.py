from dputils.scrape import Scraper

#
#
# def test_read_file():
#     assert len(get_data(r"pyproject.toml")) > 0
#     assert type(get_data(r"pyproject.toml")) == str
#
#
# def test_read_pdf():
#     assert len(get_data(r"examples/sample.pdf")) > 0
#     assert type(get_data(r"examples/sample.pdf")) == str
#
#
# def test_save_data():
#     assert save_data("examples/sample.pdf", "Hello I am inserting this new text") is True
#     assert save_data("sample.docx", "TODAY'S DATA") is True
#
#

scr = Scraper(url="https://www.google.com")


def test_get_webpage():
    assert scr.__soup__() is not None


def test_extract_one():
    assert type(scr.extract(title={'tag': 'h1', 'attrs': {'id': 'firstHeading'}, 'output': 'text'})) == dict


def test_extract_many():
    assert type(scr.extract_all(
        target={'tag': 'div', 'attrs': {'class': 's-main-slot s-result-list s-search-results sg-row'}},
        items={'tag': 'div', 'attrs': {'class': 's-result-item'}},
        title={'tag': 'h2', 'attrs': {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'}})
    ) == list


def test_extract_links():
    assert type(scr.links()) == set
