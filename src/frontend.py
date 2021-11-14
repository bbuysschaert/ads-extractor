import streamlit as st

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
    _level = st.sidebar.selectbox('Level', [1,2,3])

    # Start extracting
    if st.button('Start extracting'):
        with st.spinner('Starting extracting now -- Please wait'):
            from time import sleep
            sleep(5)

if __name__ == '__main__':
    main()