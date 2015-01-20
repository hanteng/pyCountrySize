# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

import pyCountrySize
from scipy import stats

(x_picked, y_picked)=("LP", "PPPGDP")

df=pyCountrySize.sizec
df=df.copy()
varx= df[x_picked]  
vary= df[y_picked]


#Dealing with missing values
#http://stackoverflow.com/questions/13643363/linear-regression-of-arrays-containing-nans-in-python-numpy
mask = ~np.isnan(varx) & ~np.isnan(vary)

#Running scipy.stats.linregress
#http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.linregress.html
slope_, intercept_, r_value, p_value, std_err = stats.linregress(varx[mask],vary[mask])
print "r-squared:", r_value**2
print "slope_, intercept_:",slope_, intercept_



import statsmodels.api as sm
est = sm.OLS(vary[mask], varx[mask])
est = est.fit()
print est.summary()


import matplotlib.pyplot as plt

X_prime = np.linspace(varx.min(), varx.max(), 100)[:, np.newaxis]
y_hat = est.predict(X_prime)
plt.scatter(varx, vary, alpha=0.3)
plt.xlabel(x_picked)
plt.ylabel(y_picked)

plt.plot(X_prime, y_hat, 'r', alpha=0.9)  # Add the regression line, colored in red

#plt.show()


# import formula api as alias smf
import statsmodels.formula.api as smf

# formula: response ~ predictors
est = smf.ols(formula='%s ~ %s'%(y_picked, x_picked), data=df).fit()
print est.summary()
