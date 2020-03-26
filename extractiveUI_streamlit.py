#!pip install streamlit
#
# Date Created: 1 March 2020
#
# To run:
# streamlit run extractiveUI_streamlit.py
#
# Ref: https://docs.streamlit.io/main_concepts.html#data-flow
# Streamlit architecture is based on the ability to write apps the same way a plain
# Python scripts is written.  Streamlit apps have a unique data flow: any time 
# something must be updated on the screen (for example, when a button is pressed)
# Streamlit will just rerun the entire Python script from top to bottom.
#
# This will pose a challenge for the app developer because it is not implemented
# as a 'callback', like most web apps will function.  
#
# Some of these quirks could be 'hacked' using Streamlit's cache (streamlit@cache) 
# decorator which allows developer to skip certain costly computations when their 
# app is rerun.  Being a hack, some times it will not work unexpectedly.  Also
# not easy to debug.  

import json
import os
import pandas as pd

from numpy import asarray
from PIL import Image
from urllib.parse import urlparse

import requests
import streamlit 

import urllib.request, urllib.error

# test whether URL is properly formed
def urlProperlyFormed (url):
    try:
        result = urlparse(url)    
        #all() returns true if all the variables inside it return true
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# test whether URL is 'internet' reachable  
def urlReachable(url):
    try:
        conn = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        streamlit.warning('There is a HTTP error. Please check.')
        return False
    except urllib.error.URLError as e:
        streamlit.warning('There is an URL error. Please check.')
        return False
    else:
        return True

# the function is cached as explained in observation above
@streamlit.cache(suppress_st_warning=True, show_spinner=False)
def getSummary(engine_url, web_url):

    #strip spaces before and after the URL
    engine_url = engine_url.lstrip().rstrip()
    web_url = web_url.lstrip().rstrip()

    # if URL is not valid
    # if URL is (empty) either 'http://' or 'https://'
    # if URL is not reachable
    if not urlProperlyFormed(web_url) or (web_url == 'http://' or web_url == 'https://') or not urlReachable(web_url):
        return ('', pd.DataFrame(), [], '')
    
    # the json object to be sent across
    payload = {
        'search_url' : web_url
    }

    # send a post to flask to get a summarized csv filename
    resp = requests.post(engine_url + '/url', json=payload)
    dataFile = resp.json()
    
    #print('filename: ', dataFile['filename'])

    # load the summarized data
    df = pd.read_csv(dataFile['filename'])

    # indexes of the extractive summarizer
    summarized = df.loc[df.iloc[:, 0].str.contains('<hl>')].index.tolist()

    # return the csv filename, dataframe, indexes and title
    return (dataFile['filename'], df, summarized, df.columns[0])

# initialisation
ENGINE_URL_TEXT_DEFAULT = 'http://127.0.0.1:5500'
WEB_URL_TEXT_DEFAULT = 'http://'

# --- Side Bar BEGIN ---

engine_url_text = streamlit.sidebar.text_input('Extractive Summary Engine:', ENGINE_URL_TEXT_DEFAULT)
web_url_text = streamlit.sidebar.text_input('Web Site URL:', WEB_URL_TEXT_DEFAULT)

# add line spaces to push the 'Save' button near to the bottom of screen
for _ in range(1):
    streamlit.sidebar.text('')

save_btn = streamlit.sidebar.button('Save')        
streamlit.sidebar.markdown('<hr>', unsafe_allow_html=True)        
    
streamlit.sidebar.markdown(
    "**Capstone Project:**<br />"
    "TIPP (Intake 1 - Mar 2020)<br />",
    unsafe_allow_html=True
)

streamlit.sidebar.info('Extractive Summarizer using BERT transformer model.')

if streamlit.sidebar.button('Fun!'):
    streamlit.balloons()

# --- Side Bar END ---

# --- Main BEGIN --
rp_logo_img = Image.open(os.path.join('img', 'rplogo.png'))
rp_logo_array = asarray(rp_logo_img)
nvidia_logo_img = Image.open(os.path.join('img', 'nvidia_logo.png'))
nvidia_logo_array = asarray(nvidia_logo_img)

streamlit.image([nvidia_logo_array, rp_logo_array], width=300, format='PNG')
streamlit.markdown('<hr>', unsafe_allow_html=True)

fn, df, summarized, title_txt = getSummary(engine_url_text, web_url_text)

selected = []
if len(title_txt) > 0:
    # print the document title
    streamlit.title(title_txt)

    # create the summary lines as checkboxes
    for i in range(len(df)):
        selected.append(streamlit.checkbox(df.loc[i][0], value=(i in summarized), key=i))
    
# --- Main END ---
      
if save_btn:
    #print('Save button pressed!\n\n')
    
    idxs = []
    for i in range(len(selected)):
        if selected[i]:
            idxs.append(i)
    payload = {
        'filename' : fn,
        'indexes' : idxs
    }
    
    # send the filename and indexes to be updated to server
    resp = requests.post(engine_url_text + '/update', json=payload)
       
# hide the 'Make with Streamlit' footer at bottom of web page
hide_streamlit_style = """
            <style>
            //#MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True) 


