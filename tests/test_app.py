

def test_smoke_get_image_map():
    """
    author: juliaz35
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
