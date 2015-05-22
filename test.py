#!/usr/bin/env python

import json
import pytest
from wikidata_suggest import suggest, _wikidata, _wikipedia

def test_wikidata():
    results = _wikidata('tolstoi')
    assert len(results['search']) > 0

def test_wikidata_missing():
    results = _wikidata('Catherine Breshkovksy')
    assert len(results['search']) == 0

def test_wikipedia():
    assert _wikipedia('Catherine Breshkovksy') == "Catherine Breshkovsky"

def test_wikipedia_another():
    results = _wikipedia('leo nikolaievich tolstoy')
    assert "Leo Tolstoy" in results
