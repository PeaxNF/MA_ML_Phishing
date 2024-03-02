import re
import tldextract
from sklearn.feature_extraction.text import TfidfVectorizer
from subprocess import check_output
import pandas as pd
import time
from bs4 import BeautifulSoup
#import helper_functions
import yagooglesearch
import numpy as np
import logging
import os

def get_html(htmlfile):
    with open('../../../dataset/htmldataset/' + htmlfile) as fp:
        soup = BeautifulSoup(fp, 'html.parser',multi_valued_attributes=None)
        return soup  



def get_vpn_list(style_string):
    pattern=re.compile(r'\n\t\t([^\s]*)')
    return pattern.findall(style_string)


def cantina(htmlobject,domaintld, num_words=5,num_results=30, add_domain=1):
    tfidfvectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english')
    try:
        tfidf = tfidfvectorizer.fit_transform([htmlobject.get_text()]).toarray()
        index_top_words = tfidf.max(axis=0).argsort()[-num_words:]
        tfidf_words = tfidfvectorizer.get_feature_names_out()
        search_words = tfidf_words[index_top_words]
        if add_domain == 1:
            search_words = np.append(search_words, domaintld)
        googlesearch = ' '.join(search_words)

        client = yagooglesearch.SearchClient(
            googlesearch,
            tbs="li:1",
            max_search_result_urls_to_return=num_results,

             verbosity=4,
            yagooglesearch_manages_http_429s=False,
            verbose_output=False,  
        )
        client.assign_random_user_agent()
        urls = client.search()

        for url in urls:
            hyperlink=tldextract.extract(url).domain+'.'+ tldextract.extract(url).suffix
            if url == 'HTTP_429_DETECTED':
                return 2
            if hyperlink == domaintld:
                print("Searchdomain: "+hyperlink + "Urldomain: "+domaintld)
                logging.info("Searchdomain: "+hyperlink + "Urldomain: "+domaintld)
                return 1
        return 0
    except Exception as error:
        print(error)
        return 0
    

