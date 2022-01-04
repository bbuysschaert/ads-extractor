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
    _info['authors'] = P.parse_authorlist(_info['authors'])
    _info['keywords'] = P.parse_keywordlist(_info['keywords'])
    
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
        return _info
    else:
        # Retrieve the information from ADS
        try:
            _info = retrieve_paper_from_ADS(_bibcode, _apitoken, **kwargs)
            
            # Write out the information to a file
            L.write_data(_info, _path=_path)
            return _info
        except:
            L.write_error(_bibcode, _path=_path)
            return None

def follow_papers_old(_bibcode:str, _apitoken:str, _path='./', _levels=0, **kwargs) -> list:
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
                    _temp.append(retrieve_paper(cc, _apitoken, _path=_path)) # Should actually have levels here?
                except:
                    L.write_error(cc, _path=_path)
            for rr in _refs:
                try:
                    _temp.append(retrieve_paper(rr, _apitoken, _path=_path)) # Should actually have levels here?
                except:
                    L.write_error(rr, _path=_path)

            # Get all citations and references out for the next level
            _cits = [cc for tt in _temp for cc in tt['citations']]
            _refs = [rr for tt in _temp for rr in tt['references']]

            # Append to the _infos object
            _infos += _temp
            
    return _infos

def follow_paper(_bibcode:str, _apitoken:str, _path='./', _nlevels=0, **kwargs) -> list:
    """
    Perform an iterative lookup and extraction starting from _bibcode.
    Will fetch a result for all citations and references and this for the specified number of _levels.

    Optional arguments:
        _followcitations: follow citations as links (defaults to True)
        _followreferences: follow references as links (defaults to True)
        _followauthors: follow authors as links (defaults to False)
    """
    # Get the information for specified paper
    _info = retrieve_paper(_bibcode, _apitoken, _path=_path, **kwargs)
    _infos = [_info]
    
    # Follow the different levels of links in the paper
    if _nlevels > 0:
        
        # Empty lists
        _links = [] # will contain bibcodes
        _level = [] # will contain paper dicts
        
        # Check which information to follow
        if kwargs.get('_followcitations', True):
            _links += _info['citations']
        if kwargs.get('_followreferences', True):
            _links += _info['references']
        if kwargs.get('_followauthors', False):
            _authors = _info['authors']
            for aa in _authors:
                _links += E.get_bibcodes_author(aa, _apitoken, **kwargs)
    
        # Determine uniqueness of the links
        _links = list(set(_links))
    
        # Loop through the different links
        # TODO Should be multithreaded through a worker pool 
        for ll in _links:
            _level.append(follow_paper(ll, _apitoken, _path=_path, _nlevels=_nlevels-1, **kwargs))
   
        # Flatten the level
        _level = [pp for ll in _level for pp in ll]
        _infos += _level
        
    # Ensure no duplicate information is passed above
    # _infos = list(set(_infos)) will not work
    
    return _infos





if __name__ == '__main__':
    path = 'C:\\Users\\bramb\\Desktop\\ads-extractor\\bibcodes'
    token = ''
    bibcode = '2019A&A...622A..67B'
    info = follow_paper(bibcode, token, path, _nlevels=2)
    print(len(info))


