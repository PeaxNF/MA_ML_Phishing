import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import pickle
from urllib.parse import urlparse
import tldextract
import time

def collectdata(url,outputpath):
    try:
        #time.sleep(2)
        x = requests.get(url,timeout=5)
        print(x.text)
        if(len(x.text) > 0):
            filename=tldextract.extract(url).domain+'_'+str(round(time.time() * 10**6))+'.html'
            with open(outputpath+'/'+filename, 'wb') as f:
                f.write(x.content)
            print(url)
            return filename
            #print(filename)
        else:
            print('Length ' + str(len(x.text)))
            return 0
#         with open('files/'+filename, 'wb') as f:
#             f.write(x.content)
#         return filename
    except Exception as error:
        print(error)
        return 0