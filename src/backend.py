import extractors as E
import parsers as P
import loaders as L

def lookup_paper(_bibcode:str, _apitoken:str, **kwargs):
    """
    Get all information for the paper specified by the bibcode and parse the information
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
    _infos = _infos[0]

    # Parse individual information keys
    _infos['authors'] = P.parse_authorlist([_infos['authors']])
    _infos['keywords'] = P.parse_keywordlist([_infos['keywords']])
    
    # Combine all information
    _infos['citations'] = _cits
    _infos['references'] = _refs
    return _infos

def follow_papers(_bibcode:str, _apitoken:str, _levels=0, **kwargs):
    """
    Perform an iterative lookup and extraction starting from _bibcode.
    Will fetch a result for all citations and references and this for the specified number of _levels.

    Will only look at the paper itself with _levels=0
    """
    _info = lookup_paper(_bibcode, _apitoken)
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
                _temp.append(lookup_paper(cc, _apitoken))
            for rr in _refs:
                _temp.append(lookup_paper(rr, _apitoken))

            # Get all citations and references out
            _cits = [cc for tt in _temp for cc in tt['citations']]
            _refs = [rr for tt in _temp for rr in tt['references']]

            # Append to the _infos object
            _infos += _temp
            
    return _infos






if __name__ == '__main__':
    token = ''
    bibcode = '2019A&A...622A..67B'


