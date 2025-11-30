import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import json
import os
import time

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="YoKA KNUST Information System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.3rem;
        color: #2e86ab;
        border-bottom: 2px solid #2e86ab;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        color: #155724;
        margin: 1rem 0;
    }
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        color: #721c24;
        margin: 1rem 0;
    }
    .stButton button {
        background-color: #2e86ab;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
        width: 100%;
    }
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
    }
    .admin-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2e86ab;
    }
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .section-header {
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

class AuthenticationSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.initialize_users()
    
    def initialize_users(self):
        """Initialize users file with default admin if it doesn't exist"""
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "role": "admin",
                    "email": "admin@yoka.knust.edu.gh"
                }
            }
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=4)
    
    def hash_password(self, password):
        """Hash a password for storing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, hashed):
        """Verify a stored password against one provided"""
        return self.hash_password(password) == hashed
    
    def add_user(self, username, password, role="user", email=""):
        """Add a new user"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username in users:
                return False, "Username already exists"
            
            users[username] = {
                "password": self.hash_password(password),
                "role": role,
                "email": email
            }
            
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=4)
            
            return True, "User created successfully"
        except Exception as e:
            return False, f"Error creating user: {str(e)}"
    
    def authenticate(self, username, password):
        """Authenticate a user"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username in users and self.verify_password(password, users[username]["password"]):
                return True, users[username]["role"]
            else:
                return False, "Invalid credentials"
        except Exception as e:
            return False, f"Authentication error: {str(e)}"
    
    def get_users(self):
        """Get all users (admin only)"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}

