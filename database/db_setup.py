import sqlite3
import random

import sqlite3

import pandas as pd
# # Function to get a database connection
# def get_db_connection():
#     conn = sqlite3.connect(r'D:\FundastA\riddlebot\database\riddles.db')
#     return conn

# # Function to create the riddles table
# def create_riddles_table():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Create the riddles table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS riddles (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             question TEXT NOT NULL,
#             correct_answer TEXT NOT NULL,
#             reasoning_of_answer TEXT NOT NULL
#         );
#     ''')

#     # Commit the changes to the database
#     conn.commit()
#     conn.close()

# # Function to add a riddle to the database
# def add_riddle(question, correct_answer, reasoning_of_answer):
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     # Insert the data into the table
#     cursor.execute('''
#         INSERT INTO riddles (question, correct_answer, reasoning_of_answer)
#         VALUES (?, ?, ?);
#     ''', (question, correct_answer, reasoning_of_answer))

#     # Commit the changes to the database
#     conn.commit()
#     conn.close()

# def get_row_count():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Query to get the number of rows in the table
#     cursor.execute('SELECT COUNT(*) FROM riddles')
#     row_count = cursor.fetchone()[0]
    
#     conn.close()
#     return row_count
    
# # Function to fetch a random riddle from the database
# def fetch_random_riddle():
#     st.session_state.qcount += 1
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Get the total number of rows in the table
#     cursor.execute('SELECT COUNT(*) FROM riddles')
#     row_count = cursor.fetchone()[0]
    
#     if row_count == 0:
#         conn.close()
#         return None  # No data available

#     # Get a random row number
#     random_row_number = random.randint(0, row_count - 1)  # OFFSET starts at 0

#     # Retrieve the random row from the table
#     cursor.execute('''
#         SELECT question, correct_answer, reasoning_of_answer
#         FROM riddles
#         LIMIT 1 OFFSET ?
#     ''', (random_row_number,))

#     # Fetch the result
#     result = cursor.fetchone()
#     conn.close()

#     if result:
#         # Return the result as a dictionary
#         return {
#             "question": result[0],
#             "correct_answer": result[1],
#             "reasoning_of_answer": result[2]
#         }
#     else:
#         return None

# # Example usage
# if __name__ == "__main__":
#     # # Create the table (uncomment to run the first time)
#     # create_riddles_table()

#     # # Add a riddle to the database
#     # # add_riddle("What has to be broken before you can use it?", "Egg", "An egg must be broken before you can cook with it.")

#     # # Fetch a random riddle
#     # riddle = fetch_random_riddle()
#     # print(riddle)
#     row_count = get_row_count()
#     print(f'Number of rows in the riddles table: {row_count}')



# import sqlite3

# # Connect to the SQLite database
# connection = sqlite3.connect(r'D:\FundastA\riddlebot\database\riddles.db')  # Update the path to your database file
# cursor = connection.cursor()

# # Query to get the table structure
# cursor.execute("PRAGMA table_info(riddles);")

# # Fetch and print the table structure
# columns = cursor.fetchall()
# for column in columns:
#     print(f"Column Name: {column[1]}, Type: {column[2]}, Not Null: {column[3]}, Default Value: {column[4]}, Primary Key: {column[5]}")

# # Close the connection
# connection.close()




# import sqlite3

# # Connect to the SQLite database
# connection = sqlite3.connect(r'D:\FundastA\riddlebot\database\riddles.db')  # Update the path to your database file
# cursor = connection.cursor()

# # Step 1: Create a new table without the 'reasoning_of_answer' column
# cursor.execute('''
# CREATE TABLE riddles_new (
#     id INTEGER PRIMARY KEY,
#     question TEXT NOT NULL,
#     correct_answer TEXT NOT NULL
# );
# ''')

# # Step 2: Copy data from the old table to the new table
# cursor.execute('''
# INSERT INTO riddles_new (id, question, correct_answer)
# SELECT id, question, correct_answer FROM riddles;
# ''')

# # Step 3: Drop the old table
# cursor.execute('DROP TABLE riddles;')

# # Step 4: Rename the new table to the old table's name
# cursor.execute('ALTER TABLE riddles_new RENAME TO riddles;')

# # Commit the changes and close the connection
# connection.commit()
# connection.close()

import os

# Function to create the database and table if it doesn't already exist
def create_database(db_name='quiz.db'):
    db_path = os.path.join(os.path.dirname(__file__), 'quiz.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Create table with auto-incrementing primary key
    c.execute('''
    CREATE TABLE IF NOT EXISTS quiz_data (
        number INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        model TEXT,
        question TEXT,
        correct_answer TEXT,
        user_answer TEXT,
        llm_response TEXT,
        reasoning TEXT,
        llm_hint TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Function to export the database contents to an Excel file
def export_to_excel(excel_filename='quiz_data.xlsx', db_name='quiz.db'):
    db_path = os.path.join(os.path.dirname(__file__), 'quiz.db')
    conn = sqlite3.connect(db_path)
    
    # Use pandas to read the table and export to Excel
    df = pd.read_sql_query("SELECT * FROM quiz_data", conn)
    
    # Write the DataFrame to an Excel file
    df.to_excel(excel_filename, index=False)  # Export without the DataFrame index
    
    conn.close()


# Function to add data to the database (note that number is auto-incremented, so it is not provided)
def add_data(username, model, question, correct_answer, user_answer, llm_response, reasoning, llm_hint, db_name='quiz.db'):
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

if __name__ == '__main__':
    # create_database()
     # Add example data (no need to specify 'number' as it auto-increments)
    # add_data("What is the capital of France?", "Paris", "London", "Paris is the capital", "Hint: It's a European city.")
    # add_data("What is 2 + 2?", "4", "3", "Correct answer is 4", "Hint: Think basic math.")
    export_to_excel('quiz_data.xlsx')
    #  add_data(
    #     "jane_smith", "gpt-4", 
    #     "What is 2 + 2?", 
    #     "4", 
    #     "3", 
    #     "Correct answer is 4", 
    #     "User made a simple arithmetic mistake", 
    #     "Hint: Think basic math."
    # )
