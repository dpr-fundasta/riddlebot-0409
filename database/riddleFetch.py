import sqlite3
import os
import random
import streamlit as st

# Function to get a database connection
def get_db_connection():

    db_path = os.path.join(os.path.dirname(__file__), 'riddles.db')
    conn = sqlite3.connect(db_path)
    return conn

def add_riddle(question, correct_answer):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert the data into the table
    cursor.execute('''
        INSERT INTO riddles (question, correct_answer)
        VALUES (?, ?);
    ''', (question, correct_answer))

    # Commit the changes to the database
    conn.commit()
    conn.close()

def fetch_random_riddle():
    st.session_state.qcount += 1
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the total number of rows in the table
    cursor.execute('SELECT COUNT(*) FROM riddles')
    row_count = cursor.fetchone()[0]
    
    if row_count == 0:
        conn.close()
        return None  # No data available

    # Get a random row number
    random_row_number = random.randint(0, row_count - 1)  # OFFSET starts at 0

    # Retrieve the random row from the table
    cursor.execute('''
        SELECT question, correct_answer
        FROM riddles
        LIMIT 1 OFFSET ?
    ''', (random_row_number,))

    # Fetch the result
    result = cursor.fetchone()
    conn.close()

    if result:
        # Return the result as a dictionary
        return {
            "question": result[0],
            "correct_answer": result[1]
            }
    else:
        return None

