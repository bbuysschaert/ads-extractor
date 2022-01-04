# ads-extractor
This streamlit application extracts the information of scientific papers from the [NASA ADS website](https://ui.adsabs.harvard.edu/).  This is to prepare a dataset for a graph database project in a later stage.

Information on the API of NASA ADS can be found at the following locations:
- https://ui.adsabs.harvard.edu/help/api/
- https://ui.adsabs.harvard.edu/help/search/search-syntax


## Dependencies:
To be added in a dependencies.txt

## Caveats

### Rate limit greedy
The current setup does not work smartly with the daily API call limit, by not combining the different queries.  Instead, the different queries to the API are repeated for each individual paper, identified by its bibcode, instead of grouping these API calls for mulitiple papers.  This is done as it requires less bookkeeping of which information is already collected, but comes at the price of a significant increase in API calls needed.

### Collection vs tree-like
The current implementation to follow links (like citations, references, and authors) works as an iterative function that expands like a tree.  The function determines the links from the input paper and follows each of these a branch down.  At each branch, the function enforces the uniqueness of the coming leaves.  However, it cannot guarantee that a leaf already exists at another branch.  If both leaves are not executed simultaneously, one will be read from file.

## To do:
- rate limit checker
- checker whether reference exists
- extractor on author name
- forward author list to extractors
- check whether citations and bibinfo exists
- split bibinfo from citations
- check whether HTML documentation is an option for the code
- perform parallelism 