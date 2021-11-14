import streamlit as st
import backend as app

def header():
    """
    """
    st.markdown('# ADS bibtex extractor')
    st.text('Please provide the API token and bibcode in the sidebar')
    st.sidebar.markdown('# Input variables')
    
def main():
    """
    Set up the streamlit application
    """
    # Header
    header()

    # Input fields    
    _token = st.sidebar.text_input('ADS API token', '')
    _bibcode = st.sidebar.text_input('Starting bibcode', '')
    _outputpath = st.sidebar.text_input('Output folder', '')
    _levels = st.sidebar.selectbox('Levels', [0,1,2])

    # Start extracting
    if st.button('Start extracting'):
        with st.spinner('Starting extracting now -- Please wait'):
            app.follow_papers(_bibcode=_bibcode,
                              _apitoken=_token, 
                              _path=_outputpath,
                              _levels=_levels
            )


if __name__ == '__main__':
    main()