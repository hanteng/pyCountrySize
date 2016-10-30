# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
datasource_sn=1

import configparser
Config = configparser.ConfigParser()
Config.read("config.ini")

dir_source = Config.get("Directory", 'source')
dir_inprocess =  Config.get("Directory",'inprocess')
dir_outcome = Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')

#file_name defined in config.ini
fn_input=Config.get("datasource{0}".format(datasource_sn),'filename')

import os.path

import pandas as pd
## Loading the XLS source file
df = pd.io.parsers.read_table(os.path.join(dir_source,fn_input), thousands=',' , na_values=["n/a", "--"], encoding="cp1252")

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
df[['WEO']]=df[['WEO']].astype(int)
df[['ISO']]=df[['ISO']].astype(str)
df[['Subject']]=df[['Subject']].astype(str)
df[['Country_Notes']]=df[['Country_Notes']].astype(str)
df[['Estimates_Start_After']]=df[['Estimates_Start_After']].fillna(-1)
df[['Estimates_Start_After']]=df[['Estimates_Start_After']].astype(int)

#df.convert_objects(convert_numeric=True)

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

## Change column names that look like integer, integers
def integerization(x):
    try:
        return int(x)
    except:
        return x

df.columns=[integerization(x) for x in list(df.columns)]

df.to_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))

##>>> df.head()
##               WEO      Country                       Subject_Descriptor  \
##ISO Subject                                                                
##AFG NGDP_R     512  Afghanistan  Gross domestic product, constant prices   
##    NGDP_RPCH  512  Afghanistan  Gross domestic product, constant prices   
##    NGDP       512  Afghanistan   Gross domestic product, current prices   
##    NGDPD      512  Afghanistan   Gross domestic product, current prices   
##    NGDP_D     512  Afghanistan         Gross domestic product, deflator   
##
##                                                   Subject_Notes  \
##ISO Subject                                                        
##AFG NGDP_R     Expressed in billions of national currency uni...   
##    NGDP_RPCH  Annual percentages of constant price GDP are y...   
##    NGDP       Expressed in billions of national currency uni...   
##    NGDPD      Values are based upon GDP in national currency...   
##    NGDP_D     The GDP deflator is derived by dividing curren...   
##
##                           Units     Scale  \
##ISO Subject                                  
##AFG NGDP_R     National currency  Billions   
##    NGDP_RPCH     Percent change       NaN   
##    NGDP       National currency  Billions   
##    NGDPD           U.S. dollars  Billions   
##    NGDP_D                 Index       NaN   
##
##                                                   Country_Notes  1980  1981  \
##ISO Subject                                                                    
##AFG NGDP_R     Source: National Statistical Office Latest act...   NaN   NaN   
##    NGDP_RPCH  See notes for:  Gross domestic product, consta...   NaN   NaN   
##    NGDP       Source: National Statistical Office Latest act...   NaN   NaN   
##    NGDPD      See notes for:  Gross domestic product, curren...   NaN   NaN   
##    NGDP_D     See notes for:  Gross domestic product, consta...   NaN   NaN   
##
##               1982          ...               2011      2012      2013  \
##ISO Subject                  ...                                          
##AFG NGDP_R      NaN          ...            386.368   440.336   456.172   
##    NGDP_RPCH   NaN          ...              6.479    13.968     3.596   
##    NGDP        NaN          ...            836.222  1033.590  1148.110   
##    NGDPD       NaN          ...             17.890    20.296    20.735   
##    NGDP_D      NaN          ...            216.432   234.728   251.684   
##
##                   2014      2015      2016      2017      2018      2019  \
##ISO Subject                                                                 
##AFG NGDP_R      470.947   492.083   516.838   542.993   571.601   603.538   
##    NGDP_RPCH     3.239     4.488     5.031     5.060     5.269     5.587   
##    NGDP       1248.660  1378.500  1526.440  1682.610  1858.130  2057.320   
##    NGDPD        21.706    23.227    24.787    26.380    28.117    30.028   
##    NGDP_D      265.139   280.136   295.342   309.878   325.075   340.876  
