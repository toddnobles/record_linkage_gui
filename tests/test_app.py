"""Tests for app.py"""
import pytest
import pandas as pd
from record_linkage.app import load_data, main

def test_smoke():
    """
    author: toddnobles
    reviewer: tttran01
    category: smoke test
    """
    main()
    return

## edge test
def test_not_csv_upload():
    """
    author: toddnobles
    reviewer: tttran01
    category: edge test
    """
    with pytest.raises(Exception):
        # we ideally want the function to raise a better error here. Currenlty this is caught in the main() function, but we probably want to exract it to be self-contained here. (I think)
        load_data("test.pdf")
    return

## oneshot test
def test_load_data():
    """
    author: toddnobles
    reviewer: tttran01
    category: oneshot test
    Testing that an uploaded CSV actually loads.
    """
    df = load_data("tests/test_data/sample_data.csv")
    # we probably want a better function here that tells the user that the CSV is empty if this fails
    assert not df.empty
    return

## pattern test
def pattern_test_tn ():
    """
    author: toddnobles
    reviewer: tttran01
    category: pattern test (still working on this one)
    """
    input_df = pd.read_csv("tests/test_data/sample_data.csv")
    main()  # Run the main app function to simulate user running the app
    output_df = df ## here df is the output of main(). We can't really simulate user inputs here.
    assert list(input_df.columns) == list(output_df.columns)
    return


