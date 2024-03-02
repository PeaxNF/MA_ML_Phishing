from urllib.parse import urlparse
from ipaddress import ip_address, IPv4Address, IPv6Address
import os
import tldextract
from datetime import datetime
import pandas as pd


def is_ip(input):
        try:
            decimal_input = int(input, 16)
            test = ".".join(map(str, [decimal_input >> 24, (decimal_input >> 16) & 255, (decimal_input >> 8) & 255, decimal_input & 255]))
            #print(ip_address)
            if type(ip_address(test)) is IPv4Address or IPv6Address:
                return 1
        except:
            try:
                decimal_input = int(input, 8)
                test = ".".join(map(str, [decimal_input >> 24, (decimal_input >> 16) & 255, (decimal_input >> 8) & 255, decimal_input & 255]))
                #print(ip_address)
                if type(ip_address(test)) is IPv4Address or IPv6Address:
                    return 1
            except:
                try:
                    decimal_input = int(input)
                    test = ".".join(map(str, [decimal_input >> 24, (decimal_input >> 16) & 255, (decimal_input >> 8) & 255, decimal_input & 255]))
                    #print(ip_address)
                    if type(ip_address(test)) is IPv4Address or IPv6Address:
                        return 1
                except:
                    try:
                        if type(ip_address(input)) is IPv4Address or IPv6Address:
                            return 1
                    except:
                        return 0


def protocolsecure(protocol):
    if protocol == 'https':
        return 1
    else:
        return 0
    

def punycode(hostname):
    puny=hostname.encode('idna').decode('utf-8')
    return int(puny.startswith('xn--'))
     

def parseurl(dataframeurl):
  dataframeurl['protocol']=dataframeurl['url'].apply(lambda x: urlparse(x).scheme)
  dataframeurl['subdomain']=dataframeurl['url'].apply(lambda x: tldextract.extract(x).subdomain)
  dataframeurl['domain']=dataframeurl['url'].apply(lambda x: tldextract.extract(x).domain)
  dataframeurl['tld']=dataframeurl['url'].apply(lambda x: tldextract.extract(x).suffix)
  dataframeurl['hostname']= dataframeurl['url'].apply(lambda x: urlparse(x).hostname)
  dataframeurl['path']=dataframeurl['url'].apply(lambda x: urlparse(x).path)
  dataframeurl['params']=dataframeurl['url'].apply(lambda x: urlparse(x).params)
  dataframeurl['query']=dataframeurl['url'].apply(lambda x: urlparse(x).query)
  dataframeurl['fragment']=dataframeurl['url'].apply(lambda x: urlparse(x).fragment)
  dataframeurl['filename']=dataframeurl['path'].apply(lambda x: os.path.basename(x))



def character_count_url(inputdataframe,outputdataframe):
    outputdataframe['https_true']=inputdataframe['protocol'].apply(lambda x: protocolsecure(x))
    outputdataframe['url_digits_count']=inputdataframe['url'].apply(lambda x: sum(c.isdigit() for c in x))
    outputdataframe['url_lenght']=inputdataframe['url'].str.len()
    outputdataframe['url_dot_count']=inputdataframe['url'].str.count('\.')
    outputdataframe['url_underline_count']=inputdataframe['url'].str.count('\_')
    outputdataframe['url_hyphen_count']=inputdataframe['url'].str.count('\-')
    outputdataframe['url_slash_count']=inputdataframe['url'].str.count('\/')
    outputdataframe['url_questionmark_count']=inputdataframe['url'].str.count('\?')
    outputdataframe['url_equal_count']=inputdataframe['url'].str.count('\=')
    outputdataframe['url_at_count']=inputdataframe['url'].str.count('\@')
    outputdataframe['url_and_count']=inputdataframe['url'].str.count('\&')
    outputdataframe['url_exclamation_count']=inputdataframe['url'].str.count('\!')
    outputdataframe['url_space_count']=inputdataframe['url'].str.count(' ')
    outputdataframe['url_space_encoded_count']=inputdataframe['url'].str.count('\%20')
    outputdataframe['url_comma_count']=inputdataframe['url'].str.count('\,')
    outputdataframe['url_tilde_count']=inputdataframe['url'].str.count('\~')
    outputdataframe['url_plus_count']=inputdataframe['url'].str.count('\+')
    outputdataframe['url_asterisk_count']=inputdataframe['url'].str.count('\*')
    outputdataframe['url_hashtag_count']=inputdataframe['url'].str.count('\#')
    outputdataframe['url_dollar_count']=inputdataframe['url'].str.count('\$')
    outputdataframe['url_percent_count']=inputdataframe['url'].str.count('\%')
    outputdataframe['url_www_count']=inputdataframe['url'].str.count('www')
    outputdataframe['url_doubleslash_count']=inputdataframe['url'].str.count('.//')
    outputdataframe['url_http_count']=inputdataframe['url'].str.count('http')
    outputdataframe['url_https_count']=inputdataframe['url'].str.count('https')
    return outputdataframe

