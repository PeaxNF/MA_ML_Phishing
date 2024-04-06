from urllib.parse import urlparse
from ipaddress import ip_address, IPv4Address, IPv6Address
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
#       # df['scheme']= urlparse(i).scheme
  dataframeurl['hostname']= dataframeurl['url'].apply(lambda x: urlparse(x).hostname)
  dataframeurl['path']=dataframeurl['url'].apply(lambda x: urlparse(x).path)
  dataframeurl['params']=dataframeurl['url'].apply(lambda x: urlparse(x).params)
  dataframeurl['query']=dataframeurl['url'].apply(lambda x: urlparse(x).query)
  dataframeurl['fragment']=dataframeurl['url'].apply(lambda x: urlparse(x).fragment)
  dataframeurl['filename']=dataframeurl['path'].apply(lambda x: os.path.basename(x))
  #dataframeurl['whoisobject']=dataframeurl['hostname'].apply(lambda x: checkdomain(x))

#def regular_expression_url(dataframeurl):


def parseurlstring(seriesurl):
  seriesurl['protocol']=seriesurl.apply(lambda x: urlparse(x).scheme)
#       # df['scheme']= urlparse(i).scheme
  #seriesurl['hostname']= seriesurl.apply(lambda x: urlparse(x).hostname)
  #seriesurl['path']=seriesurl.apply(lambda x: urlparse(x).path)
  #seriesurl['params']=seriesurl.apply(lambda x: urlparse(x).params)
  #seriesurl['query']=seriesurl.apply(lambda x: urlparse(x).query)
  #seriesurl['fragment']=seriesurl.apply(lambda x: urlparse(x).fragment)
  #seriesurl['filename']=seriesurl['path'].apply(lambda x: os.path.basename(x))

    
def feature_generator(inputdataframe):
    #outputdataframe=inputdataframe[['url','phishing']].copy()
    outputdataframe=inputdataframe[['url','status']].copy()
    parseurl(inputdataframe)
    url_features.character_count_url(inputdataframe,outputdataframe)
    url_features.character_count_hostname(inputdataframe,outputdataframe)
    url_features.character_count_query(inputdataframe,outputdataframe)
    #outputdataframe=character_count_path(inputdataframe,outputdataframe)
    url_features.character_count_filename(inputdataframe,outputdataframe)

    #content_features.html_features(inputdataframe,outputdataframe)
    return(outputdataframe)

# def feature_generator_c(inputdataframe):
#   outputdataframe=inputdataframe[['url','status']].copy()
#   outputdataframe=url_features.categorical_features(inputdataframe,outputdataframe)
#   return(outputdataframe)

#def test_generator(inputdataframe):
    #outputdataframe=inputdataframe['url'].copy()
    #outputdataframe=outputdataframe.to_frame()
    #outputdataframe=character_count_url(inputdataframe,outputdataframe)
    #outputdataframe=character_count_hostname(inputdataframe,outputdataframe)
    #outputdataframe=character_count_path(inputdataframe,outputdataframe)
    #outputdataframe=character_count_filename(inputdataframe,outputdataframe)
    #return(outputdataframe)


