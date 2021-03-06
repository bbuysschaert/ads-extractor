import os

import extractors as E
import parsers as P
import loaders as L
import helpers as H

def retrieve_paper_from_ADS(_bibcode:str, _apitoken:str, **kwargs) -> dict:
    """
    Get all the information for the paper specified by the bibcode from ADS.
    The information is subsequently parsed and returned as a dictionnary.
    """
    # Extract the info from ADS
    _refs = E.get_references_paper(_bibcode, _apitoken)
    _cits = E.get_citations_paper(_bibcode, _apitoken)
    _infos = E.get_info_papers([_bibcode], _apitoken)
    _abs = E.get_abstract_papers([_bibcode], _apitoken)

    # Parse the information object
    _infos = P.parse_info_papers(_infos)
    _infos = P.paperinfo_list2dict(_infos)

    # Add abstract
    _infos = P.enrich_paperinfo_abstract(_infos, _abs)

    # Only have one paper here
    assert len(_infos) == 1, f'Got more papers out than expected for bibcode {_bibcode}'
    _info = _infos[0]

    # Parse individual information keys
    _info['authors'] = P.parse_authorlist([_info['authors']])
    _info['keywords'] = P.parse_keywordlist([_info['keywords']])
    
    # Combine all information
    _info['citations'] = _cits
    _info['references'] = _refs
    return _info

def retrieve_paper_from_file(_bibcode:str, _path='./', **kwargs) -> dict:
    """
    Get all the information for the paper specified by the bibcode from a file.  It is expected that this file was created during an earlier run.

    Returns the paper information as a dictionnary object.
    """
    # Build the filename
    _filename = H.build_filename_data(_bibcode)
    _filename = os.path.join(_path, _filename)
    _info = L.read_data(_filename, **kwargs)
    return _info

def retrieve_paper(_bibcode:str, _apitoken:str, _path='./', **kwargs) -> dict:
    """
    Get all the information for the paper specified by the bibcode.  
    The function will first check if the information exists at the path.
    If it does, it will retrieve the information from the file.
    If not, it will retrieve the information from ADS and store it to a file.
    
    Returns the paper information as a dictionnary object.
    """
    # Build the filename to check it
    _filename = H.build_filename_data(_bibcode)
    _filename = os.path.join(_path, _filename)

    if (H.check_if_dir_exists(_path)) & (H.check_if_file_exists(_filename)):
        # Retrieve the information from file
        _info = retrieve_paper_from_file(_bibcode, _path, **kwargs)
    else:
        # Retrieve the information from ADS
        _info = retrieve_paper_from_ADS(_bibcode, _apitoken, **kwargs)
        
        # Write out the information to a file
        L.write_data(_info, _path=_path)

    return _info

def follow_papers(_bibcode:str, _apitoken:str, _path='./', _levels=0, **kwargs) -> list:
    """
    Perform an iterative lookup and extraction starting from _bibcode.
    Will fetch a result for all citations and references and this for the specified number of _levels.

    Will only look at the paper itself with _levels=0
    """
    _info = retrieve_paper(_bibcode, _apitoken, _path=_path)
    _infos = [_info]

    # Look at the paper itself
    if _levels == 0:
        return _infos
    
    elif _levels > 0:
        # Extract the citations and references
        _cits = _info['citations']
        _refs = _info['references']

        # Start building iteratively
        for ll in range(_levels):
            # Blank list for appending
            _temp = []

            for cc in _cits:
                try:
                    _temp.append(retrieve_paper(cc, _apitoken, _path=_path))
                except:
                    L.write_error(cc, _path=_path)
            for rr in _refs:
                try:
                    _temp.append(retrieve_paper(rr, _apitoken, _path=_path))
                except:
                    L.write_error(rr, _path=_path)

            # Get all citations and references out for the next level
            _cits = [cc for tt in _temp for cc in tt['citations']]
            _refs = [rr for tt in _temp for rr in tt['references']]

            # Append to the _infos object
            _infos += _temp
            
    return _infos






if __name__ == '__main__':
    token = ''
    bibcode = '2019A&A...622A..67B'


