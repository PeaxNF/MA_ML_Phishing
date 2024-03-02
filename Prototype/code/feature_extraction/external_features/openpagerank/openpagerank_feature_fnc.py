from bs4 import BeautifulSoup
import requests
import pandas as pd


def openpagerank(domaintld):
    headers = {'API-OPR':'<API-KEY-HERE>'}
    print(domaintld)
    url = 'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + domaintld
    request = requests.get(url, headers=headers)
    result = request.json()
    print(result)
    if result['response'][0]['rank']:
        return result['response'][0]['rank'],result['response'][0]['page_rank_integer']
    else:
        return 0, 0
    

def openpagerank_features(inputdataframe):
   outputdataframe = pd.DataFrame()
   outputdataframe[["openpagerank","openpagescore"]]=inputdataframe.apply(lambda x: openpagerank(x.domaintld), axis='columns', result_type='expand')
   return outputdataframe