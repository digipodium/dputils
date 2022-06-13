A python library which can be used to extraxct data from files, pdfs, doc(x) files, as well as save data 
into these files. This library can be used to scrape and extract webpage data from websites as well.

Functions from dputils.files:
1. get_data: 
    - To import, use statement: from dputils.files import get_data
    - get_data can be used to obtain data from txt, pdf, doc(x) and other    files depending on the type specified in the args
    - method specifications: get_data(path : str, output = 's', encoding = 'utf-8') -> str
    - sample call: get_data(r"sample.docx")
    - Documentation:
        Obtains data from files of any extension (supports text files, binary files, pdf, doc for now; more coming!)
        Returns a string or binary data depending on the output arg
    
        Args:
        path (str): path of the file to be read ex:"sample.txt" or "sample.pdf", or "sample.doc", etc.
        output (str): 's' is passed for the data to be stored as string; 'b' to obtain binary data
        encoding (str): existing encoding of file

2. save_data:
    - To import, use statement: from dputils.files import save_data
    - save_data can be used to write and save data into a file of valid extension.
    - method specifications: save_data(path : str, data : str)
    - sample call: save_data("sample.pdf", "Sample text to insert") -> bool
    - Documentation:
        Writes and saves data into a file of any extension
        Returns True if file is successfully accessed and modified. Otherwise False.
        
        Args:
        path (str): path of the file to be modified ex:"sample.txt" or "sample.pdf", or "sample.doc", etc.
        data (str): data to be stored and saved into the given file

Functions from dputils.scrape:
1. get_webpage_data:
    - To import, use statement: from dputils.scrape import get_webpage_data
    - get_webpage_data can be used to obtain data from any website in the form of BeautifulSoup object
    - method specifications: get_webpage_data(url, headers = None, cookies = None) -> BeautifulSoup
    - sample call: get_webpage_data("ht://pypi.org/project/fake-useragent/")
    - Documentation:
        Obtains data from any website
        Returns data as a BeautifulSoup object
        
        Args:
        url (str): url of the website to take data from
        headers (str): default value is None, which then creates fake useragent
        cookies (str): default value is None, which then satisfies given website's cookie policy

2. extract_one:
    - To import, use statement: from dputils.scrape import extract_one
    - extract_one can be used to extract a data item as a dict from data in a given BeautifulSoup object
    - method specifications: extract_one(soup : BeautifulSoup, **selectors) -> dict
    - sample call: extract_one(get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)"), title = {'tag' : 'h1', 'attrs' : {'id' : 'firstHeading'}, 'output' : 'text'})
    - Documentation:
        Extracts a single data item from given BeautifulSoup object
        Output will be a dict of {title : data_stored_in_selectors}
        
        Args:
        soup (BeautifulSoup): Contains entire page data as BeautifulSoup object. Data will be extracted from this object
        **selectors (dict): dict of {key : info}
            info must be written in following manner:
            first key is 'tag' with value as tag from where data is obtained
            second key is 'attrs' with value as dict containing id or class information
            third key is the output type of data: text, href or src (for images)
        Valid Examples of selectors:
            titleDict = {'tag' : 'span', 'attrs' : {'id' : 'productTitle'}, 'output' : 'text'} (info)
            priceDict = {'tag' : 'span', 'attrs' : {'class' : 'a-price-whole'}, 'output' : 'text'}
        Valid call: 
            extract_one(soup, titleDict, priceDict) 

These functions can used on python versions 3.9 or greater
references for more help: 
Thank you for using dputils!