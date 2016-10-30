# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
datasource_sn=3

import configparser
Config = configparser.ConfigParser()
Config.read("config.ini")

dir_source = Config.get("Directory", 'source')
dir_inprocess =  Config.get("Directory",'inprocess')
dir_outcome = Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')

fn_input=Config.get("datasource{0}".format(datasource_sn),'filename')
subject_picked=Config.get("datasource{0}".format(datasource_sn),'subject_picked')
year_picked=Config.get("datasource{0}".format(datasource_sn),'year_picked')

import os.path

import pandas as pd
import numpy as np

## Loading the TXT source file
df = pd.io.parsers.read_table(os.path.join(dir_source,fn_input), sep="\s\s+", index_col=0, header=None,
                              names = ["sn","cn",subject_picked], thousands=',')

# dtype={"sn": np.int32, "cn": "S45", "IH": np.float}

##>>> df.head()
##               cn         IS
##sn                          
##1   United States  505000000
##2           Japan   64453000
##3          Brazil   26577000
##4           Italy   25662000
##5           China   20602000

## Set Index and Rename
df=df.set_index("cn")               #set index
df.index.name="country_name_CIA"    #rename


## Loading the XLS source file: country name mapping data
dir_countryname = Config.get("Directory",'countryname')
file_name_cn= Config.get("countryname",'mapping')  #"country_name.xls"

df_cn = pd.io.excel.read_excel(os.path.join(dir_countryname,file_name_cn), na_values=["NaN"], sheetname='CIA', keep_default_na=False)

df_cn = df_cn.set_index('country_name_CIA')
#df_cn['cn_CIA']=df.index.values

## Join two dataframes so that country codes are available to use
df=df.join(df_cn)

## Adding index points to the dataframe    'ISO', 'Subject'
df.set_index(['ISO'], inplace=True)


df.to_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))

##>>> df.head()
##            IH ISO2  ISO
##ISO                     
##USA  505000000   US  USA
##JPN   64453000   JP  JPN
##BRA   26577000   BR  BRA
##ITA   25662000   IT  ITA
##CHN   20602000   CN  CHN
