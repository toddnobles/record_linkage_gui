"""Tests for app.py"""
import pytest
from streamlit.testing.v1 import AppTest 
from record_linkage.app import load_data

def test_application_runs():
    """
    author: toddnobles
    reviewer: tttran01
    category: smoke test
    """
    at = AppTest.from_file("src/record_linkage/app.py").run()
    assert not at.exception
    return


def test_not_csv_upload():
    """
    author: toddnobles
    reviewer: tttran01
    category: edge test
    Testing that the load_data function behaves as expected when we give it a non-CSV filepath. 
    """
    with pytest.raises(Exception):
        # we ideally want the function to raise a better error here. Currenlty this is caught in the main() function, but we probably want to exract it to be self-contained here. (I think)
        load_data("test.pdf")
    return

def test_load_data():
    """
    author: toddnobles
    reviewer: tttran01
    category: oneshot test
    Testing that an uploaded CSV actually loads.
    """
    df = load_data("tests/test_data/sample_data.csv")
    # we probably want a better function in the main app that tells the user that the CSV is empty if this fails
    assert not df.empty
    return

def test_initial_ui_render():
    """
    author: toddnobles
    reviewer: tttran01
    category: smoke test
    Adding another (sort of) smoke test for the app logic of the order steps and sections are displayed to the user. 
    I can't figure out how to get the user interactivity testing in Streamlit to work for file uploads. There is currently no file_upload testing in Streamlit's AppTest. Additionally, I don't think we have pattern test as an option here as we do no calculations. So patterns could only be tested if we can simulate user inputs which we can't currently do for file uploads (which our app requires to run properly). Using this to get experience with the AppTest framework.  
    """
    at = AppTest.from_file("src/record_linkage/app.py").run()
    assert at.header[0].value == "1. Upload Data"
    ## confirming that the second section hasn't rendered yet since no CSV has been uploaded
    header_values = [h.value for h in at.header]
    assert "2. Configure Mapping" not in header_values
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
