import pandas as pd

def scoring(bertdf,userdf):
    
    #1.1 clean up bert df, extract the first row, and reset index
    bertsum = bertdf.iloc[0:1]
    bertsum =bertsum.to_string(header=False,index=False,index_names=False)
    bertsum= [int(s) for s in bertsum.split(',')]
    
    
    bertdf=bertdf.drop(0).reset_index(drop=True)
    
    #1.2 clean up user df, extract the first row, and reset index
    usersum = userdf.iloc[0:1]
    usersum =usersum.to_string(header=False,index=False,index_names=False)
    usersum= [int(s) for s in usersum.split(',')]
    
    userdf=userdf.drop(0).reset_index(drop=True)    
    
    #2.1 convert to list
    berttitle= bertdf.columns[0]
    cleanedbert =bertdf.iloc[bertsum , : ]
    
    bertdf =cleanedbert[berttitle].tolist()
    bert = ' '.join([str(elem) for elem in bertdf]) 
    
    #2.2 convert to list
    usertitle= userdf.columns[0]
    cleaneduser =userdf.iloc[usersum , : ]
    
    userdf =cleaneduser[usertitle].tolist()
    user = ' '.join([str(elem) for elem in userdf]) 
    
    
    #scoring, we use rouge-l (ROUGE-L: Longest Common Subsequence based statistics, takes sentences into account) 
    from rouge import Rouge
    
    rouge = Rouge()
    scores = rouge.get_scores(bert, user)
    f_score =scores[0]["rouge-l"]["f"]
    precision =scores[0]["rouge-l"]["p"]
    recall =scores[0]["rouge-l"]["r"]
    
    #print(f1,precision,recall)

    print("BERT: "+str(bertsum) +"\nUSER: "+str(usersum))

    
    print("\n\nROUGE scoring:\n\n"+
          "Precision is :"+"{:.2%}".format(precision)+
          "\nRecall is :"+"{:.2%}".format(recall)+
          "\nF Score is :"+"{:.2%}".format(f_score))
    
    print("\nPrecision: how much BERT summary exceeds human summary, (if less than 100% means user removed sentences)\n"
          "Recall: how much BERT summary explains the human summary, (if less than 100% means user added sentences)\n"
          "F Score: aggregation of BERT performance,(if 100% means perfect match)")
    return 

#input 2 csv file and convert it to dataframe
bert = pd.read_csv(r"C:\Users\User\Desktop\TIPP\11 NVidia project\data\testbert.csv")
user = pd.read_csv(r"C:\Users\User\Desktop\TIPP\11 NVidia project\data\testuser.csv")


#scoring (machine, human) - this order is important
scoring(bert,user)