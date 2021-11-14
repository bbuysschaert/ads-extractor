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