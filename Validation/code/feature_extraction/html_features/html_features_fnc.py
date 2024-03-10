import tldextract
from datetime import datetime
import re
from bs4 import BeautifulSoup
import pandas as pd

 
def import_re(re_string):
    pattern=re.compile(r'@import\s+(?:url)?\(?["|\']([^"|\']*)["|\']\)?')
    return pattern.findall(re_string)


def disable_contextmenu(content):
    content_str=str(content)
    pattern=re.compile(r'contextmenu|event.button\s*?==\s*?2')
    if pattern.findall(content_str):
        return 1
    else:
        return 0
    
  
def get_html(htmlfile):
    with open('../../../dataset/htmlfiles/' + htmlfile) as fp:
        soup = BeautifulSoup(fp, 'html.parser',multi_valued_attributes=None)
        return soup    
    


    


def html_domain_in_title(htmlobject,domaintld):
  print(domaintld)  
  print(htmlobject.title)
  if htmlobject.title is not None:  
      if htmlobject.title.string is not None:
          if domaintld in htmlobject.title.string:
            return 1
  return 0



def hyperlinkscount(domaintld,htmlobject):
  
  src_elements=['embed','iframe','input','script','source','track']
  src_media_elements=['audio','img','video']
  count_int=0
  count_ext=0
  count_null=0
  count_total=0
  a_total=0
  a_int=0
  a_ext=0
  a_null=0
  src_other_total=0
  src_other_int=0
  src_other_ext=0
  src_other_null=0
  media_total=0
  media_int=0
  media_ext=0
  media_null=0
  link_total=0
  link_int=0
  link_ext=0
  link_null=0

    
    
  a_total,a_int,a_ext,a_null=html_int_ext_null_link_count_single(domaintld,htmlobject,'a','href')
  print(domaintld)
  count_total=count_total+a_total
  count_int=count_int+a_int
  count_ext=count_ext+a_ext
  count_null=count_null+a_null
  if a_total != 0:
    ratio_a_int=a_int/a_total
    ratio_a_ext=a_ext/a_total
    ratio_a_null=a_null/a_total
  else:
    ratio_a_int=0
    ratio_a_ext=0
    ratio_a_null=0


  link_total,link_int,link_ext,temp_null=html_int_ext_null_link_count_single(domaintld,htmlobject,'link','href')
  count_total=count_total+link_total
  count_int=count_int+link_int
  count_ext=count_ext+link_ext
  count_null=count_null+link_null
  if link_total != 0:
    ratio_link_int=link_int/link_total
    ratio_link_ext=link_ext/link_total
    ratio_link_null=link_null/link_total
  else:
    ratio_link_int=0
    ratio_link_ext=0
    ratio_link_null=0


  for ele_src in src_elements:
    temp_total,temp_int,temp_ext,temp_null=html_int_ext_null_link_count_single(domaintld,htmlobject,ele_src,'src')
    src_other_total=temp_total+src_other_total
    src_other_int=temp_int+src_other_int
    src_other_ext=temp_ext+src_other_ext
    src_other_null=temp_null+src_other_null
    count_total=count_total+temp_total
    count_int=count_int+temp_int
    count_ext=count_ext+temp_ext
    count_null=count_null+temp_null
  if src_other_total != 0:
    ratio_src_other_int=src_other_int/src_other_total
    ratio_src_other_ext=src_other_ext/src_other_total
    ratio_src_other_null=src_other_null/src_other_total
  else:
    ratio_src_other_int=0
    ratio_src_other_ext=0
    ratio_src_other_null=0
    

  for ele_src in src_media_elements:
    temp_total,temp_int,temp_ext,temp_null=html_int_ext_null_link_count_single(domaintld,htmlobject,ele_src,'src')
    media_total=temp_total+media_total
    media_int=temp_int+media_int
    media_ext=temp_ext+media_ext
    media_null=temp_null+media_null
    count_total=count_total+temp_total
    count_int=count_int+temp_int
    count_ext=count_ext+temp_ext
    count_null=count_null+temp_null
  if media_total != 0:
    ratio_media_int=media_int/media_total
    ratio_media_ext=media_ext/media_total
    ratio_media_null=media_null/media_total
  else:
    ratio_media_int=0
    ratio_media_ext=0
    ratio_media_null=0
    

  form_total,form_int,form_ext,form_null=html_int_ext_null_link_count_single(domaintld,htmlobject,'form','action')
  if form_null >0 or form_ext >0:
    external_null_form=1
  else:
    external_null_form=0
  count_total=count_total+form_total
  count_int=count_int+form_int
  count_ext=count_ext+form_ext
  count_null=count_null+form_null
  if form_total != 0:
    ratio_form_int=form_int/form_total
    ratio_form_ext=form_ext/form_total
    ratio_form_null=form_null/form_total
  else:
    ratio_form_int=0
    ratio_form_ext=0
    ratio_form_null=0
    

  fav_total,fav_int,fav_ext,fav_null=favicon_ft(domaintld,htmlobject)
  if fav_ext > 0:
    external_favicon=1
  else:
    external_favicon=0
  count_total=count_total+fav_total
  count_int=count_int+fav_int
  count_ext=count_ext+fav_ext
  count_null=count_null+fav_null
  if fav_total != 0:
    ratio_fav_int=fav_int/fav_total
    ratio_fav_ext=fav_ext/fav_total
    ratio_fav_null=fav_null/fav_total
  else:
    ratio_fav_int=0
    ratio_fav_ext=0
    ratio_fav_null=0
    

  css_total,css_int,css_ext,css_null=html_int_ext_null_link_count_css(domaintld,htmlobject)
  if css_ext > 0:
    external_css=1
  else:
    external_css=0
  count_total=count_total+css_total
  count_int=count_int+css_int
  count_ext=count_ext+css_ext
  count_null=count_null+css_null
  if css_total != 0:
    ratio_css_int=css_int/css_total
    ratio_css_ext=css_ext/css_total
    ratio_css_null=css_null/css_total
  else:
    ratio_css_int=0
    ratio_css_ext=0
    ratio_css_null=0


  if count_total != 0:
    ratio_int=count_int/count_total
    ratio_ext=count_ext/count_total
    ratio_null=count_null/count_total
  else:
    ratio_int=0
    ratio_ext=0
    ratio_null=0

  return count_total, ratio_int, ratio_ext, ratio_null,a_total,ratio_a_int,ratio_a_ext,ratio_a_null,link_total,ratio_link_int,ratio_link_ext,ratio_link_null,src_other_total,ratio_src_other_int,ratio_src_other_ext,ratio_src_other_null,media_total,ratio_media_int,ratio_media_ext,ratio_media_null,form_total,ratio_form_int,ratio_form_ext,ratio_form_null,fav_total,ratio_fav_int,ratio_fav_ext,ratio_fav_null,css_total,ratio_css_int,ratio_css_ext,ratio_css_null, external_css, external_favicon, external_null_form#count_int, count_ext, count_null
 
