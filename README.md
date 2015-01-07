pyCountrySize
=============

python scripts to load Country Size datasets for research/analytics

The data selection and example graphs will be explained as [an exercise explained here in a blog post](http://people.oii.ox.ac.uk/hanteng/to.be.determined), researchers are encouraged to modify the codes for their own research questions.


#INSTALL

	pip install git+https://github.com/hanteng/pyCountrySize.git

or

	pip install git+git://github.com/hanteng/pyCountrySize.git


In the event that you don't have git installed, try this:

	pip install https://github.com/hanteng/pyCountrySize/zipball/master


#Usage
1. run python
2. excute the following codes
```
import pyCountrySize
pyCountrySize.LP.head()
pyCountrySize.LP.mean()
pyCountrySize.meta['LP']
pyCountrySize.description['LP']
```

#Outcome
```
>>> pyCountrySize.LP.head()
ISO
AFG    30.552
AGO    20.820
ALB     2.788
ARE     9.031
ARG    41.492
Name: LP, dtype: float64
>>> pyCountrySize.LP.mean()
37.757295698924715
>>> pyCountrySize.meta['LP']
u'Population in 2013 (IMF WEO)'
>>> pyCountrySize.description['LP']
u'Population in 2013 (in millions) from IMF World Economic Outlook (WEO) database, October 2014'
```

#Visualization using ggplot
1. Install [ggplot for python](http://ggplot.yhathq.com/) first

2. Then execute the following codes:

'''
import pyCountrySize
from ggplot import *
(x_picked, y_picked)=("LP", "PPPGDP") #assigning LP to x axis, PPPGDP to y axis
p_d = ggplot(aes(x=x_picked, y=y_picked, label=pyCountrySize.sizec.index.values), data=pyCountrySize.sizec)
p=p_d+geom_point()+\
           geom_text(aes(hjust = 0, vjust = 0, size=10, color='darkblue'))+\
           geom_smooth(aes(x=x_picked, y=y_picked), method='lm', se=False, color='grey')+\
           labs(x = ":\n".join([x_picked, pyCountrySize.meta[x_picked]]), y = ":\n".join([y_picked, pyCountrySize.meta[y_picked]])) +\
           theme_matplotlib()+ theme(axis_text_x  = element_text(angle = 40, hjust = 1))
print p
'''

More refined examples can be found in the demograph_*.py scripts, with output graph files  *.png in the folder of [pyCountrySize](https://github.com/hanteng/pyCountrySize/tree/master/pyCountrySize)