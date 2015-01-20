# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
datasource_sn=1

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

dir_source = Config.get("Directory", 'source')
dir_inprocess =  Config.get("Directory",'inprocess')
dir_outcome = Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')

#file_name="WEOOct2014all.xls"
fn_input=Config.get("datasource{0}".format(datasource_sn),'filename')

import os.path

import pandas as pd
## Loading the XLS source file
df = pd.io.parsers.read_table(os.path.join(dir_source,fn_input), thousands=',' , na_values=["n/a", "--"])

## REMOVing the last two lines from the data source:
df=df.iloc[:-2]

## Simplifyig the column names
def name_rename(name):
    dict_trans = {'WEO Country Code':               'WEO',
                  'WEO Subject Code':               'Subject',
                  'Country/Series-specific Notes':  'Country_Notes'}
    return dict_trans.get(name, name)   

col_names = [name_rename(x) for x in df.columns]
df.columns=col_names
df.rename(columns=lambda x: x.replace(" ","_"), inplace=True)

## CHANGing data types
df[['WEO']]=df[['WEO']].astype(float)
df[['ISO']]=df[['ISO']].astype(str)
df[['Subject']]=df[['Subject']].astype(str)
df[['Country_Notes']]=df[['Country_Notes']].astype(str)
df.convert_objects(convert_numeric=True)

## Adding index points to the dataframe    'ISO', 'Subject'
df.set_index(['ISO', 'Subject'], inplace=True)

## > Select a country (e.g. AFG) and a Subject (e.g. PPPGDP) --> time series data
#print df.query('ISO == "AFG" & Subject=="PPPGDP"')
## >> Pick a Year further
#print df.query('ISO == "AFG" & Subject=="PPPGDP"')['2014']
##ISO  Subject
##AFG  PPPGDP     61.689
##Name: 2014, dtype: float64

## > Select a year (e.g. 2014) and a Subject (e.g. PPPGDP) --> cross-country (cross-sectional) data
#test=df.query('Subject=="PPPGDP"')['2014']
#print test[0:3]

## > Select a year (e.g. 2013) and a country (e.g. TWN) --> all subject data about a country in a given year
#test=df.query('ISO == "TWN"')['2013']
#print test[0:3]

df.to_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))
