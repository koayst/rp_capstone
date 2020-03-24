#!pip install streamlit
#
# to run:
# streamlit run extractiveUI_streamlit.py
#
# Observation:
# Ref: https://docs.streamlit.io/main_concepts.html#data-flow
# Streamlit architecture is based on the ability to write apps the same way a plain
# Python scripts is written.  Streamlit apps have a unique data flow: any time 
# something must be updated on the screen (for example, responding to a button is 
# pressed), Streamlit will just rerun the entire Python script from top to bottom.
#
# This will pose a challenge for the app developer because it is not implemented
# as a 'callback', like most web apps will function.  
#
# Some of these quirks can be 'hacked' using Streamlit's cache (streamlit@cache) 
# decorator which allows developers to skip certain costly computations when their 
# apps rerun.  Being a hack, some times it will not work perfectly.  

import json
import os
import pandas as pd

from urllib.parse import urlparse
from PIL import Image

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
    if not urlProperlyFormed(web_url):
        return (pd.DataFrame(), [], '')
    # if URL is http:// or https://
    elif web_url == 'http://' or web_url == 'https://':
        return (pd.DataFrame(), [], '')
    elif not urlReachable(web_url):
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

# --- Side Bar BEGIN ---

engine_url_text = streamlit.sidebar.text_input('Extractive Summary Engine:', ENGINE_URL_TEXT_DEFAULT)
web_url_text = streamlit.sidebar.text_input('Web Site URL:', WEB_URL_TEXT_DEFAULT)

# add line spaces to push the 'clear' button near to the bottom of screen
for _ in range(5):
    streamlit.sidebar.text('')

if streamlit.sidebar.button('Save'):
    print('Saved !\n\n')
    for i in range(len(selected)):
        print('{}: is {}'.format(i, selected[i]))
        
for _ in range(2):
    streamlit.sidebar.text('')
    
streamlit.sidebar.markdown(
    "**Capstone Project:**<br />"
    "TIPP (Intake 1 - Mar 2020)<br />",
    unsafe_allow_html=True
)

if streamlit.sidebar.button('Fun!'):
    streamlit.balloons()

# --- Side Bar END ---

# --- Main BEGIN --
rp_logo_img = Image.open(os.path.join('img', 'rplogo.png'))
streamlit.image(rp_logo_img, width=400, format='PNG')
streamlit.markdown('<hr>', unsafe_allow_html=True)

df, summarized, title_txt = getSummary(engine_url_text, web_url_text)

selected = []
if len(title_txt) > 0:
    # print the document title
    streamlit.title(title_txt)

    # create the summary lines as checkboxes
    for i in range(len(df)):
        selected.append(streamlit.checkbox(df.loc[i][0], value=(i in summarized), key=i))
    
# --- Main END ---
   
# hide the 'Make with Streamlit' footer at bottom of web page
hide_streamlit_style = """
            <style>
            //#MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
streamlit.markdown(hide_streamlit_style, unsafe_allow_html=True) 


