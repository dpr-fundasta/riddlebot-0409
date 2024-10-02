import streamlit as st
import pandas as pd
from database.riddleFetch import bulk_insert_riddles, clear_riddles_table, export_riddles_to_excel

# Upload Excel sheet
st.title("Riddles Management")
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

# Option to either append or replace data
if uploaded_file:
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

# Exporting the data
st.header("Export Riddles to Excel")
if st.button("Export to Excel"):
    riddles_df = export_riddles_to_excel()
    st.write(riddles_df)  # Show data preview
    
    # Download link
    st.download_button(
        label="Download data as Excel",
        data=riddles_df.to_excel(index=False),
        file_name="riddles_export.xlsx",
        mime="application/vnd.ms-excel"
    )