def character_count_hostname(inputdataframe,outputdataframe):
    outputdataframe['hostname_lenght']=inputdataframe['hostname'].str.len()
    outputdataframe['hostname_dot_count']=inputdataframe['hostname'].str.count('\.')
    outputdataframe['hostname_underline_count']=inputdataframe['hostname'].str.count('\_')
    outputdataframe['hostname_hyphen_count']=inputdataframe['hostname'].str.count('\-')
    outputdataframe['hostname_slash_count']=inputdataframe['hostname'].str.count('\/')
    outputdataframe['hostname_questionmark_count']=inputdataframe['hostname'].str.count('\?')
    outputdataframe['hostname_equal_count']=inputdataframe['hostname'].str.count('\=')
    outputdataframe['hostname_at_count']=inputdataframe['hostname'].str.count('\@')
    outputdataframe['hostname_and_count']=inputdataframe['hostname'].str.count('\&')
    outputdataframe['hostname_exclamation_count']=inputdataframe['hostname'].str.count('\!')
    outputdataframe['hostname_space_count']=inputdataframe['hostname'].str.count(' ')
    outputdataframe['hostname_space_encoded_count']=inputdataframe['hostname'].str.count('\%20')
    outputdataframe['hostname_comma_count']=inputdataframe['hostname'].str.count('\,')
    outputdataframe['hostname_tilde_count']=inputdataframe['hostname'].str.count('\~')
    outputdataframe['hostname_plus_count']=inputdataframe['hostname'].str.count('\+')
    outputdataframe['hostname_asterisk_count']=inputdataframe['hostname'].str.count('\*')
    outputdataframe['hostname_hashtag_count']=inputdataframe['hostname'].str.count('\#')
    outputdataframe['hostname_dollar_count']=inputdataframe['hostname'].str.count('\$')
    outputdataframe['hostname_percent_count']=inputdataframe['hostname'].str.count('\%')
    outputdataframe['hostname_lenght']=inputdataframe['hostname'].str.len()
    outputdataframe['hostname_isip']=inputdataframe['hostname'].apply(lambda x: is_ip(x))
    outputdataframe['hostname_digits_count']=inputdataframe['hostname'].apply(lambda x: sum(c.isdigit() for c in x))
    outputdataframe['hostname_punycode']=inputdataframe['hostname'].apply(lambda x: punycode(x))
    return outputdataframe

def character_count_query(inputdataframe,outputdataframe):
    outputdataframe['query_lenght']=inputdataframe['query'].str.len()
    outputdataframe['query_dot_count']=inputdataframe['query'].str.count('\.')
    outputdataframe['query_underline_count']=inputdataframe['query'].str.count('\_')
    outputdataframe['query_hyphen_count']=inputdataframe['query'].str.count('\-')
    outputdataframe['query_slash_count']=inputdataframe['query'].str.count('\/')
    outputdataframe['query_questionmark_count']=inputdataframe['query'].str.count('\?')
    outputdataframe['query_equal_count']=inputdataframe['query'].str.count('\=')
    outputdataframe['query_at_count']=inputdataframe['query'].str.count('\@')
    outputdataframe['query_and_count']=inputdataframe['query'].str.count('\&')
    outputdataframe['query_exclamation_count']=inputdataframe['query'].str.count('\!')
    outputdataframe['query_space_count']=inputdataframe['query'].str.count(' ')
    outputdataframe['query_space_encoded_count']=inputdataframe['query'].str.count('\%20')
    outputdataframe['query_comma_count']=inputdataframe['query'].str.count('\,')
    outputdataframe['query_tilde_count']=inputdataframe['query'].str.count('\~')
    outputdataframe['query_plus_count']=inputdataframe['query'].str.count('\+')
    outputdataframe['query_asterisk_count']=inputdataframe['query'].str.count('\*')
    outputdataframe['query_hashtag_count']=inputdataframe['query'].str.count('\#')
    outputdataframe['query_dollar_count']=inputdataframe['query'].str.count('\$')
    outputdataframe['query_percent_count']=inputdataframe['query'].str.count('\%')
    return outputdataframe

def character_count_filename(inputdataframe,outputdataframe):
    outputdataframe['file_lenght']=inputdataframe['filename'].str.len()
    outputdataframe['file_dot_count']=inputdataframe['filename'].str.count('\.')
    outputdataframe['file_underline_count']=inputdataframe['filename'].str.count('\_')
    outputdataframe['file_hyphen_count']=inputdataframe['filename'].str.count('\-')
    outputdataframe['file_slash_count']=inputdataframe['filename'].str.count('\/')
    outputdataframe['file_questionmark_count']=inputdataframe['filename'].str.count('\?')
    outputdataframe['file_equal_count']=inputdataframe['filename'].str.count('\=')
    outputdataframe['file_at_count']=inputdataframe['filename'].str.count('\@')
    outputdataframe['file_and_count']=inputdataframe['filename'].str.count('\&')
    outputdataframe['file_exclamation_count']=inputdataframe['filename'].str.count('\!')
    outputdataframe['file_space_count']=inputdataframe['filename'].str.count(' ')
    outputdataframe['file_space_encoded_count']=inputdataframe['filename'].str.count('\%20')
    outputdataframe['file_comma_count']=inputdataframe['filename'].str.count('\,')
    outputdataframe['file_tilde_count']=inputdataframe['filename'].str.count('\~')
    outputdataframe['file_plus_count']=inputdataframe['filename'].str.count('\+')
    outputdataframe['file_asterisk_count']=inputdataframe['filename'].str.count('\*')
    outputdataframe['file_hashtag_count']=inputdataframe['filename'].str.count('\#')
    outputdataframe['file_dollar_count']=inputdataframe['filename'].str.count('\$')
    outputdataframe['file_percent_count']=inputdataframe['filename'].str.count('\%')
    return outputdataframe
    
def feature_generator(inputdataframe):
    outputdataframe=inputdataframe[['url','phishing']].copy()
    outputdataframe=character_count_url(inputdataframe,outputdataframe)
    outputdataframe=character_count_hostname(inputdataframe,outputdataframe)
    outputdataframe=character_count_query(inputdataframe,outputdataframe)
    outputdataframe=character_count_filename(inputdataframe,outputdataframe)
    return(outputdataframe)