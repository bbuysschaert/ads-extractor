# ads-extractor
This streamlit application extracts the information of scientific papers from the [NASA ADS website](https://ui.adsabs.harvard.edu/).  This is to prepare a dataset for a graph database project in a later stage.

Information on the API of NASA ADS can be found at the following locations:
- https://ui.adsabs.harvard.edu/help/api/
- https://ui.adsabs.harvard.edu/help/search/search-syntax


### Dependencies:
To be added in a dependencies.txt

### To do:
- rate limit checker
- checker whether reference exists
- extractor on author name
- forward author list to extractors
- check whether citations and bibinfo exists
- split bibinfo from citations
- check whether HTML documentation is an option for the code
- perform parallelism 