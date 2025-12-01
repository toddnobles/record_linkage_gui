"""
Tests for app.py 
"""

import pytest           
import pandas as pd 
from record_linkage.app import load_data, get_image_map, find_image, render_viewer, main
















































# Natalie Tests: 

def test_smoke_find_image():
    """
    author: nturner2
    reviewer: honglamv7/juliaz35
    category: smoke test
    """
    # does find_image work
    # requires inputs of filename and image_map (dictionary)
    filename = "fake.png"
    image_map = {"fake.png": "fake_object"}

    find_image(filename, image_map)
    return 

def test_edge_load_data_excel(tmp_path):
    """
    author: nturner2
    reviewer: honglamv7/juliaz35
    category: edge test
    """
    # needed a temporary file; had to get help with that 
    # something that is not in distribution - excel
    excel_file = tmp_path / "file.xlsx"
    excel_file.write_text("this is not a CSV")

    result = load_data(excel_file)
    
    # if you do put in an excel then you get a df with no rows
    assert isinstance(result, pd.DataFrame)
    assert result.empty

def test_oneshot_load_data(tmp_path):
    """
    author: nturner2
    reviewer: honglamv7/juliaz35
    category: one shot test
    """
    # test something where we know the outcome
    # can create what's expected for load_data (a csv)
    csv_file = tmp_path / "example.csv"
    csv_file.write_text("col1,col2\n1,a\n2,b")
    df = load_data(csv_file)

    assert df.at[0, "col1"] == 1
    assert df.at[1, "col2"] == "b"
    
def test_pattern_find_image_none():
    """
    author: nturner2
    reviewer: honglamv7/juliaz35
    category: pattern test
    """
    # test something where we know the outcome for multiple inputs
    # can create what's expected for find_image 
    image_map = {"ex1.png": "object_ex1", 
                 "ex2.png": "object_ex2",
                 "ex3.png": "object_ex3"}
    assert find_image("ex1.png", image_map) == "object_ex1"
    assert find_image("ex2.png", image_map) == "object_ex2"
    assert find_image("ex3.png", image_map) == "object_ex3"

    # Not in here should get None
    assert find_image("ex4.png", image_map) is None

