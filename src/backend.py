import extractors as E
import parsers as P
import loaders as L

def lookup_paper(_bibcode:str, _apitoken:str):
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







if __name__ == '__main__':
    token = ''
    bibcode = '2019A&A...622A..67B'


