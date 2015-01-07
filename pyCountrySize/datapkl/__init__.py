# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import pandas as pd
import os

__all__ = ["LP","PPPGDP","IP","IH", "sizec", "meta", "description"]
__all__ = [str(u) for u in __all__]
_ROOT = os.path.abspath(os.path.dirname(__file__))


file_name="WEO_ITU_CIA_size"
filename_suffix="pkl"

from os.path import basename, join, splitext
sizec=pd.read_pickle(os.path.join(_ROOT, "WEO_ITU_CIA_size.pkl"))

LP=sizec['LP']
PPPGDP=sizec['PPPGDP']
IP=sizec['IP']
IH=sizec['IH']

meta={'LP': "Population in 2013 (IMF WEO)",\
      'PPPGDP': "Economy Size in 2013 (IMF WEO)",\
      'IP': "Internet Population in 2013 (ITU)",\
      'IH': "Internet Hosts in 2012 (CIA)", }

description={'LP': "Population in 2013 (in millions) from IMF World Economic Outlook (WEO) database, October 2014",\
      'PPPGDP': "Economy Size in 2013 (in billions) from IMF World Economic Outlook (WEO) database, October 2014",\
      'IP': "Internet Population in 2013 (in millions) derived from ITU 2014 report and IMF World Economic Outlook (WEO) database, October 2014",\
      'IH': "Internet Hosts in 2012 (in millions) from CIA the World Factbook", }
