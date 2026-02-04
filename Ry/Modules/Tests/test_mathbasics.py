import numpy as np
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from Ry.Modules.MathBasic import *

# ---------- SUM / PROD ----------
def test_sum():
    assert Sum([1,2,3]) == 6

def test_prod():
    assert prod([2,3,4]) == 24

# ---------- MEAN / MEDIAN ----------
def test_mean():
    assert mean([2,4,6]) == 4

def test_median_even():
    assert median([1,2,3,4]) == 2.5

def test_median_odd():
    assert median([1,2,3]) == 2

# ---------- MODE ----------
def test_mode_single():
    assert mode([1,1,2,3]) == 1

def test_mode_multiple():
    assert set(mode([1,1,2,2,3])) == {1,2}

# ---------- VAR / SD ----------
def test_variance_sample():
    x = [2,4,6]
    assert np.isclose(var(x, ddof=1), np.var(x, ddof=1))

def test_sd_sample():
    x = [2,4,6]
    assert np.isclose(sd(x, ddof=1), np.std(x, ddof=1))

# ---------- COV / COR ----------
def test_covariance():
    x = [1,2,3]
    y = [1,5,7]
    assert np.isclose(cov(x,y), np.cov(x,y)[0,1])

def test_correlation():
    x = [1,2,3]
    y = [1,5,7]
    assert np.isclose(cor(x,y), np.corrcoef(x,y)[0,1])

# ---------- MIN / MAX / RANGE ----------
def test_min_max():
    x = [5,1,9]
    assert vec_min(x) == 1
    assert vec_max(x) == 9

def test_range():
    assert vec_range([2,8,4]) == (2,8)

# ---------- RANK ----------
def test_rank():
    x = [10,20,20,30]
    assert rank(x) == [1.0,2.5,2.5,4.0]

# ---------- QUANTILE ----------
def test_quantile_single():
    x = [10,20,30,40]
    assert quantile(x, 0.5) == 25

def test_quantile_multiple():
    x = [10,20,30,40]
    q = [0.25,0.75]
    assert np.allclose(quantile(x,q), np.quantile(x,q))

# ---------- ERROR TESTS ----------
def test_empty_vector():
    with pytest.raises(ValueError):
        mean([])

def test_bad_quantile():
    with pytest.raises(ValueError):
        quantile([1,2,3], 1.5)
