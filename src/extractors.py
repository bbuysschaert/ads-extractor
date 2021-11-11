import requests
from urllib.parse import urlencode
import json

def make_searchcalls(_equery, _header, **kwargs):
    """
    Decorator function to handle pagination and rate-limiting (to do) while making search requests
    
    Returns the list of payloads under [response][docs]
    """
    # KWARGS
    _nrows = kwargs.get('_nrows', 100)
    
    # Make the API call(s)
    _pagination = True
    _start = 0
    _docs = []
    while _pagination:
        _results = requests.get('https://api.adsabs.harvard.edu/v1/search/query?{}&rows={}&start={}'.format(_equery,
                                                                                                            _nrows,
                                                                                                            _start),
                                headers = _header
                               )
        # Get the payload out
        _temp = _results.json()['response']['docs']
        
        if len(_temp) != 0:
            _start += len(_temp)
            _docs += _temp
        elif len(_temp) == 0:
            _pagination = False
            break
    return _docs

def get_references_paper(_bibcode:str, _apitoken:str, **kwargs) -> list:
    """
    Make an API call to retrieve a list of references for a specific paper.
    
    Returns a list of bibcodes
    """
    _query = 'references(bibcode:{})'.format(_bibcode)
    _equery = urlencode({'q': _query, 'fl': 'bibcode'})
    
    _header = {'Authorization': 'Bearer ' + _apitoken}
    
    # Make the API call(s)
    _refs = make_searchcalls(_equery, _header)
    return [dd['bibcode'] for dd in _refs]

def get_citations_paper(_bibcode:str, _apitoken:str, **kwargs) -> list:
    """
    Make an API call to retrieve a list of citations for a specific paper.
    
    Returns a list of bibcodes
    """
    _query = 'citations(bibcode:{})'.format(_bibcode)
    _equery = urlencode({'q': _query, 'fl': 'bibcode'})
    
    _header = {'Authorization': 'Bearer ' + _apitoken}
    
    # Make the API call(s)
    _cits = make_searchcalls(_equery, _header)
    return [dd['bibcode'] for dd in _cits]

def get_bibtex_papers(_bibcodes:list, _apitoken:str, **kwargs) -> str:
    """
    Get the bibtex for a list of papers
    
    Returns a string of bibtex information
    """
    assert type(_bibcodes) == list, '_bibcodes needs to be a list'
    
    _payload = {'bibcode': _bibcodes}
    _spayloag = json.dumps(_payload) # (Serialize the payload)
    
    _header = {'Authorization': 'Bearer ' + _apitoken}
    
    _results = requests.post("https://api.adsabs.harvard.edu/v1/export/bibtex",
                                 headers=_header,
                                 data=_spayloag
                            )
    return _results.json()['export']

def get_info_papers(_bibcodes:list, _apitoken:str, **kwargs) -> str:
    """
    Get the bibtex and abstract for a list of paper using a custom export
    
    Returns a string of bibtex information
    """
    # Define custom format
    _format = "%l;%Y;%j;%J;%V;%p;%q;%K;%pp;%pc;%R;%S;%T;%u\n"
    
    _payload = {'bibcode': _bibcodes, 'format': _format}
    _spayloag = json.dumps(_payload) # (Serialize the payload)
    
    _header = {'Authorization': 'Bearer ' + _apitoken}
    
    _results = requests.post("https://api.adsabs.harvard.edu/v1/export/custom",
                             headers=_header,
                             data=_spayloag
                            )
    
    return _results.json()['export']

def get_abstract_papers(_bibcodes:list, _apitoken:str, **kwargs) -> dict:
    """
    Get the abstract for a list of papers (Export formats: https://ui.adsabs.harvard.edu/help/actions/export)
    
    Returns a dict with the abstract per bibcode
    """
    import re
    
    # Define custom format
    _format = "%R,%B|||" # Bibcode &  Abstract
    
    _payload = {'bibcode': _bibcodes, 'format': _format}
    _spayloag = json.dumps(_payload) # (Serialize the payload)
    
    _header = {'Authorization': 'Bearer ' + _apitoken}
    
    _results = requests.post("https://api.adsabs.harvard.edu/v1/export/custom",
                             headers=_header,
                             data=_spayloag
                            )
    # Parse the exports
    _temp = _results.json()['export'].split('|||')[:-1] # Do not take last blank element
    _temp = [pp.strip() for pp in _temp]
    #_temp = [re.search('^(.*?)\,(.*?)$', ss) for ss in _temp]
    
    return _temp
    #return {ss.group(1):ss.group(2) for ss in _temp}
    