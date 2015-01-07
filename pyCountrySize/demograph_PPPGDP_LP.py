# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import pyCountrySize

#print "pyCountrySize.sizec.mean():\n",pyCountrySize.sizec.mean()
#print "pyCountrySize.LP.mean():\n",pyCountrySize.LP.mean()

# Customizing figures
import matplotlib.pyplot as plt
import matplotlib as mpl
from ggplot import ggplot, ggsave, aes, geom_point, geom_text, geom_smooth, labs, theme_matplotlib, theme, element_text

mpl.rcParams["axes.labelsize"] = 18.0
mpl.rcParams["axes.grid"] = True

mpl.rcParams["font.size"] = 12.0#
mpl.rcParams["axes.edgecolor"] = "black" 
mpl.rcParams["axes.labelcolor"] = "black"
mpl.rcParams["grid.color"] = "grey" # or  whatever you want

mpl.rcParams["figure.subplot.wspace"] = 0.05
mpl.rcParams["figure.figsize"] = [8*2, 6]
mpl.rcParams["figure.subplot.left"] = 0.15
mpl.rcParams["figure.subplot.right"] = 0.97
mpl.rcParams["figure.subplot.bottom"] = 0.20
mpl.rcParams["figure.figsize"] = [8, 6]

(x_picked, y_picked)=("LP", "PPPGDP")

p_d = ggplot(aes(x=x_picked, y=y_picked, label=pyCountrySize.sizec.index.values), data=pyCountrySize.sizec)

p=p_d+geom_point()+\
           geom_text(aes(hjust = 0, vjust = 0, size=10, color='darkblue'))+\
           geom_smooth(aes(x=x_picked, y=y_picked), method='lm', se=False, color='grey')+\
           labs(x = ":\n".join([x_picked, pyCountrySize.meta[x_picked]]), y = ":\n".join([y_picked, pyCountrySize.meta[y_picked]])) +\
           theme_matplotlib()+ theme(axis_text_x  = element_text(angle = 40, hjust = 1))

#print p
ggsave(p, "output_%s_%s.png" % (y_picked, x_picked) )

