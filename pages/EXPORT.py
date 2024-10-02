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
file_name = f"CHATLOG_{formatted_time}.xlsx"

# Button to generate and download the Excel file
if st.button("VERIFY AND DOWNLOAD"):
    # Call the export_to_excel function to get a DataFrame
    chat_history_df = export_to_excel()  # Assuming this returns a DataFrame
    
    if not chat_history_df.empty:
        # Show a preview of the data in the app
        st.write(chat_history_df)
        
        # Create an in-memory buffer to save the Excel file
        buffer = BytesIO()
        
        # Write the DataFrame to the buffer as an Excel file
        chat_history_df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)  # Move the cursor to the start of the stream
        
        # Provide a download button for the generated Excel file
        st.download_button(
            label="DOWNLOAD EXCEL",
            data=buffer,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("No data available to download.")