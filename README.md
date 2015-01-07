pyCountrySize
=============

python scripts to load Country Size datasets for research/analytics

The data selection and example graphs will be explained as [an exercise explained here in a blog post](http://people.oii.ox.ac.uk/hanteng/to.be.determined), researchers are encouraged to modify the codes for their own research questions.


INSTALL

pip install git+https://github.com/hanteng/pyCountrySize.git

or

pip install git+git://github.com/hanteng/pyCountrySize.git


In the event that you don't have git installed, try this:

pip install https://github.com/hanteng/pyCountrySize/zipball/master


=============
import pyCountrySize

pyCountrySize.LP.head()

pyCountrySize.LP.mean()

pyCountrySize.meta['LP']

pyCountrySize.description['LP']

