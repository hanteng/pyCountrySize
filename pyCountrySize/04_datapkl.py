# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
datasource_sn=4

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

dir_source = Config.get("Directory", 'source')
dir_inprocess =  Config.get("Directory",'inprocess')
dir_outcome = Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')

fn_input=Config.get("datasource{0}".format(datasource_sn),'filename')
URL_input=Config.get("datasource{0}".format(datasource_sn),'url')

import os.path

import pandas as pd
import numpy as np

from lxml import etree
parser = etree.HTMLParser(encoding='utf-8')

try:
    doc_tree = etree.parse(os.path.join(dir_source,fn_input), parser).getroot()
except:
    print "Probably no existing local files available, now try downloading"
    import requests
    r = requests.get(URL_input)
    if r.status_code <> requests.codes.ok:
        print "Sorry. Retriving file failed from", URL_seed
        exit()
    with open(URL_seed_local, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)
    doc_tree = etree.parse(filename, parser).getroot()


#Constructing dataframe
df=pd.DataFrame()

for i in range(1,3+1):
    
    #Chrome xpath tested: '//*[@id="newsPage"]/div[@class="wide_allocation1"]//text()'
    # 1, 2, 3 for wide_allocationX
    xpath_i='//*[@id="newsPage"]/div[@class="wide_allocation{0}"]//text()'.format(i)
    results=doc_tree.xpath(xpath_i)

    df[results[0]]=results[1:]

## Rename Columns
df.columns_old=df.columns #[u'ISO 3166 Code', u'Country', u'Number of IP addresses']
df.columns=[u'ISO', u'Country_CIPB', u'IPv4']

import locale
locale.setlocale( locale.LC_ALL, 'english_USA' )
df['IPv4']=[locale.atoi(x) for x in df['IPv4']]

##>>> df.head()
##  ISO         Country     IPv4
##0  AF     AFGHANISTAN   161004
##1  AL         ALBANIA   350406
##2  DZ         ALGERIA  3705440
##3  AS  AMERICAN SAMOA     6400
##4  AD         ANDORRA    37680

## Loading the XLS source file: country name mapping data
dir_countryname = Config.get("Directory",'countryname')
file_name_cn= Config.get("countryname",'mapping')  #"country_name.xls"

df_cn = pd.io.excel.read_excel(os.path.join(dir_countryname,file_name_cn), na_values=["NaN"], sheetname='CIPB', keep_default_na=False)
df_cn['ISO2']=df_cn['ISO']
iso_mapping=dict(zip(df_cn['ISO2'],df_cn['ISO_final']))

df['ISO']=[iso_mapping.get(x,"_"+x) for x in df['ISO']]

## Set Index 
df=df.set_index("ISO")               #set index

df.to_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))

##>>> df.head()
##       Country_CIPB     IPv4
##ISO                         
##AFG     AFGHANISTAN   161004
##ALB         ALBANIA   350406
##DZA         ALGERIA  3705440
##ASM  AMERICAN SAMOA     6400
##AND         ANDORRA    37680
