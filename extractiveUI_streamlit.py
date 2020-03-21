#!pip install streamlit
#
# to run:
# streamlit run extractiveUI_streamlit.py

import json
import pandas as pd

from PIL import Image

import requests
import streamlit 

import urllib.request, urllib.error

@streamlit.cache(suppress_st_warning=True)
def getSummary(engine_url, web_url):
    if web_url.lstrip().rstrip() == 'http://':
        return (pd.DataFrame(), [])

    # json.loads expect a string as input
    # it then convert it to a dict
    payload = json.loads (
        '{"search_url": ' + '"' + web_url  + '"}'
    )

    # send a post to flask to get a summarized csv file
    resp = requests.post(engine_url + '/url', json=payload)
    dataFile = resp.json()
    
    #print(dataFile['filename'])

    # Display a title
    '''
    ## Extractive Summarizer
    '''

    # load the summarized data
    df = pd.read_csv(dataFile['filename'])

    # print the document title
    streamlit.title(df.columns[0])

    # indexes of the extractive summarizer
    summarized = df.loc[df.iloc[:, 0].str.contains('<hl>')].index.tolist()

    # return the dataframe and
    # list of indexes
    return (df, summarized)

# initialisation
ENGINE_URL_TEXT_DEFAULT = 'http://127.0.0.1:5500'
WEB_URL_TEXT_DEFAULT = 'http://'

# --- Side Bar ---

engine_url_text = streamlit.sidebar.text_input('Extractive Summary Engine:', ENGINE_URL_TEXT_DEFAULT)
web_url_text = streamlit.sidebar.text_input('Web Site URL:', WEB_URL_TEXT_DEFAULT)

summarize_btn = streamlit.sidebar.button('Summarize')
if summarize_btn:
    try:
        conn = urllib.request.urlopen(web_url_text)
    except urllib.error.HTTPError as e:
        streamlit.write('There is a HTTP error. Please check.')
    except urllib.error.URLError as e:
        streamlit.write('There is an URL error. Please check.')

# add line spaces to push the 'clear' button near to the bottom of screen
#streamlit.sidebar.markdown('<br/><br/><br/>', unsafe_allow_html=True)
for _ in range(8):
    streamlit.sidebar.text(' ')
    
streamlit.sidebar.title("About")
streamlit.sidebar.info(
    "**Capstone Project**\n"
    "TIPP (Intake 1) - Mar 2020. "
    
)

test_btn = streamlit.sidebar.button('Test')
if test_btn:
    streamlit.balloons()

# --- Side Bar ---

# --- Main --
rp_logo_img = Image.open('img\\rplogo.png')
streamlit.image(rp_logo_img, width=500, caption='Tech Immersion Placement Programme - Version 0.01 (Intake 1 2020)', format='PNG')

streamlit.markdown('<hr>', unsafe_allow_html=True)

df, summarized = getSummary(engine_url_text, web_url_text)
# create the summary lines as checkboxes
for i in range(len(df)):
    streamlit.checkbox(df.loc[i][0], value=(i in summarized), key=i)

# --- Main ---
   
# hide the 'Make with Streamlit' footer at bottom of web page
hide_streamlit_style = """
            <style>
            //#MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True) 
