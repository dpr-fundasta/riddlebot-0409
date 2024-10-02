import streamlit as st
from navigation import admin_make_sidebar
from database.user_management import get_pending_users, update_user_status

admin_make_sidebar()

# Ensure that the user is logged in as admin
def check_if_admin(username):
    return username == 'admin'

# Apply custom styling
st.markdown(
    """
    <style>
    body {
        background-image: url("");
        background-size: cover;
        color: #FFFFFF;
    }
    .stTextInput>div>input {
        background-color: #333333;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50; /* Button background color */
        color: white; /* Text color */
        font-size: 16px; /* Font size */
        padding: 10px 20px; /* Padding inside the button */
        border-radius: 8px; /* Rounded corners */
        border: none; /* Remove border */
        cursor: pointer; /* Change cursor to pointer on hover */
        width: 110px; /* Width of the button */
        height: 40px; /* Height of the button */
        margin: 30px; /* Adjust this value to move the button down */
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .button-container {
        display: flex;
        justify-content: flex-start;
        gap: 10px;
    }

    .title {
        font-size: 30px; 
        color: #333333; 
        text-align: center; 
        margin:20px;
        padding:20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Admin page
st.subheader("New Account Requests")
st.caption("Please Accept or Deny The following account requests")
# st.title("Admin User Management")
username = st.session_state.username

# Check if the logged-in user is an admin
if check_if_admin(username):
    # st.subheader("Pending User Registrations")
    
    pending_users = get_pending_users()
    
    if pending_users:
        # Iterate through each pending user
        for user in pending_users:
            # Create three columns for each user: Name, Approve button, Reject button
            col1, col2, col3 = st.columns([2, 1, 1])  # Adjust column widths if needed

            with col1:
                st.write(f"**{user}**")  # Display user name in bold
            
            with col2:
                # Add a unique key to each button to prevent conflict
                if st.button(f"Approve", key=f"approve_{user}"):
                    update_user_status(user, 'active')
                    st.success(f"User {user} has been approved.")

            with col3:
                if st.button(f"Reject", key=f"reject_{user}"):
                    update_user_status(user, 'rejected')
                    st.success(f"User {user} has been rejected.")
    
    else:
        st.write("No pending user registrations.")
else:
    st.warning("You must be an admin to access this page.")
