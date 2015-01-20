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
xl = pd.ExcelFile(os.path.join(dir_source,fn_input))
df = xl.parse(xl.sheet_names[0])

## REMOVing unneeded data
df=df.iloc[:,1:14]  #slicing notes columns off the dataframe
colnames=df.iloc[0] 
df.columns=colnames.astype(int) #renaming columns
df=df.iloc[1:,]     #slicing first row off the dataframe
df.index.name="country_name_ITU"    #renaming first column

## Loading the XLS source file: country name mapping data

dir_countryname = Config.get("Directory",'countryname')
file_name_cn= Config.get("countryname",'mapping')  #"country_name.xls"

xl_cn = pd.ExcelFile(os.path.join(dir_countryname,file_name_cn))
df_cn = xl_cn.parse('ITU')

df_cn = df_cn.set_index('country_name_ITU')
df_cn['cn_ITU']=df.index.values

## CHANGing data types
df[range(2001,2012)].astype(float)
df.convert_objects(convert_numeric=True)

## Join two dataframes so that country codes are available to use
df=df.join(df_cn)

## Adding index points to the dataframe    'ISO', 'Subject'
df.set_index(['ISO'], inplace=True)

df.to_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))
