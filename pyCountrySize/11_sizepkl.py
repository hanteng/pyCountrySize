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

fn_input=Config.get("datasource{0}".format(datasource_sn),'filename')

import os.path

import pandas as pd
import numpy as np

df = pd.read_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))


year_picked=Config.get("datasource{0}".format(datasource_sn),'year_picked')
subject_picked=Config.get("datasource{0}".format(datasource_sn),'subject_picked').split(',')

for i,s in enumerate(subject_picked):
    df_picked=df.query('Subject=="{0}"'.format(s))[str(year_picked)]
    if i == 0:
        df_size=df_picked.unstack()
    else:
        df_size[s] = df_picked.unstack()

## Duplicate index column
df_size[df_size.index.name]=df_size.index

## Output size pkl
fn_ouput="_".join(["size"]+[x for x in df_size.columns if x[0:3]<>"ISO"])

df_size.to_pickle(os.path.join(dir_outcome, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))
df_size.to_pickle(os.path.join(dir_outcome, fn_ouput + "." + fn_suffix))
