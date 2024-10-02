import streamlit as st
from io import BytesIO
import os
from database.chat_history import export_to_excel  # Import your export_to_excel function
from navigation import make_sidebar, admin_make_sidebar
from datetime import datetime

if st.session_state.username == "admin":
    admin_make_sidebar()
else:
    make_sidebar()

# Streamlit app interface

st.subheader("DOWNLOAD CHAT HISTORY")
st.caption("Click the following button to View and Download log file:")

# Get the current date and time
now = datetime.now()
formatted_time = now.strftime("%d-%m-%Y-%H-%M")

# Create the file name
file_name = f"RIDDLELOG_{formatted_time}.xlsx"


# Input text box for the Excel file name
# filename = st.text_input("Enter the Excel file name (without extension):")

# Button to generate and download the Excel file
if st.button("VERIFY AND DOWNLOAD"):
    # Define the full path for the Excel file
    # excel_filename = f"{filename}.xlsx"
    
    # Call the export_to_excel function to generate the Excel file
    export_to_excel(file_name)
    
    # After the Excel file is created, read it into a BytesIO object
    with open(file_name, "rb") as f:
        excel_content = BytesIO(f.read())
    
    # # Provide the download button for the generated Excel file
    st.download_button(
        label="DOWNLOAD EXCEL",
        data=excel_content,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
        # Provide the download button for the generated Excel file

    
    
    # Optionally, you could delete the file from the server after download to avoid storing files
    os.remove(file_name)
