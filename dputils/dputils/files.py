# param: path => address of file; output => return type of file, (s default) or b (binary) if user passes
# Check if file exist otherwise error should be thrown
# encoding error => we should handle that gracefully(do research)
# Test code using Pytest (do research)
# add documentation using triple quotes
#source $HOME/.poetry/env command imp
import os
import docx2txt
from pdfminer.high_level import extract_text

def get_data(path : str, output = 's', encoding = 'utf-8') -> str:
    """
    This is a funtion to obtain data
    """
    if output == 's':
        if not os.path.exists(path):
            print("File not found")
            return None
        if not os.path.isfile(path):
            print("Not a file")
            return None
        file_type = __file_type__(path)
        if file_type == 1:
            data = __doc_read__(path)
        elif file_type == 2:
            data = __pdf_read__(path)
        elif file_type == 3:
            data = __text_read__(path, encoding = encoding)
        else:
            print("File type could not be understood")
            data = None
        return data
    else:
        return None # for now

#Test doc and pdf file

def __file_type__(path : str) -> int:
    base, ext = os.path.splitext(path)
    print(ext, "HERE IS EXTENSION")
    if ext in [".doc", ".docx"]:
        return 1
    if ext == ".pdf":
        return 2
    if ext in [".txt", ".css", ".html", ".py", ".java", ".cpp", ".ipynb", ".md", ".lock", ".toml", ".rst"]:
        return 3

def __text_read__(path : str, encoding) -> str:
    try:
        with open(path, encoding = encoding) as file:
            content = file.read()
            return content
    except Exception as e:
        print("File could not be read")
        raise e

def __doc_read__(path : str) -> str:
    try:
        text = docx2txt.process(path)
    except Exception as e:
        print("Doc/Docx file could not be read")
        raise e

def __pdf_read__(path : str) -> str:
    try:
        return extract_text(path)
    except Exception as e:
        print("Pdf file could not be read")
        raise e