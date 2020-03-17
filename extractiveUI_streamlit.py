import pandas as pd
from PIL import Image
import streamlit 

rp_logo_img = Image.open('img\\rplogo.png')
streamlit.image(rp_logo_img, caption='Republic Polytechnic (Tech Immersion Placement Programme - Intake 1 - Jan 2020)', width=400, format='PNG')

url_text_input = streamlit.sidebar.text_input('URL:', 'http://')
url_summarize_btn = streamlit.sidebar.button('Get Summary')

streamlit_balloons_btn = streamlit.sidebar.button('Balloons Test')
if streamlit_balloons_btn:
    streamlit.balloons()

if url_summarize_btn:

    # Display a title
    '''
    # Extractive Summarizer

    '''

    # load the summarized data.
    df = pd.read_csv('data\\cna_news_for_testing.csv')

    # print the document title
    streamlit.title(df.columns[0])

    # indexes of the extractive summarizer
    summarized = df.loc[df.iloc[:, 0].str.contains('<hl>')].index.tolist()
    agree = []

    for i in range(len(df)):
        agree.append(streamlit.checkbox(df.loc[i][0], value=(i in summarized)))




# # # Select some rows using st.multiselect. This will break down when you have >1000 rows.
# streamlit.write('### Full Dataset', df)
# selected_indices = streamlit.multiselect('Selected rows:', df.index.to_list(), df.loc[df.iloc[:, 0].str.contains('<hl>')].index.tolist())
# selected_rows = df.loc[selected_indices]
# streamlit.write('### Selected Rows', selected_rows)