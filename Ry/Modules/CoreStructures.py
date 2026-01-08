"""
Core Structures: Shape and metadata functions
"""

from typing import Any, Optional, Union, List

import numpy as np
import pandas as pd

__all__ = [
    "dim",
    "nrow",
    "ncol",
    "shape",
    "length",
    "class_name",
    "type_of",
    "attrs",
    "colnames",
    "rownames",
]

def dim(x): 
    """
    Return dimensions of DataFrame, ndarray, or length of list/tuple
    """
    if isinstance(x, pd.DataFrame):
        return x.shape
    elif isinstance(x, np.ndarray):
        return x.shape
    elif isinstance(x, (list, tuple)):
        return (len(x),)
    else:
        return None

def shape(x):
    """
    Alias returning array dimensions
    """
    return dim(x)

def nrow(x):
    """
    Returns number of rows in x
    """
    if isinstance(x, pd.DataFrame):
        return len(x)
    elif isinstance(x, np.ndarray):
        return x.shape[0] if x.ndim > 0 else 1
    elif isinstance(x, (list, tuple)):
        return len(x)
    else:
        return None

def ncol(x):
    """
    Returns number of columns in x
    """
    if isinstance(x, pd.DataFrame):
        return len(x.columns)
    elif isinstance(x, np.ndarray):
        return x.shape[1] if x.ndim > 1 else 1
    else:
        return None

def length(x):
    """
    Return total number of elements in x
    """
    if isinstance(x, (pd.DataFrame, pd.Series)):
        return x.size
    elif isinstance(x, np.ndarray):
        return x.size
    elif isinstance(x, (list, tuple, str, dict)):
        return len(x)
    else:
        return None

def class_name(x):
    """
    Returns class name of x as string; e.g., type([1,2,3]).__name__ returns 'list'
    """
    return type(x).__name__

def type_of(x):
    """
    Returns actual Python type object of x; e.g., type([1,2,3]) returns <class 'list'>
    """
    return type(x)