from dputils.files import get_data,save_data
from dputils.scrape import get_webpage_data,extract_one,extract_many

def test_read_file():
    assert len(get_data(r"/Users/akulsingh/Desktop/Internship/pyproject.toml")) > 0
    assert type(get_data(r"/Users/akulsingh/Desktop/Internship/pyproject.toml")) == str
# test_read_doc():
    #assert len(get_data(r"/Users/akulsingh/Desktop/Internship/examples/example.docx")) > 0
    #assert type(get_data(r"/Users/akulsingh/Desktop/Internship/examples/example.docx")) == str
def test_read_pdf():
    assert len(get_data(r"/Users/akulsingh/Desktop/Internship/examples/sample.pdf")) > 0
    assert type(get_data(r"/Users/akulsingh/Desktop/Internship/examples/sample.pdf")) == str
def test_save_data():
    assert save_data("examples/sample.pdf", "Hello I am inserting this new text") is True          
    assert save_data("/Users/akulsingh/Desktop/Internship/examples/sample.docx", "TODAY'S DATA") is True                
def test_get_webpage():
    assert get_webpage_data("ht://pypi.org/project/fake-useragent/") is None
def test_extract_one():
    assert type(extract_one(get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)"), title = {'tag' : 'h1', 'attrs' : {'id' : 'firstHeading'}, 'output' : 'text'})) == dict
def test_extract_many():
    assert type(extract_many(get_webpage_data("https://www.amazon.com/s?k=headphones&crid=1DUUWW6PEVAJ1&sprefix=headphones%2Caps%2C161&ref=nb_sb_noss_1"), 
    target = {'tag' : 'div', 'attrs' : {'class':'s-main-slot s-result-list s-search-results sg-row'}},
    items =  {'tag' : 'div', 'attrs' : {'class':'s-result-item'}},
    title =  {'tag' : 'h2', 'attrs' : {'class':'a-size-mini a-spacing-none a-color-base s-line-clamp-2'}})) == list