A python library which can be used to extraxct data from files, pdfs, doc(x) files, as well as save data into these files. This library can be used to scrape and extract webpage data from websites as well.

Functions from dputils.files:
1. get_data: 
    - To import, use statement: 
        ```python3
        from dputils.files import get_data
        ``` 
    - Obtains data from files of any extension given as args(supports text files, binary files, pdf, doc for now, more coming!)
    - sample call:
        ```python3
        content = get_data(r"sample.docx")
        print(content)
        ```
    - Returns a string or binary data depending on the output arg

2. save_data:
    - To import, use statement:
         ```python3
        from dputils.files import save_data
        ```
    - save_data can be used to write and save data into a file of valid   extension.
    - sample call: 
         ```python3
        pdfContent = save_data("sample.pdf", "Sample text to insert")
        print(pdfContent)
        ```
    - Returns True if file is successfully accessed and modified. Otherwise False.

Functions from dputils.scrape:
1. get_webpage_data:
    - To import, use statement: 
         ```python3
        from dputils.scrape import get_webpage_data
        ```
    - get_webpage_data can be used to obtain data from any website in the   form of BeautifulSoup object
    - sample call: 
        ```python3
        soup = get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)")
        print(type(soup))
        ```
    - Returns data as a BeautifulSoup object

2. extract_one:
    - To import, use statement: 
        ```python3
        from dputils.scrape import extract_one
        ```
    - extract_one can be used to extract a data item as a dict from data in a given BeautifulSoup object
    - sample call: 
        ```python3
        soup = get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)")

        dataDict = extract_one(soup, title = {'tag' : 'h1', 'attrs' : {'id' : 'firstHeading'}, 'output' : 'text'})
        print(dataDict)
        ```
    - Output will be of type dict

These functions can used on python versions 3.8 or greater.

References for more help: https://github.com/digipodium/dputils

Thank you for using dputils!