from nltk.tokenize import sent_tokenize
from newspaper import Article
from summarizer import Summarizer
import pandas as pd
from datetime import datetime
import urllib.request, urllib.error
from gensim.summarization.summarizer import summarize


#1 get full articles
def getArticle(url):
    global urlname 
    global title

    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    full = article.text
    title = article.title

    urlname= title[0:30] #first 30 characters
    urlname = urlname.replace(" ","_")

    illegal = r"<>:/\|?*"

    for i in illegal:
        urlname = urlname.replace(i, "")
        #print(urlname)

    return full

#2: extractive summary (gensim-summarizer)
def genSumm(full):
    orgi = full
    # model = Summarizer( model ='distilbert-base-uncased') # can adjust parameters
    summa = summarize(orgi, ratio=0.2, word_count=None, split=False) # can adjust parameters
    return summa


#2: extractive summary (distilbert)
def extSumm(full):
    orgi = full
    model = Summarizer( model ='distilbert-base-uncased') # can adjust parameters
    #summa = model(orgi, ratio=0.3, min_length=60) # can adjust parameters
    summa = model(orgi, ratio=0.2, min_length=60)
    return summa

#3 cleaning up text
def cleanup(textbody):
    
    main_list =[]
    for word in range(len(textbody)):
        sentence = textbody[word].split("\n")
        main_list.append(sentence)

    main_list = [item for items in main_list for item in items] 
    
    textbody = main_list
    return textbody

# 4 tokenise text 
def tokenise(text):
    orgi = sent_tokenize(text)
    orgi = cleanup(orgi)

    summ_list = []
    for things in orgi:
        if len(things) > 20:
            summ_list.append(things)

    return summ_list

# 5 highlighting tool for summaried sentenses that are in original article
def highlight(List1, List2): 
    check = False
    global full_list
    global number
    number = []
    full_list=[]
    index_num = 0
  
    # Iterate in the 1st list 
    for m in List1: 
        full_list.append(m)
  
        # Iterate in the 2nd list 
        for n in List2: 
    
            # if there is a match
            if m == n: 
                check = True
                full_list.pop()
                #full_list.append("<hl>"+ m)
                full_list.append(m)
                number.append(index_num)

        index_num= index_num+1
    #full_list.insert(0, number)        
                 
    return full_list

# 6 clean and save (gensim)
def cleanSaveGen(full_list):
    import os
    import pandas as pd
    
    listToStr = ','.join([str(elem) for elem in number]) 
    print(listToStr)

    df = pd.DataFrame(columns=[title])
    # add the indexes to first row
    df.loc[0] = listToStr
    # add the sentences to rest of dataframe
    for i in range(len(full_list)):
        df.loc[i+1] = full_list[i]

    path = r".\data"

    now = datetime.now() # current date and time
    date_time = now.strftime("%m-%d-%Y_%H-%M-%S")

    name = urlname + "_"+ date_time + "gen.csv"
    #print(name)
    fileloc = os.path.join(path, name)
    df.to_csv (fileloc, index = False, header=True, encoding="utf-8")
    #print(fileloc)
    
    return fileloc

# 6.2 clean and save (bert)
def cleanSaveBert(full_list):
    import os
    import pandas as pd
    
    listToStr = ','.join([str(elem) for elem in number]) 
    print(listToStr)

    df = pd.DataFrame(columns=[title])
    # add the indexes to first row
    df.loc[0] = listToStr
    # add the sentences to rest of dataframe
    for i in range(len(full_list)):
        df.loc[i+1] = full_list[i]

    path = r".\data"

    now = datetime.now() # current date and time
    date_time = now.strftime("%m-%d-%Y_%H-%M-%S")

    name = urlname + "_"+ date_time + "bert.csv"
    #print(name)
    fileloc = os.path.join(path, name)
    df.to_csv (fileloc, index = False, header=True, encoding="utf-8")
    #print(fileloc)
    
    return fileloc

# use this for gensim summariser
def getSummaryGen(url):
    
    full = getArticle(url)
    summ = genSumm(full)
    
    list1 = tokenise(full)
    list2 = tokenise(summ)
    
    fullart= highlight(list1, list2)
    df = cleanSaveGen(fullart)
    #print('getSummary: ', df)
    return df    


# use this for BERT summariser
def getSummaryBert(url):
    
    full = getArticle(url)
    summ = extSumm(full)
    
    list1 = tokenise(full)
    list2 = tokenise(summ)
    
    fullart= highlight(list1, list2)
    df = cleanSaveBert(fullart)
    #print('getSummary: ', df)
    return df  

url0 = "https://www.channelnewsasia.com/news/singapore/coronavirus-covid-19-lee-hsien-loong-update-address-nation-tv-12606328"
# url1 = "https://www.channelnewsasia.com/news/singapore/palm-view-primary-student-covid-19-home-learning-extended-12601428"
# url2 = "https://www.channelnewsasia.com/news/world/coronavirus-covid-19-australia-police-restrictions-12600678"
# url3 = "https://www.channelnewsasia.com/news/sport/aston-martin-return-formula-one-2021-confirmed-12599506"

getSummaryGen(url0)
getSummaryBert(url0)

