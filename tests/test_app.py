"""
Tests for app.py 
"""

import pytest
import pandas as pd
from io import BytesIO
from record_linkage.app import load_data, get_image_map, find_image, render_viewer, main

# Terresa Tests:
def csv_upload_test():
    """
    author: tttran01
    reviewer: toddnobles
    category: smoke test
    Test if program will crash when given a small file
    """
    csv_bytes = BytesIO(b"col1,col2\nA,1\n") # creates a fake local binary file simulating a csv file
    df = load_data(csv_bytes)

    assert df is not None

def test_find_image():
    """
    author: tttran01
    reviewer: toddnobles
    category: one shot test
    Test if image selected is in image map
    """
    img_map = {"img1.jpg":"image 1", "img2.png":"image 2", "img3.png":"image 3"}

    assert find_image("img1.jpg", img_map) == "image 1"

def edge_test_find_image_none():
    """
    author: tttran01
    reviewer: toddnobles
    category: edge test
    Test if an empty image map returns None
    """
    img_map = {}

    assert find_image("some_image.png",img_map) is None

def pattern_test():
    """
    author: tttran01
    reviewer: toddnobles
    category: pattern test
    Test if image selected is in image map
    """
    

# Honglam Tests:
def test_smoke_load_data(tmp_path):
    """
    author: honglamv7
    reviewers: nturner27, juliaz35
    Smoke test: checks to see if the file created matches what's expected
    """
    # create temp file path with sample csv file
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("a,b,c\n1,2,3\n")

    # call function
    df = load_data(csv_path)

    # check that the file is a dataframe type
    assert isinstance(df, pd.DataFrame)


def test_one_shot_find_image():
    """
    author: honglamv7
    reviewers: nturner27, juliaz35
    Tests that a mismatched image file returns None
    """

    m = {"a.jpg": 123}
    assert find_image("b.jpg", m) is None

def test_edge_get_image_duplicate_names():
    """
    author: honglamv7
    reviewers: nturner27, juliaz35
    Testing duplicated file names in uploaded images are de-duplicated
    """
    # create mock object that has .name
    class MockImg:
        def __init__(self, name):
            self.name = name

    files = [MockImg("a.jpg"), MockImg("a.jpg")]

    result = get_image_map(files)

    # Check that keys are unique
    assert len(result) == 2
    assert list(result.keys())[0].startswith("a") 
    assert list(result.keys())[1].startswith("a")
    assert list(result.keys())[0] != list(result.keys())[1]

def test_pattern_find_image():
    """
    author: honglamv7
    reviewers: nturner27, juliaz35
    Testing that find_image works multiple times
    """
    image_map = {
        "a.jpg": "imgA",
        "b.jpg": "imgB",
    }
    assert find_image("a.jpg", image_map) == "imgA"
    assert find_image("b.jpg", image_map) == "imgB"
    assert find_image("c.jpg", image_map) is None


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
