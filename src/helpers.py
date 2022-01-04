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