import pytest
import pandas as pd
from io import BytesIO
from record_linkage.app import load_data, main

def csv_upload_test():
    """
    author: tttran01
    reviewer: toddnobles
    category: smoke test
    """
    csv_bytes = BytesIO(b"col1,col2\nA,1\n") # creates a fake local binary file mimiking a csv file
    df = load_data(csv_bytes)

    assert df is not None