import pandas as pd

def feature_connection(csv_list):
    for i in range(len(csv_list)):
        print(i)
        if i == 0:
            base=pd.read_csv(csv_list[i]) 
        else:    
            temp=pd.read_csv(csv_list[i])
            base=pd.concat([base, temp], axis=1, join='outer')
    return base

def dataframe_append(legit_csv_list,phishing_csv_list):
    legit=feature_connection(legit_csv_list)
    phishing=feature_connection(phishing_csv_list)
    df_final = pd.concat([legit, phishing]).reset_index(drop=True)
    return df_final