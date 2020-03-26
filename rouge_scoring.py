#pip install rouge

import pandas as pd
import argparse

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
    
    bertdf = cleanedbert[berttitle].tolist()
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rouge Scoring')
    parser.add_argument('filename_1', help='CSV file of BERT summarizer of a searched URL', nargs='?')
    parser.add_argument('filename_2', help='CSV file user changes', nargs='?')
    args = parser.parse_args()

    if args.filename_1 is not None and args.filename_2 is not None:

        #input 2 csv file and convert it to dataframe
        bert = pd.read_csv(args.filename_1)
        user = pd.read_csv(args.filename_2)

        #scoring (machine, human) - this order is important
        scoring(bert,user)
    else:
        # print usage help if either file name is not provided
        print(parser.print_help())