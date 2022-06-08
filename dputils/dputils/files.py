#source $HOME/.poetry/env command imp
#To publish, cd dutils, then poetry publish
#poetry add 'module'
import os
from xmlrpc.client import Boolean
import docx2txt
from pdfminer.high_level import extract_text
from fpdf import FPDF

#GET DATA
def get_data(path : str, output = 's', encoding = 'utf-8') -> str:
    """
    This is a funtion to obtain data from txt, doc and pdf files. UTF-8 is preferred.
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
            try: 
                data = __text_read__(path, encoding = encoding)
            except:
                print("Encoding not supported")
        else:
            print("File type could not be understood")
            data = None
        return data
    elif output == 'b':
        return __binary_read__(path)

def __file_type__(path : str) -> int:
    base, ext = os.path.splitext(path)
    if ext in [".doc", ".docx"]:
        return 1
    if ext == ".pdf":
        return 2
    if ext in [".txt", ".css", ".html", ".py", ".java", ".cpp", ".ipynb", ".md", ".lock", ".toml", ".rst"]:
        return 3

def __text_read__(path : str, encoding) -> str:
    try:
        with open(path, encoding = encoding) as file:
            return file.read()
    except Exception as e:
        print("File could not be read")
        raise e

def __doc_read__(path : str) -> str:
    try:
        return docx2txt.process(path)
    except Exception as e:
        print("Doc/Docx file could not be read")
        raise e

def __pdf_read__(path : str) -> str:
    try:
        return extract_text(path)
    except Exception as e:
        print("Pdf file could not be read")
        raise e

def __binary_read__(path : str):
    try:
        with open(path, mode = 'rb') as file:
            return file.read()
    except Exception as e:
        print("Binary file could not be read")
        raise e

def save_data(path : str, data : str) -> bool:
    """
    """
    status = False
    file_type = __file_type__(path)
    if file_type == 1:
        status = __txt_file_write__(path, data)
    if file_type == 2:
        status =  __pdf_write__(path, data)
    return status

def __txt_file_write__(path : str, data : str) -> bool:
    try:
        with open(path, 'w') as file:
            file.write(data)
        return True
    except Exception as e:
        print("File could not be modified")
        raise e

def __pdf_write__(path : str, data : str) -> bool:
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica', size =12)
        pdf.cell(txt=data)
        pdf.output(path)
        return True
    except Exception as e:
        print("Pdf file could not be modified")
        raise e