class YokaInformationSystem:
    def __init__(self):
        self.data_file = "yoka_data.csv"
        self.auth_system = AuthenticationSystem()
        self.initialize_data()
    
    def initialize_data(self):
        """Initialize the CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.data_file):
            columns = [
                'timestamp', 'official_name', 'date_of_birth', 'age', 'phone_numbers', 
                'email', 'interests_skills', 'on_campus_business', 'business_name_type',
                'father_name', 'father_phone', 'father_church_member', 'father_branch',
                'father_position', 'father_occupation',
                'mother_name', 'mother_phone', 'mother_church_member', 'mother_branch',
                'mother_position', 'mother_occupation',
                'guardian_name', 'guardian_phone', 'guardian_church_member', 'guardian_branch',
                'guardian_position', 'guardian_occupation',
                'school_name', 'program', 'current_class', 'hostel_hall', 'room_number',
                'church_branch', 'branch_pastor', 'shepherd_group', 'yoka_position',
                'submitted_by'
            ]
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.data_file, index=False)
    
    def save_data(self, data):
        """Save form data to CSV"""
        df = pd.DataFrame([data])
        # Use mode='a' to append to existing file
        if os.path.exists(self.data_file):
            df.to_csv(self.data_file, mode='a', header=False, index=False)
        else:
            df.to_csv(self.data_file, index=False)
    
    def load_data(self):
        """Load existing data from CSV"""
        try:
            if os.path.exists(self.data_file):
                return pd.read_csv(self.data_file)
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()

def login_page():
    """Display login page"""
    st.markdown('<h1 class="main-header">🔐 YoKA KNUST Login</h1>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        st.subheader("Please Login to Continue")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            login_btn = st.button("Login", use_container_width=True)
            if login_btn:
                if username and password:
                    with st.spinner("Authenticating..."):
                        time.sleep(0.5)  # Small delay for better UX
                        success, message = yoka_system.auth_system.authenticate(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.role = message
                            st.success("Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.error("Please enter both username and password")
        
        with col2:
            if st.button("Clear", use_container_width=True):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Admin registration section
        if 'logged_in' not in st.session_state:
            with st.expander("Admin Registration (First Time Setup)"):
                st.info("Use this section to create the first admin account if needed.")
                new_admin_user = st.text_input("New Admin Username", key="new_admin_user")
                new_admin_password = st.text_input("New Admin Password", type="password", key="new_admin_pass")
                new_admin_email = st.text_input("Admin Email", key="new_admin_email")
                
                if st.button("Create Admin Account", key="create_admin"):
                    if new_admin_user and new_admin_password:
                        success, message = yoka_system.auth_system.add_user(
                            new_admin_user, new_admin_password, "admin", new_admin_email
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.error("Please fill all fields")

def user_management():
    """User management section for admins"""
    st.markdown('<div class="admin-section">', unsafe_allow_html=True)
    st.subheader("👥 User Management")
    
    # Add new user
    with st.form("add_user_form"):
        st.write("Add New User")
        new_username = st.text_input("Username", key="new_username")
        new_password = st.text_input("Password", type="password", key="new_password")
        new_role = st.selectbox("Role", ["user", "admin"], key="new_role")
        new_email = st.text_input("Email", key="new_email")
        
        if st.form_submit_button("Add User"):
            if new_username and new_password:
                success, message = yoka_system.auth_system.add_user(
                    new_username, new_password, new_role, new_email
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
            else:
                st.error("Please fill all required fields")
    
    # Show existing users
    st.subheader("Existing Users")
    users = yoka_system.auth_system.get_users()
    if users:
        users_df = pd.DataFrame([
            {"Username": user, "Role": info["role"], "Email": info.get("email", "")}
            for user, info in users.items()
        ])
        st.dataframe(users_df, use_container_width=True)
    else:
        st.info("No users found.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main_application():
    """Main application after login"""
    # Header with user info
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f'<h1 class="main-header">📚 YoKA KNUST Information System</h1>', unsafe_allow_html=True)
    with col2:
        st.write(f"Welcome, **{st.session_state.username}**")
    with col3:
        if st.button("Logout"):
            for key in ['logged_in', 'username', 'role']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Admin features
    if st.session_state.role == "admin":
        with st.sidebar:
            st.header("Admin Panel")
            if st.button("User Management"):
                st.session_state.show_user_management = not st.session_state.get('show_user_management', False)
            
            if st.session_state.get('show_user_management', False):
                user_management()
    
    # Create form
    with st.form("yoka_info_form", clear_on_submit=True):
        st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
        
        # Personal Information Section
        col1, col2 = st.columns(2)
        
        with col1:
            official_name = st.text_input("Official Name *", placeholder="Enter your full official name")
            date_of_birth = st.date_input("Date of Birth *", min_value=datetime(1900, 1, 1))
            age = st.number_input("Age *", min_value=1, max_value=100, step=1)
            phone_numbers = st.text_input("Active Phone Numbers *", placeholder="e.g., 0241234567, 0207654321")
        
        with col2:
            email = st.text_input("Email Address *", placeholder="your.email@example.com")
            interests_skills = st.text_area("Interests or Skills", placeholder="List your interests, hobbies, or skills")
            on_campus_business = st.radio("Any on campus business? *", ["No", "Yes"])
            
            if on_campus_business == "Yes":
                business_name_type = st.text_input("Business Name/Type", placeholder="Describe your business")
            else:
                business_name_type = ""
        
        # Parents/Guardian Details Section
        st.markdown('<div class="section-header">Parents/Guardian Details</div>', unsafe_allow_html=True)
        
        # Father's Information
        st.subheader("Father's Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            father_name = st.text_input("Father's Name", placeholder="Full name")
            father_phone = st.text_input("Father's Phone Number", placeholder="Phone number")
        
        with col2:
            father_church_member = st.radio("Is he a church member?", ["No", "Yes"], key="father_member")
            if father_church_member == "Yes":
                father_branch = st.text_input("Which branch?", placeholder="Church branch", key="father_branch")
                father_position = st.text_input("Any position (formal or current)", placeholder="Position held", key="father_position")
            else:
                father_branch = ""
                father_position = ""
        
        with col3:
            father_occupation = st.text_input("Occupation", placeholder="Father's occupation", key="father_occupation")
        
        # Mother's Information
        st.subheader("Mother's Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            mother_name = st.text_input("Mother's Name", placeholder="Full name")
            mother_phone = st.text_input("Mother's Phone Number", placeholder="Phone number")
        
        with col2:
            mother_church_member = st.radio("Is she a church member?", ["No", "Yes"], key="mother_member")
            if mother_church_member == "Yes":
                mother_branch = st.text_input("Which branch?", placeholder="Church branch", key="mother_branch")
                mother_position = st.text_input("Any position (formal or current)", placeholder="Position held", key="mother_position")
            else:
                mother_branch = ""
                mother_position = ""
        
        with col3:
            mother_occupation = st.text_input("Occupation", placeholder="Mother's occupation", key="mother_occupation")
        
        # Guardian's Information
        st.subheader("Guardian's Information (If applicable)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            guardian_name = st.text_input("Guardian's Name", placeholder="Full name")
            guardian_phone = st.text_input("Guardian's Phone Number", placeholder="Phone number")
        
        with col2:
            guardian_church_member = st.radio("Is he/she a church member?", ["No", "Yes"], key="guardian_member")
            if guardian_church_member == "Yes":
                guardian_branch = st.text_input("Which branch?", placeholder="Church branch", key="guardian_branch")
                guardian_position = st.text_input("Any position (formal or current)", placeholder="Position held", key="guardian_position")
            else:
                guardian_branch = ""
                guardian_position = ""
        
        with col3:
            guardian_occupation = st.text_input("Occupation", placeholder="Guardian's occupation", key="guardian_occupation")
        
        # Educational Information Section
        st.markdown('<div class="section-header">Educational Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            school_name = st.text_input("Name of School *", placeholder="KNUST")
            program = st.text_input("Program Offered *", placeholder="e.g., Computer Science")
            current_class = st.text_input("Current Class or Level *", placeholder="e.g., Level 300")
        
        with col2:
            hostel_hall = st.text_input("Hostel/Hall", placeholder="e.g., Unity Hall, Republic Hall")
            room_number = st.text_input("Room Number", placeholder="e.g., A45")
        
        # Church Information Section
        st.markdown('<div class="section-header">Church Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            church_branch = st.text_input("Name of Branch *", placeholder="Your church branch")
            branch_pastor = st.text_input("Name of Branch Pastor *", placeholder="Pastor's name")
        
        # YoKA KNUST Information Section
        st.markdown('<div class="section-header">YoKA KNUST Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            shepherd_group = st.text_input("Shepherd Group", placeholder="Your shepherd group")
        
        with col2:
            yoka_position = st.text_input("Any position (formal or current)", placeholder="Position in YoKA")
        
        # Submit button
        submitted = st.form_submit_button("Submit Information")
        
        if submitted:
            # Validate required fields
            required_fields = {
                "Official Name": official_name,
                "Date of Birth": date_of_birth,
                "Age": age,
                "Phone Numbers": phone_numbers,
                "Email": email,
                "School Name": school_name,
                "Program": program,
                "Current Class": current_class,
                "Church Branch": church_branch,
                "Branch Pastor": branch_pastor
            }
            
            missing_fields = [field for field, value in required_fields.items() if not value]
            
            if missing_fields:
                st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
            else:
                # Prepare data for saving
                form_data = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'official_name': official_name,
                    'date_of_birth': date_of_birth.strftime("%Y-%m-%d"),
                    'age': age,
                    'phone_numbers': phone_numbers,
                    'email': email,
                    'interests_skills': interests_skills,
                    'on_campus_business': on_campus_business,
                    'business_name_type': business_name_type,
                    'father_name': father_name,
                    'father_phone': father_phone,
                    'father_church_member': father_church_member,
                    'father_branch': father_branch,
                    'father_position': father_position,
                    'father_occupation': father_occupation,
                    'mother_name': mother_name,
                    'mother_phone': mother_phone,
                    'mother_church_member': mother_church_member,
                    'mother_branch': mother_branch,
                    'mother_position': mother_position,
                    'mother_occupation': mother_occupation,
                    'guardian_name': guardian_name,
                    'guardian_phone': guardian_phone,
                    'guardian_church_member': guardian_church_member,
                    'guardian_branch': guardian_branch,
                    'guardian_position': guardian_position,
                    'guardian_occupation': guardian_occupation,
                    'school_name': school_name,
                    'program': program,
                    'current_class': current_class,
                    'hostel_hall': hostel_hall,
                    'room_number': room_number,
                    'church_branch': church_branch,
                    'branch_pastor': branch_pastor,
                    'shepherd_group': shepherd_group,
                    'yoka_position': yoka_position,
                    'submitted_by': st.session_state.username
                }
                
                # Save data
                yoka_system.save_data(form_data)
                
                # Success message
                st.markdown('<div class="success-message">✅ Information submitted successfully! Thank you for registering with YoKA KNUST.</div>', unsafe_allow_html=True)

    # Data Management Section (for administrators)
    st.sidebar.markdown("---")
    st.sidebar.header("Data Management")
    
    if st.sidebar.checkbox("Show Submitted Data"):
        try:
            data = yoka_system.load_data()
            if not data.empty:
                st.sidebar.dataframe(data)
                
                # Download option
                csv = data.to_csv(index=False)
                st.sidebar.download_button(
                    label="Download Data as CSV",
                    data=csv,
                    file_name="yoka_knust_data.csv",
                    mime="text/csv"
                )
            else:
                st.sidebar.info("No data submitted yet.")
        except Exception as e:
            st.sidebar.error(f"Error loading data: {str(e)}")

# Initialize the system
yoka_system = YokaInformationSystem()

# Main app logic
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
else:
    main_application()