import pytest
import pandas as pd
from io import BytesIO
from record_linkage.app import load_data, find_image

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
