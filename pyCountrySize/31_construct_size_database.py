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
## Basis: >>> wp.items   from size_IPop_LP_PPPGDP.pkl
# Index([u'IPop', u'LP', u'PPPGDP'], dtype='object')
init=[i for i,x in enumerate(filename_list) if "IPop" in x][0]
filename_list=filename_list[init:]+filename_list[:init]

data=dict()
for i,f in enumerate(filename_list):
    if i==0:
        wp = pd.read_pickle(f)
        for item in list(wp.items):
            data[item]=wp[item]
    else:
        df_ = pd.read_pickle(f)
        #df=df.join(df_, how="outer", on=df_.index.name)
        data_label=f.split("size_")[1].split(".pkl")[0]
        data[data_label]=df_

## Reconstructing panel
wp=pd.Panel(data)
##>>> wp.items
##Index([u'IH', u'IPop', u'IPv4', u'LP', u'PPPGDP'], dtype='object')

dir_db = Config.get("Directory",'database')
fn_db = Config.get("output",'filename')


wp.to_pickle(os.path.join(dir_db, fn_db))


