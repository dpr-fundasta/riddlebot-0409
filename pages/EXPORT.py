import streamlit as st
from io import BytesIO
import os
from database.chat_history import export_to_excel  # Import your export_to_excel function
from navigation import make_sidebar, admin_make_sidebar

if st.session_state.username == "admin":
    admin_make_sidebar()
else:
    make_sidebar()

# Streamlit app interface
st.title("Download Quiz Data")

# Input text box for the Excel file name
filename = st.text_input("Enter the Excel file name (without extension):")

# Button to generate and download the Excel file
if st.button("SUBMIT"):
    # Define the full path for the Excel file
    excel_filename = f"{filename}.xlsx"
    
    # Call the export_to_excel function to generate the Excel file
    export_to_excel(excel_filename)
    
    # After the Excel file is created, read it into a BytesIO object
    with open(excel_filename, "rb") as f:
        excel_content = BytesIO(f.read())
    
    # # Provide the download button for the generated Excel file
    st.download_button(
        label="DOWNLOAD EXCEL",
        data=excel_content,
        file_name=excel_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
        # Provide the download button for the generated Excel file

    
    
    # Optionally, you could delete the file from the server after download to avoid storing files
    os.remove(excel_filename)
