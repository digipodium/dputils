#enter pytest dputils
from dputils import __version__
from dputils.files import get_data, save_data
from dputils.scrape import get_webpage_data, extract_one

def test_read_file():
    assert len(get_data(r"/Users/akulsingh/Desktop/Internship/requirements.txt")) > 0
    assert type(get_data(r"/Users/akulsingh/Desktop/Internship/requirements.txt")) == str
def test_read_doc():
    assert len(get_data(r"/Users/akulsingh/Desktop/Internship/sample.docx")) > 0
    assert type(get_data(r"/Users/akulsingh/Desktop/Internship/sample.docx")) == str
def test_read_pdf():
    assert len(get_data(r"/Users/akulsingh/Desktop/Internship/sample.pdf")) > 0
    assert type(get_data(r"/Users/akulsingh/Desktop/Internship/sample.pdf")) == str
def test_save_data():
    assert save_data("sample.pdf", "Hello I am inserting this new text") is True          
    assert save_data("/Users/akulsingh/Desktop/Internship/sample.docx", "TODAY'S DATA") is True                
def test_get_webpage():
    assert get_webpage_data("ht://pypi.org/project/fake-useragent/") is None
def test_extract_one():
    assert type(extract_one(get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)"), title = {'tag' : 'h1', 'attrs' : {'id' : 'firstHeading'}, 'output' : 'text'})) == dict