#!pip install streamlit
#
# to run:
# streamlit run extractiveUI_streamlit.py

import json
import pandas as pd
from PIL import Image
import requests
import streamlit 

def getSummary(engine_url, web_url):
     # json.loads expect a string as input
    # it then convert it to a dict
    payload = json.loads (
        '{"search_url": ' + '"' + web_url  + '"}'
    )

    resp = requests.post(engine_url, json=payload)
    dataFile = resp.json()
    
    print(dataFile['filename'])

    # Display a title
    '''
    ## Extractive Summarizer
    '''

    # load the summarized data.
    df = pd.read_csv(dataFile['filename'])

    # print the document title
    streamlit.title(df.columns[0])

    # indexes of the extractive summarizer
    summarized = df.loc[df.iloc[:, 0].str.contains('<hl>')].index.tolist()
    agree = []

    for i in range(len(df)):
        agree.append(streamlit.checkbox(df.loc[i][0], value=(i in summarized), key=i))

# initialisation
ENGINE_URL_TEXT_DEFAULT = 'http://127.0.0.1:5500/url'
WEB_URL_TEXT_DEFAULT = 'http://'

rp_logo_img = Image.open('img\\rplogo.png')
streamlit.image(rp_logo_img, width=500, caption='Tech Immersion Placement Programme - Version 0.01 (Intake 1 2020)', format='PNG')

engine_url_text = streamlit.sidebar.text_input('Extractive Summary Engine:', ENGINE_URL_TEXT_DEFAULT)
web_url_text = streamlit.sidebar.text_input('Web Site URL:', WEB_URL_TEXT_DEFAULT)

url_summarize_btn = streamlit.sidebar.button('Summarize')
if url_summarize_btn:
    getSummary(engine_url_text, web_url_text)
   
# add line spaces to push the 'clear' button near to the bottom of screen
streamlit.sidebar.markdown('<br/><br/><br/>', unsafe_allow_html=True)

streamlit_clear_btn = streamlit.sidebar.button('Clear')
if streamlit_clear_btn:
    streamlit.balloons()

# hide the 'Make with Streamlit' footer at bottom of web page
hide_streamlit_style = """
            <style>
            //#MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True) 
