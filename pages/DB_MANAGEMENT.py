import streamlit as st
import pandas as pd
from database.riddleFetch import bulk_insert_riddles, clear_riddles_table, export_riddles_to_excel
import io
from time import sleep
from navigation import make_sidebar, admin_make_sidebar
from datetime import datetime
if (st.session_state.logged_in == False):
    sleep(0.5)
    st.switch_page("login.py")

if st.session_state.username=="admin":
    admin_make_sidebar()
else:
    make_sidebar()
st.subheader("Database Management")
# Upload Excel sheet
st.caption("Please upload an excel sheet with column question | correct_answer")
uploaded_file = st.file_uploader("", type="xlsx")
# Option to either append or replace data
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        
        # Show preview of the data
        st.write("Preview of uploaded data:")
        st.write(df)
        
        # Insert options
        action = st.radio("Do you want to append to or replace the existing riddles data?", 
                          ('Append', 'Replace'))
        
        if st.button("Insert Data"):
            if action == 'Replace':
                # Clear existing data
                clear_riddles_table()
            
            # Insert new data
            bulk_insert_riddles(df)
            st.success(f"Data successfully {'replaced' if action == 'Replace' else 'appended'}!")
    except Exception as e:
        st.error(f"Error: Unable to read the file. Please upload a valid Excel (.xlsx) file.")

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