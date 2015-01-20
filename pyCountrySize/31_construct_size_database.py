# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。

import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

dir_source = Config.get("Directory", 'source')
dir_inprocess =  Config.get("Directory",'inprocess')
dir_outcome = Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')

import os.path, glob

import pandas as pd
import numpy as np

filename_list=[os.path.normpath(x) for x in glob.glob(os.path.join(dir_outcome, "size*."+fn_suffix))]

#filename_list.reverse()

init=filename_list.index('sizepkl\\size_IPv4.pkl')
filename_list=filename_list[init:]+filename_list[:init]

for i,f in enumerate(filename_list):
    if i==0:
        df = pd.read_pickle(f)
    else:
        df_ = pd.read_pickle(f)
        #df=df.join(df_, how="outer", on=df_.index.name)
        df = pd.merge(df, df_, on=df_.index.name, how='outer')

dir_db = Config.get("Directory",'database')
fn_db = Config.get("output",'filename')

## Sorting
df = df.sort_index(by=['ISO', 'ISO2'], ascending=[True, True])

## Set ISO index
df = df.set_index('ISO')

## Duplicate index column
df[df.index.name]=df.index

df.to_pickle(os.path.join(dir_db, fn_db))


