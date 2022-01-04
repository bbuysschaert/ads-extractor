import json
import os.path

def write_data(_info:dict, _path='./', **kwargs):
    """
    Write the info object as a json at _path.  The filename is the bibcode
    """
    _filename = _info['bibcode'] + '.json'
    with open(os.path.join(_path, _filename), 'w') as _out:
        json.dump(_info,
                _out,
                indent=1
                )
    return

def read_data(_inputfile:str, **kwargs) -> dict:
    """
    Read the info object of a paper form a json file at _inputfile.
    Returns a dict with the info object
    """
    with open(_inputfile, 'r') as _in:
        _info = json.load(_in)
    return _info

def write_paperinfo(_info:dict, _path='./', **kwargs):
    """
    Write the info object of a paper as a json at _path.  The filename contains the bibcode
    """
    _filename = _info['bibcode'] + '_paperinfo.json'
    with open(os.path.join(_path, _filename), 'w') as _out:
        json.dump(_info,
                _out,
                indent=1
                )
    return

def write_papercitations(_info:dict, _path='./', **kwargs):
    """
    Write the citations of a paper as a json at _path.  The filename contains the bibcode
    """
    _filename = _info['bibcode'] + '_citations.json'

    # Subset the information
    _info = {_key:_info[_key] for _key in ['bibcode', 'citations']}
    with open(os.path.join(_path, _filename), 'w') as _out:
        json.dump(_info,
                _out,
                indent=1
                )
    return

def write_error(_bibcode:str, _path='./', **kwargs):
    """
    Write the bibcode to a separate file to trace which bibcodes could not be searched and parsed
    """
    _filename = _bibcode + '.json'
    _info = {'bibcode':_bibcode}
    with open(os.path.join(_path, 'logs', _filename), 'w') as _out:
        json.dump(_info,
                _out,
                indent=1
                )