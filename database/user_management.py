import sqlite3
import hashlib
import os
# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def user_registration(username, password):
    # Define the database path
    db_path = os.path.join(os.path.dirname(__file__), 'login.db')
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Ensure the users table exists
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        number INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending'
    )
    ''')
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Insert the new user into the users table
    try:
        c.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, hashed_password))
        
        # Commit the transaction
        conn.commit()
        conn.close()
        
        # Return success message
        return "User registered successfully."
        
    except sqlite3.IntegrityError:
        # Handle cases where the username already exists (due to UNIQUE constraint)
        conn.close()
        return "Username already exists. Please choose another one."
def login_check(username, password):
    # Define the database path
    db_path = os.path.join(os.path.dirname(__file__), 'login.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Hash the input password
    hashed_password = hash_password(password)
    
    # Check if the username and password match any user
    c.execute('SELECT status FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    result = c.fetchone()
    
    conn.close()

    # Return different responses based on the user status
    if result:
        status = result[0]
        if status == 'active':
            return "Login successful"
        elif status == 'pending':
            return "Your account is pending approval by an admin."
        else:
            return "Your account has been rejected."
    else:
        return "Incorrect Username/Password"

# Function to get pending users
def get_pending_users():
 
    db_path = os.path.join(os.path.dirname(__file__), 'login.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('SELECT username FROM users WHERE status = ?', ('pending',))
    pending_users = c.fetchall()
    conn.commit()
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
        c.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()
