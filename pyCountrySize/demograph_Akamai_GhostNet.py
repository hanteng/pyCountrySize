# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import pyCountrySize

#print "pyCountrySize.sizec.mean():\n",pyCountrySize.sizec.mean()
#print "pyCountrySize.LP.mean():\n",pyCountrySize.LP.mean()

# Customizing figures
import matplotlib.pyplot as plt
import matplotlib as mpl
from ggplot import ggplot, ggsave, aes, geom_point, geom_text, geom_smooth, labs, theme_matplotlib, theme, element_text, facet_grid

mpl.rcParams["axes.labelsize"] = 18.0
mpl.rcParams["axes.grid"] = True

mpl.rcParams["font.size"] = 12.0#
mpl.rcParams["axes.edgecolor"] = "black" 
mpl.rcParams["axes.labelcolor"] = "black"
mpl.rcParams["grid.color"] = "grey" # or  whatever you want

mpl.rcParams["figure.subplot.wspace"] = 0.05
mpl.rcParams["figure.figsize"] = [8*2, 6]
mpl.rcParams["figure.subplot.left"] = 0.08
mpl.rcParams["figure.subplot.right"] = 0.97
mpl.rcParams["figure.subplot.bottom"] = 0.10


## Constructing dataframes with values indexed by ISO country codes
def dataframe_var_from_dict(dep_dictionary, col_label):
    return pd.DataFrame(dep_dictionary.items(), dtype=np.dtype(float), columns=['ISO', col_label]).set_index('ISO')

# cyberattack data
Akamai_Traffic_Source={'CHN':0.43, 'IDN':0.15, 'USA':0.13, 'TWN':0.037, 'IND':0.021, 'RUS':0.02, 'BRA':0.017, 'KOR':0.014, 'TUR':0.012, 'ROU':0.012, }
GhostNet_IPs={'IND':53, 'VNM':130, 'TWN':148, 'CHN':92, 'FRA':15, 'MYS':17, 'IDN':13, 'BGD':12, 'BEL':19, 'JPN':24, 'BTN':13, 'HKG':65, 'PHL':11, 'SLB':36, 'USA':113, }

variables={}
variables['Akamai']=dataframe_var_from_dict(Akamai_Traffic_Source,'Akamai')
variables['GhostNet']=dataframe_var_from_dict(GhostNet_IPs,'GhostNet')


# Contructing dataframes with dependent variables
def dataframe_var_join(df_dictionary):
    for n,x in enumerate(df_dictionary.keys()):
        if n==0:
            df_output=df_dictionary[x].copy(deep=True) #Make a copy of this object
        else:
            df_output=df_output.join(df_dictionary[x], how='outer')
    return df_output

df_variable=dataframe_var_join(variables)
# All possible independent and dependent variables
y_possible = df_variable.columns.values


# Constructing dataframes with independent size variables
x_possible = pyCountrySize.sizec.columns.values
df_size=pyCountrySize.sizec

##Constructing an integrated dataframe df_all
for i,x in enumerate(x_possible):
    for j,y in enumerate(y_possible):
        if x<>y:     
            y_select=df_variable[y_possible[j]]
            x_select=df_size[x_possible[i]]
            df=pd.DataFrame(y_select, index=y_select.keys())
            dfx=pd.DataFrame(x_select, index=x_select.keys())
            df=df.join(dfx)
            df.columns=['y','x']
            df['y_attr']=y_select.name
            df['x_attr']=x_select.name
            df=df.dropna(axis=0) #remove rows with na
            df['ISO_']=df.index.values # turn index to columns
            if i==0 and j==0:
                df_all=df.copy(deep=True) #Make a copy of this object
            else:
                df_all=pd.concat([df_all,df], ignore_index=True)

df_all['ISO']=df_all['ISO_']
#set index
df_all.set_index([df_all.ISO_, df_all.y_attr, df_all.x_attr])


for y_picked in y_possible:
    df_selected=df_all[df_all['y_attr']==y_picked]
    label_len=len(df_selected)/len(x_possible)
    p_d = ggplot(aes(x='x', y='y', label=df_selected['ISO'].values[0:label_len]), data=df_selected)
    p=p_d+geom_point()+\
               geom_text(aes(hjust = 0, vjust = 0, size=10, color='darkblue'))+\
               geom_smooth(aes(x="x", y="y"), method='lm', se=False, color='grey')+\
               facet_grid("y_attr", "x_attr",scales="free")+\
               labs(x = "Size Indicators", y = "Cyber Incidents") +\
               theme_matplotlib()+ theme(axis_text_x  = element_text(angle = 40, hjust = 1))

    #print p
    ggsave(p, "CyberIncidents_%s.png" % y_picked)

