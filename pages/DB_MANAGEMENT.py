import streamlit as st
import pandas as pd
from database.riddleFetch import bulk_insert_riddles, clear_riddles_table, export_riddles_to_excel
import io
from time import sleep
from navigation import make_sidebar, admin_make_sidebar
from datetime import datetime

# User authentication and sidebar setup
if (st.session_state.logged_in == False):
    sleep(0.5)
    st.switch_page("login.py")

if st.session_state.username == "admin":
    admin_make_sidebar()
else:
    make_sidebar()

st.subheader("Database Management")
st.caption("Please upload an Excel sheet with columns: question | correct_answer")

# Upload Excel sheet
uploaded_file = st.file_uploader("", type="xlsx")

# Option to either append or replace data
if uploaded_file:
    try:
        # Read the uploaded file into a Pandas DataFrame
        df = pd.read_excel(uploaded_file)
        
        # Validate the required columns
        if 'question' not in df.columns or 'correct_answer' not in df.columns:
            st.error("The uploaded Excel file must contain 'question' and 'correct_answer' columns.")
        else:
            # Show a preview of the data
            st.write("Preview of uploaded data:")
            st.write(df)

            # Insert options: Append or Replace
            action = st.radio("Do you want to append to or replace the existing riddles data?", 
                              ('Append', 'Replace'))
            
            # Insert Data button
            if st.button("Insert Data"):
                # Perform database operations only if the file is valid
                if action == 'Replace':
                    # Clear existing data before inserting new data
                    with st.spinner("Replacing existing data..."):
                        clear_riddles_table()
                
                # Bulk insert new data
                with st.spinner("Inserting data..."):
                    bulk_insert_riddles(df)
                st.success(f"Data successfully {'replaced' if action == 'Replace' else 'appended'}!")
    
    except Exception as e:
        # Display error message if file upload fails
        st.error(f"Error: Unable to read the file. Please upload a valid Excel (.xlsx) file.")
        
st.divider()

# Exporting the data
st.subheader("Export Riddles to Excel")
if st.button("Export"):
    riddles_df = export_riddles_to_excel()
    st.write(riddles_df)  # Show data preview
    
    # Save DataFrame to an in-memory buffer
    buffer = io.BytesIO()
    riddles_df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)

    # Get the current date and time
    now = datetime.now()
    formatted_time = now.strftime("%d-%m-%Y-%H-%M")

    # Create the file name
    file_name = f"RIDDLEDB_{formatted_time}.xlsx"

    # Download link
    st.download_button(
        label="Download data as Excel",
        data=buffer,
        file_name=file_name,
        mime="application/vnd.ms-excel"
    )
