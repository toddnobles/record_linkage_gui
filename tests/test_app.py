"""Tests for app.py."""

import types
from io import BytesIO

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from record_linkage.app import find_image, get_image_map, load_data


def csv_upload_test():
    """Test if program will crash when given a small file.

    author: tttran01
    reviewer: toddnobles
    category: smoke test
    """
    # creates a fake local binary file simulating a csv file
    csv_bytes = BytesIO(b"col1,col2\nA,1\n")
    df = load_data(csv_bytes)

    assert df is not None

def test_find_image():
    """Test if image selected is in image map.

    author: tttran01
    reviewer: toddnobles
    category: one shot test
    """
    img_map = {"img1.jpg":"image 1", "img2.png":"image 2", "img3.png":"image 3"}

    assert find_image("img1.jpg", img_map) == "image 1"

def edge_test_find_image_none():
    """Test if an empty image map returns None.

    author: tttran01
    reviewer: toddnobles
    category: edge test
    """
    img_map = {}

    assert find_image("some_image.png",img_map) is None

def pattern_test():
    """Test if sample data uploaded to app matches an expected outcome.

    author: tttran01
    reviewer: toddnobles
    category: pattern test
    """
    sample_data = BytesIO(b"Name,StrCol,MissingCol\nAlbert,12345,\n")
    sample_df = load_data(sample_data)

    expected_df = pd.DataFrame({
        "Name": ["Albert"],
        "NumCol": [12345],
        "MissingCol": [pd.NA]
    })

    assert sample_df == expected_df

def test_smoke_load_data(tmp_path):
    """Checks to see if the file created matches what's expected.

    author: honglamv7
    reviewers: nturner27, juliaz35
    """
    # create temp file path with sample csv file
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("a,b,c\n1,2,3\n")

    # call function
    df = load_data(csv_path)

    # check that the file is a dataframe type
    assert isinstance(df, pd.DataFrame)


def test_one_shot_find_image():
    """Tests that a mismatched image file returns None.

    author: honglamv7.
    reviewers: nturner27, juliaz35
    """
    m = {"a.jpg": 123}
    assert find_image("b.jpg", m) is None

def test_pattern_find_image():
    """Testing that find_image works multiple times.

    author: honglamv7
    reviewers: nturner27, juliaz35
    """
    image_map = {
        "a.jpg": "imgA",
        "b.jpg": "imgB",
    }
    assert find_image("a.jpg", image_map) == "imgA"
    assert find_image("b.jpg", image_map) == "imgB"
    assert find_image("c.jpg", image_map) is None

def test_smoke_get_image_map():
    """Check that get_image_map correctly maps uploaded images by filename.

    author: juliaz35.
    reviewer: nturner2/honglamv7
    category: smoke test
    """
    # Minimal "uploaded image" objects with a .name attribute
    img1 = types.SimpleNamespace(name="img1.png")
    img2 = types.SimpleNamespace(name="img2.jpg")

    image_map = get_image_map([img1, img2])

    # Just sanity-check that the mapping is created correctly
    assert isinstance(image_map, dict)
    assert set(image_map.keys()) == {"img1.png", "img2.jpg"}

def test_oneshot_get_image_map_single_image():
    """Verify get_image_map correctly handles a single uploaded image.

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
    """Check that load_data correctly handles a CSV with headers but no data rows.

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
    """Verify get_image_map maps multiple uploaded images to their filenames.

    author: juliaz35
    reviewer: nturner2/honglamv7
    category: pattern test
    justification: verify get_image_map consistently maps filenames
                   to objects across different lists of images.
    """
    # Build fake uploaded image objects with .name
    uploaded_images = [types.SimpleNamespace(name=name) for name in image_names]
    image_map = get_image_map(uploaded_images)

    # Not in here should get None
    assert find_image("ex4.png", image_map) is None

    image_map = get_image_map(uploaded_images)

    # Keys should match the input names exactly, in any order
    assert set(image_map.keys()) == set(image_names)

    # Each filename should map to an object whose .name is that filename
    for name in image_names:
        assert name in image_map
        assert getattr(image_map[name], "name", None) == name


# Natalie Tests

def test_smoke_find_image():
    """Check that find_image returns the correct object for a given filename.

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
    """Verify load_data returns an empty DataFrame for non-CSV (Excel) files.

    author: nturner2
    reviewer: honglamv7/juliaz35
    category: edge test
    """
    # Needed a temporary file; had to get help with that
    # something that is not in distribution - excel
    excel_file = tmp_path / "file.xlsx"
    excel_file.write_text("this is not a CSV")

    result = load_data(excel_file)

    # if you do put in an excel then you get a df with no rows
    assert isinstance(result, pd.DataFrame)
    assert result.empty

def test_oneshot_load_data(tmp_path):
    """Check that load_data correctly reads a known CSV file.

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
    """Verify find_image returns the correct object or None for given filenames.

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

def test_application_runs():
    """Check that the application runs without exceptions using AppTest.

    author: toddnobles
    reviewer: tttran01
    category: smoke test
    """
    at = AppTest.from_file("src/record_linkage/app.py").run()
    assert not at.exception
    return


def test_not_csv_upload():
    """Verify load_data raises an error when given a non-CSV file.

    author: toddnobles
    reviewer: tttran01
    category: edge test
    Testing that the load_data function behaves as expected when given
    a non-CSV filepath.
    """
    with pytest.raises(FileNotFoundError):
        # Ideally we want the function to raise a better error here.
        # Currently this is caught in the main() function, but we probably
        # want to exract it to be self-contained here. (I think)
        load_data("test.pdf")
    return

def test_load_data():
    """Check that load_data successfully reads a CSV file.

    author: toddnobles
    reviewer: tttran01
    category: oneshot test
    Testing that an uploaded CSV actually loads.
    """
    df = load_data("tests/test_data/sample_data.csv")
    # We probably want a better function in the main app that tells the user
    # that the CSV is empty if this fails
    assert not df.empty
    return

def test_initial_ui_render():
    """Verify the initial UI renders correctly before any CSV is uploaded.

    author: toddnobles
    reviewer: tttran01
    category: smoke test
    Adding another (sort of) smoke test for the app logic of the order steps
    and sections are displayed to the user.
    I can't figure out how to get the user interactivity testing in Streamlit
    to work for file uploads. There is currently no file_upload testing in
    Streamlit's AppTest. Additionally, I don't think we have pattern test as an
    option here as we do no calculations. So patterns could only be tested if we
    can simulate user inputs which we can't currently do for file uploads
    (which our app requires to run properly). Using this to get experience with
    the AppTest framework.
    """
    at = AppTest.from_file("src/record_linkage/app.py").run()
    assert at.header[0].value == "1. Upload Data"
    # Confirming that the second section hasn't rendered yet
    # since no CSV has been uploaded
    header_values = [h.value for h in at.header]
    assert "2. Configure Mapping" not in header_values
