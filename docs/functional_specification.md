## Background
Large scale quantitative analysis of archival data involves a number of steps that are tedious, error prone, and create difficulties for reproducibility. Our tool assists with the first two of these problems by improving the workflow for users who are turning images of historical documents into analysis ready datasets. Users would begin with their scans of documents, run these through their OCR tool of choice. Then, where our tool comes in is during the manual verification and correction of the OCR'd information. Computers have gotten much better at processing images and PDFs but there is almost always a need for manual cleaning.  Our tool allows users to quickly see the information extracted from each image alongside the original image and then make any necessary changes to the text fields. 



## User profile
Below is a sample of the user stories we generated during our project planning. For a full set of example users please see the user_story.md file. In general, our tool is designed for researchers who are working to process images of documents into machine readable information. We built the tool so that someone who only has a basic understanding of installing and running one Python command could execute this. No coding knowledge or skills are needed by the user as our tool is all a point, click, and type GUI. 


## Data sources
The data sources for this tool are all user-supplied. We include some example data and images for demonstration purposes, but as long as the user has images that can be linked by name to rows of a CSV file they can use this tool. 

## Use Cases
These are generalized uses or tasks that users might want to complete with the software we're building. 

- Compare side by side text fields extracted from an image and the original image for accuracy and do this in a manner that isn't scrolling through an Excel document. 
- Manually edit the text for a field that was extracted from an image and save a new dataset with the corrected data. 
- For those who are working on testing the accuracy of various OCR techniques our tool also offers the ability to quickly generate a small ground truth dataset by uploading a file with headers only for the extracted text file and a linkage key to the images, and then quickly input the ground truth values that the user can read in the image. 