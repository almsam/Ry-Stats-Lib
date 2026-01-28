"""
Ry Stats Lang — utils/MathBasics.py

This file contains basic functions of math.
"""


import numpy as np
import pandas as pd

def Sum(x):
    if len(x)==0:
        return "Your vector is empty"
    if len(x) ==1:
        return x[0]
    else:
        return np.sum(x)
    
#def prod(x):
    if len(x)==0:
        return "Your vector is empty"
    elif len(x)==1:
        return x[0]
    else:
        return np.prod(x)

def mean(x):
    if len(x)==0:
        return "Your vector is empty"
    elif len(x)==1:
        return x[0]
    else:
        return(Sum(x)/len(x))
    
def median(x):
    if len(x)==0:
        return "Your vector is empty"
    elif len(x)==1:
        return x[0]
    else:
        return(np.median(x))
    
def mode(x):
    if len(x)==0:
        return "Your vector is empty"
    elif len(x)==1:
        return x[0]
    else:
        y=[]
        unique, count = np.unique(x, return_counts=True)
        count_max=np.argmax(count)
        for i in range(len(count)):
            if count[count_max]==count[i]:
                y.append(unique[i])
        if len(y)>=2:
            return y
        else:
            return y[0]
    
def var(x, ddof:int=1):
    if len(x)==0:
        return "Your vector is empty"
    elif len(x)==1:
        return "Your vector has a single item. Cannot calculate the variance."
    elif len(x)<=ddof:
        return "Your ddod if equal or bigger than denominator. Make sure length of float vector minus ddof is bigger than 0."
    else:
        y=[]
        average=mean(x)
        for i in range(len(x)):
            y.append((x[i]-average)**2)
        return Sum(y)/(len(y)-ddof)

def sd(x, ddof:int=1):
    return np.sqrt(var(x,ddof))

def cov(x,y):
    return np.cov(x,y)

def cor(x,y):
    return np.correlate(x,y)

def vec_min(x):
    return np.min(x)

def vec_max(x):
    return np.max(x)

def vec_range(x):
    if len(x)==0:
        return "Your vector is empty"
    elif len(x)==1:
        return " Your vector has one item"
    else:
        return(np.min(x),np.max(x))
    
def rank(x, method: str = "average"):
    return pd.Series(x).rank(method=method)

def quantile(x,q:float | list[float] =0.5):
    if len(x)==0:
        return "Your vector is empry. Cannot calculate qnantile."

    elif np.isscalar(q):
        if q<0 or q>1 :
            return "Your quantile value has to be between 0 to 1"
        else:
            return np.quantile(x,q)
    else:
        for i in range(len(q)):
            if q[i]<0 or q[i]>1:
                return "Your quantiles value has to be between 0 to 1"
        return np.quantile(x,q)

    




    


