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

import os.path

import pandas as pd
import numpy as np

df = pd.read_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))

## Get the # of IPv4 addressed scaled to millons

df['IPv4_old']=df.IPv4
df['IPv4']=df.IPv4_old*1e-6  # just only one dataset to pick, no time series data
                    #*1e-6 (million)
df_size=pd.DataFrame(df['IPv4'])

## Duplicate index column
df_size[df_size.index.name]=df_size.index

## Output size pkl
fn_ouput="_".join(["size"]+[x for x in df_size.columns if x[0:3]<>"ISO"])

df_size.to_pickle(os.path.join(dir_outcome, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))
df_size.to_pickle(os.path.join(dir_outcome, fn_ouput + "." + fn_suffix))