def html_iframe_invisible(htmlobject):
  style = ['border:none', 'display:none']

  for link in htmlobject.find_all('iframe'):
    if link.get('src'):
      try:
        if tldextract.extract(link.get('src')).domain != 'googletagmanager':
            if link.get('width') and link.get('height'):
              print(link.get('width'))
              print(link.get('height'))
              if 0 <= float(link.get('width').strip('px%')) <=5 and 0 <= float(link.get('height').strip('px%')) <=5:
                  return 1
            if link.get('style'):
              if any(x in link.get('style') for x in style):
                  return 1
            if link.get('frameborder'):
              if str(link.get('frameborder')) == '0' or str(link.get('frameborder')) == 'no':
                return 1
        else:
            if link.get('width') and link.get('height'):
              if 0 <= float(link.get('width').strip('px%')) <=5 and 0 <= float(link.get('height').strip('px%')) <=5:
                  return 1
            if link.get('style'):
              if any(x in link.get('style') for x in style):
                  return 1
            if link.get('frameborder'):
              if str(link.get('frameborder')) == '0' or str(link.get('frameborder')) == 'no':
                return 1
      except:
         return 0      
  return 0


def html_prompt(htmlobject):
  if 'prompt(' in str(htmlobject).lower():
    return 1
  else:
     return 0
  
def html_windows_status(htmlobject):
  if 'window.status' in str(htmlobject).lower():
    return 1
  else:
     return 0
  

