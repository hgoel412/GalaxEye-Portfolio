"""Unit tests for STK data parsers"""

import pytest
import pandas as pd
from src.parsers.parse_stk_access import parse_access_files

def test_parse_access_files():
    """Test STK access file parsing"""
    data = parse_access_files()
    assert len(data) > 0
    assert 'constellation_size' in data.columns
    assert 'access_start' in data.columns

def test_data_quality():
    """Verify no missing data"""
    data = parse_access_files()
    assert data.isnull().sum().sum() == 0

def test_constellation_sizes():
    """Verify expected constellation sizes"""
    data = parse_access_files()
    sizes = data['constellation_size'].unique()
    assert set(sizes) == {6, 12, 32}
