# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")
dir_inprocess =  Config.get("Directory",'inprocess')
fn_suffix = Config.get("Filename",'suffix')

import pandas as pd
import os.path, glob
ldf={}
for datasource_sn in range(1,5):
    fn_input=Config.get("datasource{0}".format(datasource_sn),'filename')
    subject_picked=Config.get("datasource{0}".format(datasource_sn),'subject_picked')
    year_picked=Config.get("datasource{0}".format(datasource_sn),'year_picked')
    print datasource_sn, subject_picked, year_picked, fn_input
    ldf[datasource_sn] = pd.read_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))
##1 LP,PPPGDP 2013 WEOOct2014all.xls
##2 IPop 2013 Individuals_Internet_2000-2013.xls
##3 IH 2012 rawdata_2184.txt
##4 IPv4 2015 CIPB - Allocation of IP addresses by Country.html
    
dict_eq_IMF=ldf[1].reset_index()[['ISO','Country']].drop_duplicates().set_index(['ISO'])['Country']
dict_eq_ITU=ldf[2].reset_index()[['ISO','ISO2']].drop_duplicates().set_index(['ISO'])['ISO2']
dict_eq_CIA=ldf[3].reset_index()[['ISO','ISO2']].drop_duplicates().set_index(['ISO'])['ISO2']
dict_eq_CIPB=ldf[4].reset_index()[['ISO','Country_CIPB']].drop_duplicates().set_index(['ISO'])['Country_CIPB']


df=pd.DataFrame(dict_eq_CIA)
df['ISO2ITU']=[dict_eq_ITU.get(x, None) for x in df.index]
df['name_IMF']=[dict_eq_IMF.get(x, None) for x in df.index]

dir_db = Config.get("Directory",'database')
fn_db = Config.get("output",'filename_mapping')
df.to_pickle(os.path.join(dir_db, fn_db))
