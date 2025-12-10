## List of components and subcomponents


These are the components of the data checking portion of the record linkage tool. The overarching goal is for a user to upload a file of extracted data, select fields they'd like to confirm were OCRd correctly by viewing the extracted data beside the image in the GUI. The user should be able to edit any errors to these fields, have those changes saved, and at the end of a session download a log of edits and a csv that contains the full original dataset with the edits incorporated. 

- Setup GUI
    - File upload: Field to allow user to upload/point to CSV (can build out other file type handling in future and determine whether they're uploading or pointing to file based on if this is web based or run locally)
    - Input field in the CSV that represents the key for linkage to the images
    - Select Fields: lets users select the columns of the csv they want to view
- Interaction capabilities
    - Zoom in/out buttons for zooming in/out on image
    - Search bar for searching for specific row of data
- Data Display 
    - Text fields/boxes that display the value for each of the selected fields for each row of data. These should be editable so a user can make corrections to the data.
- Image display 
    - Display the image for an associated row of the uploaded CSV.
    - Ability to pan around the image along with the zoom feature described above.    
- Data export
    - Ability to export a csv with any changes made using the GUI
    - A log of the edits made. This could be done by us creating a database on the backend when a user uploads the csv and logging edits to it. Open to other ideas. 

### Preliminary Plan: List of Tasks
- Upload file containing data
- Select columns users want to check for data cleaning
- Upload image for data comparison
- Edit data fields to match image