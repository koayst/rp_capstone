#!pip install streamlit

# streamlit run extractiveUI_streamlit.py

import json
import pandas as pd
from PIL import Image
import requests
import streamlit 

FLASK_SERVER_URL = 'http://127.0.0.1:5500/url' 

rp_logo_img = Image.open('img\\rplogo.png')
streamlit.image(rp_logo_img, width=500, caption='Tech Immersion Placement Programme - Version 0.01 (Intake 1 2020)', format='PNG')

url_text = streamlit.sidebar.text_input('URL:', 'http://')

url_summarize_btn = streamlit.sidebar.button('Summarize')
if url_summarize_btn:

    # json.loads expect a string as input
    # it then convert it to a dict
    payload = json.loads (
        '{"search_url": ' + '"' + url_text  + '"}'
    )

    resp = requests.post(FLASK_SERVER_URL, json=payload)
    dataFile = resp.json()
    
    print(dataFile['filename'])

    # Display a title
    '''
    # Extractive Summarizer

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

streamlit_balloons_btn = streamlit.sidebar.button('Balloons!')
if streamlit_balloons_btn:
    streamlit.balloons()
