import sqlite3
import hashlib
import os
# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function for new user registration
def user_registration(username, password):
    # conn = sqlite3.connect('riddles.db')
    
    db_path = os.path.join(os.path.dirname(__file__), 'login.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Ensure the users table exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL PRIMARY KEY,
        password TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending'
    )
    ''')
    
    # Check if the username already exists
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    if c.fetchone():
        conn.close()
        return False  # Username already exists
    
    # Hash the user's password before storing it
    hashed_password = hash_password(password)
    
    # Insert the new user data with status 'pending'
    c.execute('INSERT INTO users (username, password, status) VALUES (?, ?, ?)', (username, hashed_password, 'pending'))
    conn.commit()
    conn.close()
    
    return True  # Registration successful

# Function to check login credentials
def login_check(username, password):
     
    db_path = os.path.join(os.path.dirname(__file__), 'login.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Hash the input password
    hashed_password = hash_password(password)
    
    # Query the database for a matching user
    c.execute('SELECT * FROM users WHERE username = ? AND password = ? AND status = ?', (username, hashed_password, 'active'))
    result = c.fetchone()
    
    conn.close()
    
    # If a match is found, return True, else return False
    return bool(result)

# Function to get pending users
def get_pending_users():
 
    db_path = os.path.join(os.path.dirname(__file__), 'login.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('SELECT username FROM users WHERE status = ?', ('pending',))
    pending_users = c.fetchall()
    
    conn.close()
    
    return [user[0] for user in pending_users]

# Function to update user status
def update_user_status(username, status):
 
    db_path = os.path.join(os.path.dirname(__file__), 'login.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    if status == 'active':
        c.execute('UPDATE users SET status = ? WHERE username = ?', (status, username))
    elif status == 'rejected':
        c.execute('DELETE FROM users WHERE username = ?', (username))
    conn.commit()
    conn.close()
