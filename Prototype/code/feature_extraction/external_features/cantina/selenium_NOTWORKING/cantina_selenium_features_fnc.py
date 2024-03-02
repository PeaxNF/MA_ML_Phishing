from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import tldextract
import pandas as pd
from random import randrange
from bs4 import BeautifulSoup

def get_html(htmlfile):
    with open('../../../dataset/htmldataset/' + htmlfile) as fp:
        soup = BeautifulSoup(fp, 'html.parser',multi_valued_attributes=None)
        return soup    

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def cantina_features(inputdataframe):
   outputdataframe = pd.DataFrame()
   outputdataframe["cantina"]=inputdataframe.apply(lambda x: cantina(get_html(x.website),x.domaintld), axis='columns', result_type='expand')
   return outputdataframe

def selenium_search_google(query):
    links=[]
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    time.sleep(randrange(1,3))
    driver.get('https://google.com')

    time.sleep(randrange(5,8))
    
    search = driver.find_element(By.NAME, "q")
    search.send_keys(query)
    time.sleep(randrange(3,6))
    search.send_keys(Keys.RETURN)
    time.sleep(randrange(1,4))
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(randrange(1,4))
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")
    for result in search_results:

        link_element = result.find_element(By.CSS_SELECTOR, "a")
        link = link_element.get_attribute("href")
        links.append(link)
    

    time.sleep(1)
    driver.close()
    time.sleep(1)
    driver.quit()
    return links       

def cantina(htmlobject,domaintld, num_words=5,add_domain=1):
    tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english')
    try:
        tfidf = tfidfvectorizer.fit_transform([htmlobject.get_text()]).toarray()
        index_top_words = tfidf.max(axis=0).argsort()[-num_words:]
        tfidf_words = tfidfvectorizer.get_feature_names_out()
        search_words = tfidf_words[index_top_words]
        if add_domain == 1:
            search_words = np.append(search_words, domaintld)
        googlesearch = ' '.join(search_words)
        time.sleep(3)
        links=selenium_search_google(googlesearch)
        for result in links:
            hyperlink=tldextract.extract(result).domain+'.'+ tldextract.extract(result).suffix
            print('searchresults: '+hyperlink + " Domaintld: "+ domaintld)
            if hyperlink == domaintld:
                return 1
       
        print('Not Found')

        return 0
                
    except Exception as error:
        print(error)
        return 0     

