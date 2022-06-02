# cd dputils, then pytest
from Files import file_read

def test_read():
    assert len(file_read('../LICENSE')) > 0