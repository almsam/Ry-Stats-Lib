"""
Module for indexing, slicing, and selection 
"""

import numpy as np
import pandas as pd
from typing import Any, Callable

__all__ = [ # export funtions for import * 
    "subset",
    "unique",
    "select",
]

def subset(obj, condition): # filter rows based on boolean condition

    if isinstance(obj, pd.DataFrame):
        return obj[condition]
    elif isinstance(obj, np.ndarray):
        return obj[condition]
    elif isinstance(obj, (list, tuple)):
        return [item for item, cdtn in zip(obj, condition) if cdtn == True]
    else:
        raise TypeError(f"Cannot subset type {type(obj)}")

def unique(obj): # extract unique elements
    
    if isinstance(obj, pd.DataFrame):
        return obj.drop_duplicates()
    elif isinstance(obj, pd.Series):
        return obj.unique()
    elif isinstance(obj, np.ndarray):
        return np.unique(obj)
    elif isinstance(obj, (list, tuple)):
        return list(dict.fromkeys(obj)) # preserves insertion order
    else:
        raise TypeError(f"Cannot get unique elements from type {type(obj)}")

def select(obj, cols): # select columns by name or index
    
    if isinstance(obj, pd.DataFrame):
        if isinstance(cols, (list, tuple)):
            return obj[list(cols)]
        else:
            return obj[cols]
    else:
        raise TypeError("select() only works with DataFrames")