from dputils import __version__
from dputils.files import get_data

def test_version():
    assert __version__ == '0.1.0'
def test_read_file():
    assert len(get_data(r"/Users/akulsingh/Desktop/Internship/requirements.txt")) > 0
    assert type(get_data(r"/Users/akulsingh/Desktop/Internship/requirements.txt")) == str