def googlesearchfunc(df,startindex,stopindex,searchpervpn=10,timeout=10,num_words=5,num_results=30, sleep_interval=5, add_domain=1, vpnoffset=0):
    searchcount=0
    vpnlist=get_vpn_list(check_output('mullvad relay list', shell=True).decode('utf-8'))
    vpncount=vpnoffset
    timeoutcount=0
    googlesearch = pd.DataFrame()
    print(check_output('mullvad relay set location ' + vpnlist[vpncount], shell=True).decode('utf-8'))
    logging.info("mullvad relay set location "+vpnlist[vpncount])
    del vpnlist[27:45]
    print(len(vpnlist))
    print(check_output('mullvad connect',shell=True).decode('utf-8'))
    for i in range(startindex,stopindex,1):
        time.sleep(sleep_interval)
            #if lastvpn == vpncount:
            #check_output("mullvad relay set location se mma"+vpnlist[vpncount])
        print(df.loc[i]['url'])
        logging.info(df.loc[i]['url'])
        logging.info("ROW "+str(i))
        print("\nROW "+str(i))
        result=cantina(get_html(df.loc[i]['website']),df.loc[i]['domaintld'], num_words, num_results, add_domain)
        while (result == 2) :
        #if result == 2:    
            vpncount=vpncount+1
            #print('mullvad relay set location ' + vpnlist[vpncount])
            print(check_output('mullvad relay set location ' + vpnlist[vpncount], shell=True).decode('utf-8'))
            logging.info("mullvad relay set location "+vpnlist[vpncount])
            time.sleep(2)
            while('Connected' not in check_output('mullvad status', shell=True).decode('utf-8')):
                    time.sleep(1)
                    timeoutcount=timeoutcount+1
                    print("Not Connected retrying " + str(timeoutcount))
                    if(timeoutcount==timeout):
                        vpncount=vpncount+1
                        timeoutcount=0
                        print(check_output('mullvad relay set location ' + vpnlist[vpncount], shell=True).decode('utf-8'))
                        logging.info("mullvad relay set location "+vpnlist[vpncount])
                        time.sleep(2)
            timeoutcount=timeoutcount+1
            result=cantina(get_html(df.loc[i]['website']),df.loc[i]['domaintld'], num_words, num_results, add_domain)
        googlesearch.at[i, 'cantina']=result
        print("\nVPNCOUNT "+str(vpncount)+ " List: " +vpnlist[vpncount])
        logging.info("VPNCOUNT "+str(vpncount)+ " List: " +vpnlist[vpncount])
        logging.info("SEARCHCOUNTVPN "+str(searchcount))
        print("\nSEARCHCOUNTVPN "+str(searchcount))
        if searchcount < searchpervpn-1:
            searchcount=searchcount+1
        else:
            searchcount=0
            if vpncount < len(vpnlist)-1:
                vpncount=vpncount+1
                print(check_output('mullvad relay set location ' + vpnlist[vpncount], shell=True).decode('utf-8'))
                logging.info("mullvad relay set location "+vpnlist[vpncount])
                time.sleep(2)
                while('Connected' not in check_output('mullvad status', shell=True).decode('utf-8')):
                    time.sleep(2)
                    timeoutcount=timeoutcount+1
                    print("Not Connected retrying " + str(timeoutcount))
                    logging.info("Not Connected retrying " + str(timeoutcount))
                    if(timeoutcount==timeout):
                        vpncount=vpncount+1
                        timeoutcount=0
                        print(check_output('mullvad relay set location ' + vpnlist[vpncount], shell=True).decode('utf-8'))
                        logging.info("mullvad relay set location "+vpnlist[vpncount])
                        time.sleep(2)
                timeoutcount=0


            else:
                vpncount=0
                print(check_output('mullvad relay set location ' + vpnlist[vpncount], shell=True).decode('utf-8'))
                logging.info("mullvad relay set location "+vpnlist[vpncount])
                time.sleep(2)
                while('Connected' not in check_output('mullvad status', shell=True).decode('utf-8')):
                    time.sleep(2)
                    timeoutcount=timeoutcount+1
                    print("Not Connected retrying " + str(timeoutcount))
                    logging.info("Not Connected retrying " + str(timeoutcount))
                    if(timeoutcount==timeout):
                        vpncount=vpncount+1
                        timeoutcount=0
                        print(check_output('mullvad relay set location ' + vpnlist[vpncount], shell=True).decode('utf-8'))
                        logging.info("mullvad relay set location "+vpnlist[vpncount])
                        time.sleep(2)
                timeoutcount=0
    time.sleep(5)
    print("mullvad disconnect")
    logging.info("mullvad disconnect")
    print(check_output('mullvad disconnect', shell=True).decode('utf-8'))
    return googlesearch


def save_cantina(df,outputfoldercsv,outputfolderlog,filename,startpoint=0):
    logging.basicConfig(filename=outputfolderlog + '/cantina.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
    startpoint=int(startpoint/250)
    for i in range(startpoint,40):
        logging.info('start'+str(i*250)+ 'end' + str((i+1)*250))
        google_result=googlesearchfunc(df,i*250,(i+1)*250)
        google_result.to_csv(outputfoldercsv + '/' + filename + '_' + str(i*250)+ '_' + str(((i+1)*250)-1) + '_index_t.csv',index=True)
        logging.info(outputfoldercsv + '/' + filename + '_' + str(i*250) + '_' + str(((i+1)*250)-1) + '_index_t.csv')
        #google_result.to_csv('./cantina/phishing/automated/index/cantina_phishing_'+ str(i*250)+'_'+str(((i+1)*250)-1)+'_index_t.csv',index=True)
        #logging.info('./cantina/phishing/automated/index/cantina_phishing_'+ str(i*250)+'_'+str(((i+1)*250)-1)+'_index_t.csv')
        # google_result.to_csv('./cantina/phishing/automated/no_index/cantina_phishing_'+ str(i*250)+'_'+str(((i+1)*250)-1)+'.csv',index=False)
        # logging.info('./cantina/phishing/automated/no_index/cantina_phishing_'+ str(i*250)+'_'+str(((i+1)*250)-1)+'_index_t.csv')

def combine_parts(partspath,outputpath):
    list_parts=os.listdir(partspath)
    list_parts.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    df=pd.read_csv(partspath + '/cantina_phishing_0_249_index_t.csv')
    for i in range (1,len(list_parts)):
        temp=pd.read_csv(partspath + '/' + list_parts[i])
        df=pd.concat([df,temp],axis=0)
    df.set_index('Unnamed: 0',inplace=True)
    df.index.names = ['Index']
    df.to_csv(outputpath + '/cantina_phishing.csv',index=False)