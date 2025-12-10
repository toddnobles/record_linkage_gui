# Record Linkage Toolkit
CSE 583 Entity Resolution and Record Linkage Toolkit

## Contributors 
- Natalie Turner, School of Social Work
- Terresa Tran, MSIM
- Honglam Van, Department of Mechanical Engineering
- Todd Nobles, Department of Sociology. Contributions: project conceptualization, project administration, test development, writing application script 
- Julia Zhu, MSIM

## Project Description
This toolkit is designed for users working to digitize documents using OCR or computer vision models and who need a way to compare the extracted text to the original images. Additionally, it allows users to make edits to the extracted data as they're reviewing and save these edits to a cleaned version of their data set.

Future extensions will assist users who are trying to link records between datasets and need a way to speed up and reduce the errors in the process of performing hand matches or adjudicating between potential matches.

## Project Structure
The project has the following structure:

 - record_linkage_gui
   - |- README.md
   - |- LICENSE
   - |- environment.yml
   - |- pyproject.toml
   - |- src
      - |- record_linkage
          - |- app.py
          - |- __init__.py
   - |-tests
      - |- test_app.py
      - |- test_data
        - |- sample_data.csv
        - |- 100V1274_no_back.png
        - |- 100V1276_no_back.png
   - |- docs
      - |- user_story.md
      - |- functional_specification.md
      - |- component_specification.md
      - |- Record Linkage Demo.mp4
   - |- .github
      - |- workflows
        - |- testsuite.yml
   - |- .gitignore

## Core Module Code
The core functionality of the toolkit lives inside `src/record_linkage/app.py`. This file contains:
1. `load_data()` reads and caches the uploaded CSV file. This ensures the dataframe is only loaded once, even when the user interacts with Streamlit widgets.
   
2. `get_image_map()` processes uploaded image files and creates a mapping:`{ filename → UploadedFile object }`

   It also performs validation:
 - Detects duplicate filenames
 - Ensures uploaded image names appear in the CSV

3. `find_image()` looks up an image by filename in the image_map. Returns the image object or None.
   
4. `render_viewer()` displays:
 - Editable text fields on the left
 - The corresponding image preview on the right
 - A rotation selector
 - A Save button that updates the dataframe
 - A Download button for exporting cleaned data

5. `main()` is the Streamlit entry point that defines the workflow:
 - Upload CSV
 - Select filename column & fields to edit
 - Upload images
 - Validate images vs. CSV
 - Render the viewer
 - Export cleaned CSV

## Dependencies
 - pandas
 - pytest
 - pytest-cov
 - streamlit
 - pillow
 - ruff

## Instructions

### 1. Launch the App
From the project’s src/record_linkage directory, run: `streamlit run app.py`. Follow the link provided in terminal.

### 2. Upload Your CSV File
Under 'Upload Data', click 'Upload your CSV file' and select a CSV that contains: 
 - Acolumn listing image filenames (e.g., image_name)
 - Any additional cleaned/extracted fields you want to review.

You will see a preview of the first 3 rows.

### 3. Select the Filename Column
Under 'Configure Mapping', use the dropdown labeled 'Column with filenames'

Choose the column in your CSV that contains image filenames (e.g., filename, image_id, etc.)

Then choose which columns you'd like to edit in the viewer (default = first 3 columns)

### 4. Upload Images
Under 'Upload Images', click the image uploader and select all the images referenced in the CSV (supported formats: png, jpg, jpeg)

The app will automatically check duplicate filenames and the upload will be blocked with an error message.

### 5. Browse and Edit Records
Under 'Viewer':
 - Choose a record from the dropdown list
 - The left side displays editable fields
 - The right side displays the corresponding image
 - You can rotate the image (0°, 90°, 180°, 270°)

Any text fields you edit are saved into session state.

### 6. Save Changes
Click 'Save changes' to write your edits back into the dataframe. A success message will appear.

### 7. Export the Cleaned CSV
Scroll to the bottom and click 'Download Updated CSV'

This downloads a new CSV file containing:
 - All edits made in the viewer
 - The original column structure
 - Updated values for edited fields

Demo video: https://github.com/toddnobles/record_linkage_gui/blob/3065acbd021e896de2844e294e82c2f083ede099/docs/Record%20Linkage%20Demo.mp4
