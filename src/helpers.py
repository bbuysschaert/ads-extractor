import os

def check_if_file_exists(_path:str) -> bool:
    """
    Check whether a file exists at the specified location.  Returns a boolean
    """
    return (os.path.exists(_path)) & (os.path.isfile(_path))

def check_if_dir_exists(_path:str) -> bool:
    """
    Check whether a directory exists at the specified location.  Returns a boolean
    """
    return (os.path.exists(_path)) & (os.path.isdir(_path))

def build_filename_data(_bibcode:str) -> str:
    """
    Builds the name for the data output file
    """
    return '{}.json'.format(_bibcode)

def build_filename_paperinfo(_bibcode:str) -> str:
    """
    Builds the name for the paperinfo output file
    """
    return '{}_paperinfo.json'.format(_bibcode)

def build_filename_citationsfile(_bibcode:str) -> str:
    """
    Builds the name for the citations output file
    """
    return '{}_citations.json'.format(_bibcode)