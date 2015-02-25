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
subject_picked=Config.get("datasource{0}".format(datasource_sn),'subject_picked')
year_picked=Config.get("datasource{0}".format(datasource_sn),'year_picked')

import os.path

import pandas as pd
import numpy as np

df = pd.read_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))

## Get the # of IPv4 addressed scaled to millons

#df['IPv4_old']=df.IPv4
df['IPv4']=df.IPv4*1e-6  # just only one dataset to pick, no time series data
                    #*1e-6 (million)
df_size=pd.DataFrame(df['IPv4'])

## Duplicate index column
#df_size[df_size.index.name]=df_size.index

## Drop name
df=df.drop("Country_CIPB", axis=1)
## Drop _BOGONS
df=df.drop("_BOGONS", axis=0)

## Change column name to year
l=list(df_size.columns)
l[[i for i,x in enumerate(l) if subject_picked in x][0]]=int(year_picked)
df_size.columns=l

## Output size pkl
fn_output="_".join(["size",subject_picked])

df_size.to_pickle(os.path.join(dir_outcome, fn_output + "." + fn_suffix))