def unsafe_anchor(htmlobject):
  unsafe_anchor=['#', 'javascript', 'mailto']
  for link in htmlobject.find_all('a'):
    if link.get('href'):
        if any(x in link.get('href') for x in unsafe_anchor):
          return 1
  return 0
  
  
def html_int_ext_null_link_count_single(domaintld,htmlobject,element,tag):
  if element == 'form':
     nullvalues = ['','#','#!',';','#nothing','#doesnotexist','#null','#void','#whatever','javascript:void(0);','javascript:;','javascript:null','javascript:{}','javascript:void(0)','about:blank']
     print('form')
  else:
    nullvalues = ['','#','#!',';','#nothing','#doesnotexist','#null','#void','#whatever','javascript:void(0);','javascript:;','javascript:null','javascript:{}','javascript:void(0)']
  count_int=0
  count_ext=0
  count_null=0
  for link in htmlobject.find_all(element):
    if link.get(tag) is not None:
      hyperlinktld=tldextract.extract(link.get(tag)).domain+'.'+ tldextract.extract(link.get(tag)).suffix
      if link.get(tag) in nullvalues:
          count_null=count_null+1
      elif domaintld in hyperlinktld or not link.get(tag).startswith(('http','//')):
          count_int=count_int+1
      else:
        count_ext=count_ext+1
  count_total= count_int + count_ext + count_null
  return count_total, count_int, count_ext, count_null 


def html_int_ext_null_link_count_css(domaintld,htmlobject):
    nullvalues = ['','#','#!',';','#nothing','#doesnotexist','#null','#void','#whatever','javascript:void(0);','javascript:;','javascript:null','javascript:{}','javascript:void(0)']
    count_int=0
    count_ext=0
    count_null=0
    for link in htmlobject.find_all('link'):
        if link.get('rel'):
          if link.get('rel') == 'stylesheet' or link.get('type') == 'text/css':
              if link.get('href') is not None:
                  hyperlinktld=tldextract.extract(link.get('href')).domain+'.'+ tldextract.extract(link.get('href')).suffix
                  if link.get('href') in nullvalues:
                    count_null=count_null+1
                  elif domaintld in hyperlinktld or not link.get('href').startswith(('http','//')):
                    count_int=count_int+1
                  else:
                    count_ext=count_ext+1
    for link in htmlobject.find_all('style'):
        import_list=import_re(link.get_text())
        for import_string in import_list:
            if import_string is not None:
                hyperlinktld=tldextract.extract(import_string).domain+'.'+ tldextract.extract(import_string).suffix
                if import_string in nullvalues:
                    count_null=count_null+1
                elif domaintld in hyperlinktld or not import_string.startswith(('http','//')):
                    count_int=count_int+1
                else:
                    count_ext=count_ext+1
    count_total= count_int + count_ext + count_null
    return count_total, count_int, count_ext, count_null

def favicon_ft(domaintld,htmlobject):
    nullvalues = ['','#','#!',';','#nothing','#doesnotexist','#null','#void','#whatever','javascript:void(0);','javascript:;','javascript:null','javascript:{}','javascript:void(0)']
    count_int=0
    count_ext=0
    count_null=0
    for head in htmlobject.find_all('head'):
        for headlink in head.find_all('link'):
            if headlink.get('rel'):
                if 'icon' in headlink.get('rel'):
                  if headlink.get('href'):
                    hyperlinktld=tldextract.extract(headlink.get('href')).domain+'.'+ tldextract.extract(headlink.get('href')).suffix
                    if headlink.get('href') in nullvalues:
                        count_null=count_null+1
                    elif domaintld in hyperlinktld or not headlink.get('href').startswith(('http','//')):
                        count_int=count_int+1
                    else:
                        count_ext=count_ext+1
    count_total= count_int + count_ext + count_null
    return count_total, count_int, count_ext, count_null


def html_empty_title(htmlobject):

  if htmlobject.title:
    if htmlobject.title.string == "":
      return 1
    else:
      return 0
  else:
     return 1  



