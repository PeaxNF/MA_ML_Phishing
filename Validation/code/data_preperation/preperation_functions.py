
from bs4 import BeautifulSoup
import tldextract
from urllib.parse import urlparse
import os

def check_html(htmlfile):
  try:
    with open('../../dataset/phishing/htmlfiles/' + htmlfile) as fp:
        soup = BeautifulSoup(fp, 'html.parser',multi_valued_attributes=None)
        return 1
  except:
      return 0

def precheck(inputdataframe):
  inputdataframe["check"]=inputdataframe['website'].apply(lambda x: check_html(x))

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




