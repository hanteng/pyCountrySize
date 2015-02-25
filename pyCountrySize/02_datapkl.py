# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
datasource_sn=2

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

dir_source = Config.get("Directory", 'source')
dir_inprocess =  Config.get("Directory",'inprocess')
dir_outcome = Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')

fn_input=Config.get("datasource{0}".format(datasource_sn),'filename')

import os.path

import pandas as pd
## Loading the XLS source file
df = pd.io.excel.read_excel(os.path.join(dir_source,fn_input), na_values=["NaN"], sheetname=0, keep_default_na=False)

## REMOVing unneeded data
df=df.iloc[:,0:14]  #slicing notes columns off the dataframe
colnames=df.iloc[0] 
df.columns=colnames.astype(int) #renaming columns
df=df.iloc[1:,]     #slicing first row off the dataframe
df.index.name="country_name_ITU"    #renaming first column

## Loading the XLS source file: country name mapping data

dir_countryname = Config.get("Directory",'countryname')
file_name_cn= Config.get("countryname",'mapping')  #"country_name.xls"

df_cn = pd.io.excel.read_excel(os.path.join(dir_countryname,file_name_cn), na_values=["NaN"], sheetname='ITU', keep_default_na=False)

df_cn = df_cn.set_index('country_name_ITU')
#df_cn['cn_ITU']=df.index.values

## CHANGing data types
df=df.convert_objects(convert_numeric=True)
df=df[range(2000,2012)].astype(float)

## Join two dataframes so that country codes are available to use
df=df.join(df_cn)

## Adding index points to the dataframe    'ISO', 'Subject'
df.set_index(['ISO'], inplace=True)

df.to_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))

##>>> df.head()
##          2000      2001       2002       2003       2004       2005  \
##ISO                                                                    
##AFG        NaN  0.004723   0.004561   0.087891   0.105809   1.224148   
##ALB   0.114097  0.325798   0.390081   0.971900   2.420388   6.043891   
##DZA   0.491706  0.646114   1.591641   2.195360   4.634475   5.843942   
##ASM        NaN       NaN        NaN        NaN        NaN        NaN   
##AND  10.538836       NaN  11.260469  13.546413  26.837954  37.605766
##
##
##          2006       2007   2008   2009  2010  2011       2012  2013 ISO2  \
##ISO                                                                         
##AFG   2.107124   1.900000   1.84   3.55   4.0     5   5.454545   5.9   AF   
##ALB   9.609991  15.036115  23.86  41.20  45.0    49  54.655959  60.1   AL   
##DZA   7.375985   9.451191  10.18  11.23  12.5    14  15.228027  16.5   DZ   
##ASM        NaN        NaN    NaN    NaN   NaN   NaN        NaN   NaN   AS   
##AND  48.936847  70.870000  70.04  78.53  81.0    81  86.434425  94.0   AD   
##
##             cn_ITU  
##ISO                  
##AFG     Afghanistan  
##ALB         Albania  
##DZA         Algeria  
##ASM  American Samoa  
##AND         Andorra  
