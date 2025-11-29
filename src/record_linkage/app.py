import streamlit as st
import pandas as pd
from PIL import Image

# Functions we use below in the application.
@st.cache_data # we cache the CSV data load here
def load_data(csv_file):
    """Reads the CSV file. Cached so we don't reload the dataframe on every interaction."""
    return pd.read_csv(csv_file)

def get_image_map(uploaded_images):
    """Creates a dictionary mapping filenames to image objects."""
    return {img.name: img for img in uploaded_images}

def find_image(filename, image_map):
    """Searches for a filename in the map. Returns the image object or None."""
    return image_map.get(filename, None)

def render_viewer(image_ref_col, image_map, columns_to_check):
    """Renders the viewer section of the app that displays extracted data alongside its source image. 
    Takes the image reference column name, the mapping created by the get_image_map function, and 
    a list of columns to check/edit supplied by user within the main() function."""
    st.divider()
    st.header("Viewer")

    df = st.session_state.df

    # Make a place to store all edits that the user makes across records
    if "all_edits" not in st.session_state:
        st.session_state.all_edits = {}

    # Select record
    item_list = df[image_ref_col].astype(str).tolist() # we make a list of the values in the image ref column of the CSV
    selected_item_val = st.selectbox("Select an Item to View", item_list) # we provide a dropdown for the user to select which record to view

    if selected_item_val:
        row_index = df[df[image_ref_col].astype(str) == str(selected_item_val)].index[0]
        col_left, col_right = st.columns([1, 2])

        # ===== Left column: Editable Fields =====
        with col_left:
            st.markdown("**Edit Fields:**")

            # If there isn't a record in the all_edits for this selected item, create it
            if selected_item_val not in st.session_state.all_edits:
                st.session_state.all_edits[selected_item_val] = {}
                
                ## Prefill with the dataframe values 
                for col in columns_to_check:
                    st.session_state.all_edits[selected_item_val][col] = str(df.at[row_index, col])

            # Show each column as a vertical text input. The alternate here could be to 
            # use the st.data_editor but that only displays a horizontal row of a dataframe which isn't as visually clear. 
            for col in columns_to_check:
                st.session_state.all_edits[selected_item_val][col] = st.text_input(
                    label=col,
                    value=st.session_state.all_edits[selected_item_val][col],
                    key=f"{selected_item_val}_{col}"
                )

            # Save button updates the dataframe
            if st.button("Save changes"):
                for col in columns_to_check:
                    df.at[row_index, col] = st.session_state.all_edits[selected_item_val][col]
                st.success("Changes saved to dataframe!")
        
        # ===== Right column: image viewer =====
        # Here we display the image associated with the selected record, and allow user to rotate it 
        with col_right:
            search_filename = str(selected_item_val)
            image_file = find_image(search_filename, image_map)
            st.markdown("**Image Preview:**")
            if image_file:
                st.markdown(f"*{image_file.name}*")
                rotation_angle = st.selectbox("Rotate Image", [0, 90, 180, 270], index=0)
                image = Image.open(image_file)
                rotated = image.rotate(-rotation_angle, expand=True)
                st.image(rotated, use_container_width=True)
            else:
                st.warning(f"Could not find image for: '{search_filename}'")

    # Download button outside of record selection to export updated CSV
    # This is a bit ugly in its current location, but works for now. 
    st.download_button(
        "Download Updated CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="cleaned_output.csv",
        mime="text/csv"
    )

# ====== Main App =======
def main():
    st.set_page_config(page_title="CSV Image Viewer", layout="wide")
    st.title("Record Cleaning and Extraction Checking")

    # --- Step 1: Upload CSV ---
    st.header("1. Upload Data")
    csv_file = st.file_uploader("Upload your CSV file", type=['csv'])
    if not csv_file:
        st.info("Please upload a CSV file to start.")
        return

    # Load CSV and store in session_state
    if "df" not in st.session_state or st.session_state.get("uploaded_file_name") != csv_file.name:
        st.session_state.df = load_data(csv_file)
        st.session_state.uploaded_file_name = csv_file.name

    st.write("Preview:", st.session_state.df.head(3))

    # Step 2: Configure Mapping 
    st.header("2. Configure Mapping")
    image_ref_col = st.selectbox("Column with filenames:", options=st.session_state.df.columns)

    columns_to_check = st.multiselect(
        "Columns to check for data cleaning:",
        options=st.session_state.df.columns,
        default=st.session_state.df.columns.tolist()[0:3]
    )

    # Step 3: Upload Images 
    st.header("3. Upload Images")
    uploaded_images = st.file_uploader(
        "Select images", 
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg']
    )
    if not uploaded_images:
        st.warning("Please upload images to proceed.")
        return

    image_map = get_image_map(uploaded_images)
    st.success(f"Loaded {len(image_map)} images.")

    # Step 4: Render Viewer 
    render_viewer(image_ref_col=image_ref_col, image_map=image_map, columns_to_check=columns_to_check)

# ======= Run App ========
## For now this works with running streamlit run gui_application.py, we may need to modify this as we package this further 
if __name__ == "__main__":
    main()
