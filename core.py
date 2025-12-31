import numpy as np
import pandas as pd

def array(x):
    """Create an n-dimensional array"""
    return np.array(x)

def matrix(x, nrow=None, ncol=None):
    """Create a 2D matrix"""
    arr = np.array(x)
    if nrow and ncol:
        return arr.reshape((nrow, ncol))
    return arr

def df(data):
    """Create a DataFrame"""
    return pd.DataFrame(data)

def seq(start, stop=None, step=1):
    """Generate a numeric sequence"""
    if stop is None:
        return list(range(start))
    return list(range(start, stop + 1, step))

def rep(x, times):
    """Replicate values"""
    return x * times
