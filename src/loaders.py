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