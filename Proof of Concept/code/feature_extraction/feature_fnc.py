from urllib.parse import urlparse
import os
import tldextract
from datetime import datetime

import url_features
import pandas as pd
def domaintld(domain,tld):
  domaintld=domain+'.'+tld
  return domaintld

def parseurl(dataframeurl):
  dataframeurl['protocol']=dataframeurl['url'].apply(lambda x: urlparse(x).scheme)
  dataframeurl['subdomain']=dataframeurl['url'].apply(lambda x: tldextract.extract(x).subdomain)
  dataframeurl['domain']=dataframeurl['url'].apply(lambda x: tldextract.extract(x).domain)
  dataframeurl['tld']=dataframeurl['url'].apply(lambda x: tldextract.extract(x).suffix)
  dataframeurl['domaintld']=dataframeurl.apply(lambda x: domaintld(x.domain,x.tld), axis='columns', result_type='expand')
  dataframeurl['hostname']= dataframeurl['url'].apply(lambda x: urlparse(x).hostname)
  dataframeurl['path']=dataframeurl['url'].apply(lambda x: urlparse(x).path)
  dataframeurl['params']=dataframeurl['url'].apply(lambda x: urlparse(x).params)
  dataframeurl['query']=dataframeurl['url'].apply(lambda x: urlparse(x).query)
  dataframeurl['fragment']=dataframeurl['url'].apply(lambda x: urlparse(x).fragment)
  dataframeurl['filename']=dataframeurl['path'].apply(lambda x: os.path.basename(x))



def parseurlstring(seriesurl):
  seriesurl['protocol']=seriesurl.apply(lambda x: urlparse(x).scheme)

    
def feature_generator(inputdataframe):
    outputdataframe=inputdataframe[['url','status']].copy()
    parseurl(inputdataframe)
    url_features.character_count_url(inputdataframe,outputdataframe)
    url_features.character_count_hostname(inputdataframe,outputdataframe)
    url_features.character_count_query(inputdataframe,outputdataframe)
    url_features.character_count_filename(inputdataframe,outputdataframe)
    return(outputdataframe)



