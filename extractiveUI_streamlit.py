#!pip install streamlit
#
# to run:
# streamlit run extractiveUI_streamlit.py

import json
import os
import pandas as pd

from PIL import Image

import requests
import streamlit 

import urllib.request, urllib.error

#print('***** BEGIN')

@streamlit.cache(suppress_st_warning=True)
def getSummary(engine_url, web_url):
    if web_url.lstrip().rstrip() == 'http://':
        return (pd.DataFrame(), [], '')

    # json.loads expect a string as input
    # it then convert it to a dict
    payload = json.loads (
        '{"search_url": ' + '"' + web_url  + '"}'
    )

    # send a post to flask to get a summarized csv file
    resp = requests.post(engine_url + '/url', json=payload)
    dataFile = resp.json()
    
    #print(dataFile['filename'])

    # load the summarized data
    df = pd.read_csv(dataFile['filename'])

    # indexes of the extractive summarizer
    summarized = df.loc[df.iloc[:, 0].str.contains('<hl>')].index.tolist()

    # return the dataframe and
    # list of indexes
    return (df, summarized, df.columns[0])

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
for _ in range(9):
    streamlit.sidebar.text(' ')
    
streamlit.sidebar.markdown(
    "**Capstone Project:**<br />"
    "TIPP (Intake 1 - Mar 2020)<br />",
    unsafe_allow_html=True
)

test_btn = streamlit.sidebar.button('Fun!')
if test_btn:
    streamlit.balloons()

# --- Side Bar ---

# --- Main --
rp_logo_img = Image.open(os.path.join('img', 'rplogo.png'))
streamlit.image(rp_logo_img, width=400, format='PNG')
streamlit.markdown('<hr>', unsafe_allow_html=True)

df, summarized, title_txt = getSummary(engine_url_text, web_url_text)

if len(title_txt) > 0:
    # print the document title
    streamlit.title(title_txt)

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

#print('***** END')
