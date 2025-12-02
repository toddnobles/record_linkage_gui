import pytest
import pandas as pd

from record_linkage.app import load_data, get_image_map, find_image, render_viewer, main

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