#enter pytest dputils
from dputils import __version__
from dputils.files import get_data, save_data
from dputils.scrape import get_webpage_data
"""
def test_read_file():
    assert len(get_data(r"/Users/akulsingh/Desktop/Internship/requirements.txt")) > 0
    assert type(get_data(r"/Users/akulsingh/Desktop/Internship/requirements.txt")) == str
def test_read_doc():
    assert len(get_data(r"/Users/akulsingh/Desktop/Internship/sample.docx")) > 0
    assert type(get_data(r"/Users/akulsingh/Desktop/Internship/sample.docx")) == str
def test_read_pdf():
    assert len(get_data(r"/Users/akulsingh/Desktop/Internship/sample.pdf")) > 0
    assert type(get_data(r"/Users/akulsingh/Desktop/Internship/sample.pdf")) == str
"""
def test_save_data():
    assert save_data("sample.pdf", "Hello I am inserting this new text") is True                          
def test_get_webpage():
    assert get_webpage_data("ht://pypi.org/project/fake-useragent/") is None