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
