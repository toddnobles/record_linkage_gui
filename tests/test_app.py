import pytest
import pandas as pd
import types

from record_linkage.app import load_data, get_image_map, find_image

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
"""
Tests for app.py 
"""


def test_oneshot_get_image_map_single_image():
    """
    author: juliaz35
    reviewer: nturner2/honglamv7
    category: one-shot test
    """
    # One specific input → one specific expected mapping
    img = types.SimpleNamespace(name="only_image.png")

    image_map = get_image_map([img])

    assert list(image_map.keys()) == ["only_image.png"]
    # Make sure the value is the *same object*, not a copy
    assert image_map["only_image.png"] is img


def test_edge_load_data_empty_csv(tmp_path):
    """
    author: juliaz35
    reviewer: nturner2/honglamv7
    category: edge test
    """
    # Different edge case than teammate's test:
    # here the file IS a CSV, but it has headers and no data rows.
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("col1,col2\n", encoding="utf-8")

    df = load_data(csv_file)

    # Expect correct columns but zero rows
    assert list(df.columns) == ["col1", "col2"]
    assert df.empty
    assert len(df) == 0


@pytest.mark.parametrize(
    "image_names",
    [
        ["a.png"],
        ["a.png", "b.png", "c.png"],
        ["file1.tif", "file2.tif"],
    ],
)
def test_pattern_get_image_map_multiple_images(image_names):
    """
    author: juliaz35
    reviewer: nturner2/honglamv7
    category: pattern test
    justification: verify get_image_map consistently maps filenames
                   to objects across different lists of images.
    """
    # Build fake uploaded image objects with .name
    uploaded_images = [types.SimpleNamespace(name=name) for name in image_names]

    image_map = get_image_map(uploaded_images)

    # Keys should match the input names exactly, in any order
    assert set(image_map.keys()) == set(image_names)

    # Each filename should map to an object whose .name is that filename
    for name in image_names:
        assert name in image_map
        assert getattr(image_map[name], "name", None) == name
