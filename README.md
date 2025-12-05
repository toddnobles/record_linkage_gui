# Record Linkage Toolkit
CSE 583 Entity Resolution and Record Linkage Toolkit

## Contributors 
- Natalie Turner, School of Social Work
- Terresa Tran, MSIM
- Honglam Van, Department of Mechanical Engineering
- Todd Nobles, Sociology
- Julia Zhu, MSIM

## Project Description
This toolkit is designed for users working to digitize documents using OCR or computer vision models and who need a way to compare the extracted text to the original images. Additionally, it allows users to make edits to the extracted data as they're reviewing and save these edits to a cleaned version of their data set.

Future extensions will assist users who are trying to link records between datasets and need a way to speed up and reduce the errors in the process of performing hand matches or adjudicating between potential matches.

## Features
### ✓ CSV Upload & Preview
Load a CSV file and preview the first few rows.

### ✓ Image Upload
Upload multiple images (`png`, `jpg`, `jpeg`).  
Duplicate filenames are automatically detected and blocked.

### ✓ Interactive Viewer
 - Select a record from the CSV.
 - Edit multiple text fields.
 - View and rotate the associated image.
 - Save edits back to the dataframe.

### ✓ Export Results
Download the updated CSV with one click.


## Instructions
### 1. Launch the App
From the project’s src/record_linkage directory, run: `streamlit run app.py`

Your browser will open the app at: http://localhost:8501

### 2. Upload Your CSV File

Scroll to **Step 1: Upload Data**

Click “Upload your CSV file” and select a CSV that contains: 
 - Acolumn listing image filenames (e.g., image_name)
 - Any additional cleaned/extracted fields you want to review.

You will see a preview of the first 3 rows.

### 3. Select the Filename Column
Under **Step 2: Configure Mapping**

Use the dropdown labeled “Column with filenames”

Choose the column in your CSV that contains image filenames (e.g., filename, image_id, etc.)

Then choose which columns you'd like to edit in the viewer (default = first 3 columns)

### 4. Upload Images
Under **Step 3: Upload Images**

Click the image uploader and select all the images referenced in the CSV (supported formats: png, jpg, jpeg)

The app will automatically check duplicate filenames → upload is blocked with: “Duplicate file name.”

### 5. Browse and Edit Records
Under Viewer:
 - Choose a record from the dropdown list
 - The left side displays editable fields
 - The right side displays the corresponding image
 - You can rotate the image (0°, 90°, 180°, 270°)

Any text fields you edit are saved into session state.

### 6. Save Changes
Click “Save changes” to write your edits back into the dataframe.

A success message will appear.

### 7. Export the Cleaned CSV
Scroll to the bottom and click: “Download Updated CSV”

This downloads a new CSV file containing:
 - All edits made in the viewer
 - The original column structure
 - Updated values for edited fields

## Dependencies
 - pandas
 - pytest
 - pytest-cov
 - streamlit
 - pillow
 - ruff
