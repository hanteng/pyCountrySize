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
import numpy as np

df = pd.read_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))


year_picked=Config.get("datasource{0}".format(datasource_sn),'year_picked')


df_picked=df[int(year_picked)]/1.0

df_size=pd.DataFrame(df_picked)
df_size.columns=['IPopRate']


## Loading WEO database for population data LP
fn_input_WEO=Config.get("datasource{0}".format(1),'filename')
df_size2 = pd.read_pickle(os.path.join(dir_outcome, os.path.splitext(os.path.basename(fn_input_WEO))[0] + "." + fn_suffix))
df_size_all=df_size2.join(df_size)

## Turing IP rate into real IP  = 0.01*IP*LP
df_size_all['IPop']=.01*np.round(df_size_all['IPopRate']*df_size_all['LP'],0)


df_size=pd.DataFrame(df_size_all['IPop'])

## Duplicate index column
df_size[df_size.index.name]=df_size.index

## Output size pkl
fn_ouput="_".join(["size"]+[x for x in df_size.columns if x[0:3]<>"ISO"])

df_size.to_pickle(os.path.join(dir_outcome, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))
df_size.to_pickle(os.path.join(dir_outcome, fn_ouput + "." + fn_suffix))

