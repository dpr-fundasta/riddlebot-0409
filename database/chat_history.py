import os
import sqlite3
import pandas as pd

# Function to export the database contents to an Excel file
def export_to_excel(excel_filename):

    db_path = os.path.join(os.path.dirname(__file__), 'quiz.db')
    conn = sqlite3.connect(db_path)
    
    # Use pandas to read the table and export to Excel
    df = pd.read_sql_query("SELECT * FROM quiz_data", conn)
    
    # Write the DataFrame to an Excel file
    df.to_excel(excel_filename, index=False)  # Export without the DataFrame index
    
    conn.close()


# Function to add data to the database (note that number is auto-incremented, so it is not provided)
def add_data(username, model, question, correct_answer, user_answer, llm_response, reasoning, llm_hint):
    db_path = os.path.join(os.path.dirname(__file__), 'quiz.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Insert data into the table without specifying 'number', as it auto-increments
    c.execute('''
    INSERT INTO quiz_data (username, model, question, correct_answer, user_answer, llm_response, reasoning, llm_hint)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (username, model, question, correct_answer, user_answer, llm_response, reasoning, llm_hint))
    
    conn.commit()
    conn.close()
