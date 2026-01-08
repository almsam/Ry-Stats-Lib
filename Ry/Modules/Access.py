"""
Module for indexing, slicing, and selection 
"""

import numpy as np
import pandas as pd

__all__ = [ # export funtions for import * 
    "subset",
    "unique",
    "select",
]

def subset(obj, condition): # filter rows based on boolean condition
    
    """
    Receives an object and boolean condition, returns filtered rows/elements
    """

    if isinstance(obj, pd.DataFrame):
        return obj[condition]
    elif isinstance(obj, np.ndarray):
        return obj[condition]
    elif isinstance(obj, (list, tuple)):
        return [item for item, cdtn in zip(obj, condition) if cdtn == True]
    else:
        raise TypeError(f"Cannot subset type {type(obj)}")

def unique(obj): # extract unique elements
    
    """
    Receives an object, returns unique elements with duplicates removed; preserves order when possible
    """
    
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

def select(obj, cols):
    
    """
    Receives a DataFrame and column names/indices, returns selected columns
    """
    
    if isinstance(obj, pd.DataFrame):
        if isinstance(cols, (list, tuple)):
            return obj[list(cols)]
        else:
            return obj[cols]
    else:
        raise TypeError("select() only works with DataFrames")