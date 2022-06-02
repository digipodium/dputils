# param: path => address of file; output => return type of file, (s default) or b (binary) if user passes
# Check if file exist otherwise error should be thrown
# encoding error => we should handle that gracefully(do research)
# Test code using Pytest (do research)
# add documentation using triple quotes
#source $HOME/.poetry/env command imp
def get_data(path : str, output = 's'):
    """
    This is a funtion to obtain data
    """
    pass

import os
def file_read(fpath = r"LICENSE"):
    if not os.path.exists(fpath):
        print("File not found")
        return None
    if not os.path.isfile(fpath):
        print("Not a file")
        return None
    with open(fpath) as file:
        c = file.read()
        return c