def html_form_ext_count_mail(htmlobject):
  mailfunc = ['mail()', 'mailto:']
  for link in htmlobject.find_all('form'):
    if link.get('action'):
      if any(x in link.get('action') for x in mailfunc):
        return 1
  return 0

   

def html_features(inputdataframe):
  outputdataframe = pd.DataFrame()
  outputdataframe[["html_hl_count_total", "html_hl_ratio_int", "html_hl_ratio_ext", "html_hl_ratio_null","html_hl_a_total", "html_hl_ratio_a_int","html_hl_ratio_a_ext","html_hl_ratio_a_null","html_hl_link_total", "html_hl_ratio_link_int", "html_hl_ratio_link_ext","html_hl_ratio_link_null", "html_hl_src_other_total", "html_hl_ratio_src_other_int","html_hl_ratio_src_other_ext","html_hl_ratio_src_other_null", "html_hl_media_total", "html_hl_ratio_media_int","html_hl_ratio_media_ext","html_hl_ratio_media_null","html_hl_form_total", "html_hl_ratio_form_int","html_hl_ratio_form_ext","html_hl_ratio_form_null","html_hl_fav_total", "html_hl_ratio_fav_int","html_hl_ratio_fav_ext","html_hl_ratio_fav_null","html_hl_css_total", "html_hl_ratio_css_int","html_hl_ratio_css_ext","html_hl_ratio_css_null", "html_hl_external_css", "html_hl_external_favicon", "html_hl_external_null_form"]]=inputdataframe.apply(lambda x: hyperlinkscount(x.domaintld,get_html(x.website)), axis='columns', result_type='expand')
  outputdataframe["html_domain_titel"]=inputdataframe.apply(lambda x: html_domain_in_title(get_html(x.website),x.domaintld), axis='columns', result_type='expand')
  outputdataframe["html_windows_status"]=inputdataframe['website'].apply(lambda x: html_windows_status(get_html(x)))
  outputdataframe["html_form_ext_count_mail"]=inputdataframe['website'].apply(lambda x: html_form_ext_count_mail(get_html(x)))
  outputdataframe["html_prompt"]=inputdataframe['website'].apply(lambda x: html_prompt(get_html(x)))
  outputdataframe["html_unsafe_anchor"]=inputdataframe['website'].apply(lambda x: unsafe_anchor(get_html(x)))
  outputdataframe["html_iframe_invisible"]=inputdataframe['website'].apply(lambda x: html_iframe_invisible(get_html(x)))
  outputdataframe["html_empty_title"]=inputdataframe['website'].apply(lambda x: html_empty_title(get_html(x)))
  return outputdataframe

# def html_features(inputdataframe):
#   outputdataframe = pd.DataFrame()
#   outputdataframe[["html_hl_count_total", "html_hl_ratio_int", "html_hl_ratio_ext", "html_hl_ratio_null", "html_hl_media_total", "html_hl_ratio_media_int","html_hl_ratio_media_ext", "html_hl_link_total", "html_hl_ratio_link_int", "html_hl_ratio_link_ext",
#                    "html_hl_external_css", "html_hl_external_favicon", "html_hl_external_null_form"]]=inputdataframe.apply(lambda x: hyperlinkscount(x.domain,savehtml(x.website)), axis='columns', result_type='expand')
#   outputdataframe["html_domain_titel"]=inputdataframe.apply(lambda x: html_domain_in_title(savehtml(x.website),x.domaintld), axis='columns', result_type='expand')
#   outputdataframe["html_windows_status"]=inputdataframe['website'].apply(lambda x: html_windows_status(savehtml(x)))
#   outputdataframe["html_form_ext_count_mail"]=inputdataframe['website'].apply(lambda x: html_form_ext_count_mail(savehtml(x)))
#   outputdataframe["html_prompt"]=inputdataframe['website'].apply(lambda x: html_prompt(savehtml(x)))
#   outputdataframe["html_unsafe_anchor"]=inputdataframe['website'].apply(lambda x: unsafe_anchor(savehtml(x)))
#   outputdataframe["html_iframe_invisible"]=inputdataframe['website'].apply(lambda x: html_iframe_invisible(savehtml(x)))
#   outputdataframe["html_empty_title"]=inputdataframe['website'].apply(lambda x: html_empty_title(savehtml(x)))
#   return outputdataframe