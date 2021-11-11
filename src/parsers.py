import json
import re

def parse_info_papers(_bibtexs:str, **kwargs) -> list:
    """
    Parse the bibtex string and return a list of lists with the information
    
    It is anticipated that _bitexs has the format %l;%Y;%j;%J;%V;%p;%q;%K;%pp;%pc;%R;%S;%T;%u\n according to the documentation (https://ui.adsabs.harvard.edu/help/actions/export)
    """
    # Split per paper
    _result = _bibtexs.split('\n\n')
    
    # Split information
    _result = [pp.split(';') for pp in _result]   
    
    return _result[:-1] # Do not take last blank element

def paperinfo_list2dict(_bibtexl: list, **kwargs) -> list:
    """
    Convert the bibtex list of lists (of format %l;%Y;%j;%J;%V;%p;%q;%K;%pp;%pc;%R;%S;%T;%u) to a list of dicts
    """
    # Key names in the format
    _keys = ['authors', 'year', 'journal tex', 'journal full', 'volume', 'page first', 
             'journal abbreviation', 'keywords', 'page range', 'page count', 'bibcode', 'issue', 'title', 'url']
    
    # List comprehension around dict comprehension
    _result = [{_keys[ii]:bb[ii] for ii in range(len(bb))} for bb in _bibtexl]
    
    return _result

def parse_authorlist(_authorlist:str, **kwargs) -> list:
    """
    Parse the string of authors to retrieve the list of individual authors
    """
    # Anticipated to result in length / 2 = number of authors
    _temp = _authorlist.split(', ')
    
    # Some basic cleaning
    _temp = [ii.replace('&', '').strip() for ii in _temp]
    
    # Differentiate to extract collaborations
    if len(_temp) % 2 == 0:
        _result = [', '.join([_temp[ii * 2], _temp[ii * 2 + 1]]) for ii in range(len(_temp) // 2)]
    elif len(_temp) % 2 == 1:
        _result = [', '.join([_temp[ii * 2], _temp[ii * 2 + 1]]) for ii in range(len(_temp) // 2 - 1)]
        _result += [_temp[-1]]
    
    return _result

def parse_keywordlist(_keywords:str, **kwargs) -> list:
    """
    Parse the string of keywords to retrieve the list of keywords
    """
    _result = _keywords.split(',')
    
    # Some basic cleaning
    _result = [ii.strip() for ii in _result]
    
    return _result

def enrich_paperinfo_abstract(_paperinfos:list, _abstracts:dict) -> dict:
    """
    Enrich the list of information on the papers with their abstracts.  The matching happens on bibcode.
    """
    # Fill with a try-and-except statement
    for ii, _paper in enumerate(_paperinfos):
        try:
            _abstract = _abstracts[_paper['bibcode']]
            _paperinfos[ii]['abstract'] = _abstract
        except:
            _paperinfos[ii]['abstract'] = ''
    
    return _paperinfos    