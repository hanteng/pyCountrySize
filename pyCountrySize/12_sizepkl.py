# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

dir_source = Config.get("Directory", 'source')
dir_inprocess =  Config.get("Directory",'inprocess')
dir_outcome = Config.get("Directory",'outcome')
fn_suffix = Config.get("Filename",'suffix')

import os.path

import pandas as pd
import numpy as np

## Loading WEO database for population data LP, and other indicators in subject_picked
datasource_sn=1
#fn_input_WEO=Config.get("datasource{0}".format(datasource_sn),'filename')
#df_size2 = pd.read_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input_WEO))[0] + "." + fn_suffix))
#subject_picked=Config.get("datasource{0}".format(datasource_sn),'subject_picked').split(',')
fn_input=Config.get("datasource{0}".format(datasource_sn),'filename')
df = pd.read_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))

year_picked=Config.get("datasource{0}".format(datasource_sn),'year_picked')
year_range=Config.get("datasource{0}".format(datasource_sn),'year_range')
year_range=[int(x) for x in year_range.split(",")]

subject_picked=Config.get("datasource{0}".format(datasource_sn),'subject_picked').split(',')

data=dict()
list_years=[x for x in range(year_range[0],year_range[1]+1)]
list_meta=['Subject_Descriptor','Subject_Notes', 'Units', 'Scale']

for i,s in enumerate(subject_picked):
    df_picked=df.query('Subject=="{0}"'.format(s))[list_years]
    df_size=df_picked.reset_index().drop('Subject', 1).set_index('ISO')
    ## Duplicate index column
    #df_size[df_size.index.name]=df_size.index
    
    data[s]=df_size
        
wp = pd.Panel(data)    

## Loading ITU IPopRate
datasource_sn=2
fn_input=Config.get("datasource{0}".format(datasource_sn),'filename')
df_ITU = pd.read_pickle(os.path.join(dir_inprocess, os.path.splitext(os.path.basename(fn_input))[0] + "." + fn_suffix))

year_range=Config.get("datasource{0}".format(datasource_sn),'year_range')
year_range=[int(x) for x in year_range.split(",")]
year_range_list= range(year_range[0],year_range[1]+1)

## Now putting them together
data={"IPopRate":df_ITU, 'LP':wp['LP'],'PPPGDP':wp['PPPGDP']}
wp=pd.Panel(data)

## Generating IPop: IPop  = 0.01 * IPopRate * LP
df_a=wp['LP'][year_range_list].copy()
df_b=wp['IPopRate'][year_range_list].copy()
df_size3=pd.DataFrame(.01*df_a.values*df_b.values, columns=df_a.columns, index=df_a.index)
df_size3['ISO2']=df_ITU['ISO2']

#'IPop'
data={'LP':wp['LP'],'PPPGDP':wp['PPPGDP'],"IPop":df_size3}
wp=pd.Panel(data)

## Output size pkl
fn_ouput="_".join(["size"]+[x for x in list(wp.keys())])

wp.to_pickle(os.path.join(dir_outcome, fn_ouput + "." + fn_suffix))
# 'sizepkl\\size_IPop_LP_PPPGDP.pkl'

