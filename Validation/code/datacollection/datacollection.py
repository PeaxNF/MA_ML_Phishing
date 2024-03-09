import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import pickle
from urllib.parse import urlparse
import tldextract
import time
from comcrawl import IndexClient
import json
from io import BytesIO
import gzip
import random

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
    

def datacollector_legit(linksperdomain,domainlist,numberoflinks):
    website_df=pd.DataFrame()
    if website_df <= numberoflinks:
        client = IndexClient(["2023-50"])
        client.search("reddit.com/r/MachineLearning/*")
        client.download()


### -----------------------
### Searches the Common Crawl Index for a domain.
### -----------------------
#Searches the Common Crawl Index for a domain.
def search_domain(domain):
    record_list = []
    print ("[*] Trying target domain: " +domain)
    #for index in index_list:
    #print ("[*] Trying index" + str(index))
    cc_url  = "http://index.commoncrawl.org/CC-MAIN-2023-50-index?" 
    cc_url += "url="+domain+"&matchType=domain&output=json" #% domain
    response = requests.get(cc_url)
    if response.status_code == 200:
        records = response.content.splitlines()
        for record in records:
            record_list.append(json.loads(record))  
        print ("[*] Added "+str(len(records))+" results.") #% len(records)
    print ("[*] Found a total of "+str(len(record_list))+" hits.") #% len(record_list)
    return record_list

def download_single_result(result): 
    """Downloads HTML for single search result.

    Args:
        result: Common Crawl Index search result from the search function.

    Returns:
        The provided result, extendey by the corresponding HTML String.

    """
    offset, length = int(result["offset"]), int(result["length"])

    offset_end = offset + length - 1

    url = "https://data.commoncrawl.org/" + result["filename"] 
    response = (requests
                .get(
                    url,
                    headers={"Range": f"bytes={offset}-{offset_end}"}
                ))

    zipped_file = BytesIO(response.content)
    unzipped_file = gzip.GzipFile(fileobj=zipped_file)

    raw_data: bytes = unzipped_file.read()
    try:
        data: str = raw_data.decode("utf-8")
    except UnicodeDecodeError:
        print(f"Warning: Could not extract file downloaded from {url}")
        data = ""

    result["html"] = ""

    if len(data) > 0:
        data_parts = data.strip().split("\r\n\r\n", 2)
        result["html"] = data_parts[2] if len(data_parts) == 3 else ""

    return result

def datacollector_legit(linksperdomain,domainlist,numberoflinks,outputpath):
    offset=0
    website_df=pd.DataFrame()
    #client = IndexClient(["2023-50"],verbose=True)
    for i in range(len(domainlist)):
        time.sleep(5)
        print(len(website_df))
        if len(website_df) <= numberoflinks:
            url_list=search_domain(domainlist.loc[i]['Domain']+"/*")
            print(len(url_list))
            if len(url_list) != 0:
                # while len(url_list) == 0:
                #     offset=offset+1
                #     #client = IndexClient(["2023-50"],verbose=True)
                #     url_list=search_domain(domainlist.loc[i+offset]['Domain']+"/*")
                if len(url_list) > 0 and len(url_list) <= linksperdomain -1:
                    for j in range(len(url_list)):
                        print('Loopindex'+str(j))
                        if 'robots.txt' not in url_list[j]["url"]:
                            print(url_list[j]["url"])
                            result=download_single_result(url_list[j])
                            if(len(result["html"])>0):
                                filename=tldextract.extract(result["url"]).domain+'_'+str(round(time.time() * 10**6))+'.html'
                                website_df.at[len(website_df)+1, 'url']=result["url"]
                                website_df.at[len(website_df),'website']=filename
                                with open(outputpath+'/'+filename, 'w') as f:
                                    f.write(result["html"])
                                # website_df.at[len(website_df),'website']=filename
                else:
                    print(str(linksperdomain -1))
                    #for j in range(linksperdomain):
                    for j in range(linksperdomain):
                        print('Loopindex'+str(j))
                        rand_number=random.sample(range(len(url_list)), linksperdomain)
                        
                        # print(str(len(url_list)))
                        # print(str(rand_number[j]))
                        # print(url_list[rand_number[j]]["url"])
                        if 'robots.txt' not in url_list[rand_number[j]]["url"]:
                            print('Randnumber: '+str(rand_number[j]))
                            print('Lenurllist: '+str(len(url_list)))
                            print(url_list[rand_number[j]]["url"])
                            result=download_single_result(url_list[rand_number[j]])
                            #website_df['url']=client.results[i]["url"]
                            #website_df['website']=client.results[i]["html"]
                            if(len(result["html"])>0):
                                filename=tldextract.extract(result["url"]).domain+'_'+str(round(time.time() * 10**6))+'.html'
                                website_df.at[len(website_df)+1, 'url']=result["url"]
                                # with open(outputpath+'/'+filename, 'wb') as f:
                                #     f.write(client.results[j]["html"])
                                website_df.at[len(website_df), 'website']=filename
                                with open(outputpath+'/'+filename, 'w') as f:
                                    f.write(result["html"])
                    
        else:
            break
    return website_df


#random.sample(range(len(test)), 9)