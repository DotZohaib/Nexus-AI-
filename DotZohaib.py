import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
import time

# Load environment variables
load_dotenv()

# Enhanced Custom CSS for modern dark theme
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #ffffff;
        color: #000000;
    }
    
    /* Welcome Modal Styles */
    .welcome-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }
    
    .welcome-content {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%);
        padding: 3rem;
        border-radius: 20px;
        border: 1px solid #3d3d5c;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        text-align: center;
        max-width: 500px;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        color: #a0a0a0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Header Styles */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        color: #a0a0a0;
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    /* User Info Panel */
    .user-info {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #3d3d5c;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .user-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
    }
    
    .user-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .user-stats {
        color: #a0a0a0;
        font-size: 0.9rem;
    }
    
    /* Sidebar Enhancements */
    .sidebar .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .sidebar .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat Message Styles */
    .chat-message {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 15px;
        animation: fadeIn 0.5s ease-in;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin-left: 2rem;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%);
        border: 1px solid #3d3d5c;
        margin-right: 2rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%) !important;
        border: 1px solid #3d3d5c !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Chat History Styling */
    .chat-item {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%);
        border: 1px solid #3d3d5c;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .chat-item:hover {
        transform: translateX(5px);
        border-color: #667eea;
    }
    
    /* Metrics Styling */
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d42 100%);
        border: 1px solid #3d3d5c;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        color: #a0a0a0;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .icon_size{
        font-size: 2.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def configure_gemini():
    """Configure Gemini API and return model"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ API Key Not Configured")
        st.info("Please add your GEMINI_API_KEY to your .env file")
        return None
    
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        st.error(f"🔴 Initialization Error: {str(e)}")
        return None

# Enhanced chat storage functions
def load_user_chats(username):
    """Load chats for specific user"""
    try:
        with open(f'chats_{username}.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_user_chats(username, chats):
    """Save chats for specific user"""
    with open(f'chats_{username}.json', 'w') as f:
        json.dump(chats, f, indent=2)

def load_users():
    """Load all registered users"""
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    """Save user registry"""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)

def register_user(username):
    """Register a new user"""
    users = load_users()
    if username not in users:
        users[username] = {
            'created_at': datetime.now().isoformat(),
            'total_chats': 0,
            'total_messages': 0,
            'last_active': datetime.now().isoformat()
        }
        save_users(users)
    return users[username]

def update_user_stats(username):
    """Update user statistics"""
    users = load_users()
    if username in users:
        chats = load_user_chats(username)
        users[username]['total_chats'] = len(chats)
        users[username]['total_messages'] = sum(len(chat['messages']) for chat in chats)
        users[username]['last_active'] = datetime.now().isoformat()
        save_users(users)

def create_new_chat(username):
    """Create a new chat for user"""
    st.session_state.current_chat = {
        'id': datetime.now().strftime("%Y%m%d%H%M%S"),
        'title': 'New Chat',
        'messages': [],
        'created_at': datetime.now().isoformat(),
        'username': username
    }

def generate_chat_title(prompt):
    """Generate a smart chat title"""
    if len(prompt) <= 40:
        return prompt
    
    # Try to find a meaningful title from the first few words
    words = prompt.split()[:6]
    title = ' '.join(words)
    return title + "..." if len(title) < len(prompt) else title

def generate_response(model, question, username):
    """Generate response using Gemini model with user context"""
    try:
        # Add some context about the user
        enhanced_prompt = f"User {username} asks: {question}"
        
        with st.spinner("🌟 Generating intelligent response..."):
            response = model.generate_content(enhanced_prompt)
            return response.text
    except Exception as e:
        st.error(f"🚨 Generation Error: {str(e)}")
        return None

def display_user_info(username):
    """Display user information panel"""
    users = load_users()
    user_data = users.get(username, {})
    
    # User avatar (first letter of username)
    avatar_letter = username[0].upper() if username else "U"
    
    st.markdown(f"""
    <div class="user-info">
        <div class="user-avatar">{avatar_letter}</div>
        <div class="user-name">Welcome, {username}!</div>
        <div class="user-stats">
            {user_data.get('total_chats', 0)} Chats • 
            {user_data.get('total_messages', 0)} Messages
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Nexus AI - Advanced Chat Interface",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    inject_custom_css()

    # User Authentication
    if 'username' not in st.session_state:
        st.session_state.username = None
        st.session_state.show_welcome = True

    # Show welcome modal for new sessions
    if st.session_state.get('show_welcome', False):
        st.session_state.show_welcome = False

    # Username input if not logged in
    if not st.session_state.username:
        st.markdown("""
        <div class="main-header">
            <div class="icon_size">🚀 <span  class="app-title">Nexus AI</span></div>
            <div class="app-subtitle">Advanced AI Chat Interface</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 👋 Enter Your Name to Continue")
            username_input = st.text_input(
                "Your Name", 
                placeholder="Enter your name...",
                key="username_input"
            )
            
            if st.button("🚀 Start Chat", use_container_width=True):
                if username_input.strip():
                    st.session_state.username = username_input.strip()
                    register_user(st.session_state.username)
                    st.rerun()
                else:
                    st.error("Please enter your name to continue!")
        return

    # Initialize session state for authenticated user
    username = st.session_state.username
    
    if 'model' not in st.session_state:
        st.session_state.model = configure_gemini()
    
    if 'user_chats' not in st.session_state:
        st.session_state.user_chats = load_user_chats(username)
    
    if 'current_chat' not in st.session_state:
        create_new_chat(username)
    
    if 'editing_chat' not in st.session_state:
        st.session_state.editing_chat = None

    # Sidebar for user info and chat history
    with st.sidebar:
        # User info
        display_user_info(username)
        
        # User stats
        users = load_users()
        user_data = users.get(username, {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{user_data.get('total_chats', 0)}</div>
                <div class="metric-label">Total Chats</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{user_data.get('total_messages', 0)}</div>
                <div class="metric-label">Messages</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Chat management
        st.markdown("### 💬 Your Chats")
        
        # New Chat button
        if st.button("➕ New Chat", use_container_width=True):
            create_new_chat(username)
            st.session_state.editing_chat = None
            st.rerun()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        # Chat list
        if st.session_state.user_chats:
            for chat in reversed(st.session_state.user_chats):
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        if st.button(
                            f"💭 {chat['title']}",
                            key=f"btn_{chat['id']}",
                            use_container_width=True,
                            help=f"Created: {chat.get('created_at', 'Unknown')}"
                        ):
                            st.session_state.current_chat = chat.copy()
                            st.session_state.editing_chat = None
                            st.rerun()
                    with col2:
                        if st.button("✏️", key=f"edit_{chat['id']}", help="Edit chat"):
                            st.session_state.editing_chat = chat['id']
                            st.rerun()
        else:
            st.info("No chats yet. Start a conversation!")

    # Main chat interface
    st.markdown(f"""
    <div class="main-header">
        <div class="icon_size">🤖 <span class="app-title">Nexus AI</span></div>
        <div class="app-subtitle">Conversation with {username}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Edit mode handling
    if st.session_state.editing_chat:
        edited_chat = next(
            (chat for chat in st.session_state.user_chats 
             if chat['id'] == st.session_state.editing_chat), None)
        
        if edited_chat:
            st.markdown("### ✍️ Edit Chat")
            new_title = st.text_input("Chat Title", value=edited_chat['title'])
            
            # Message editing
            new_messages = []
            for i, msg in enumerate(edited_chat['messages']):
                st.markdown(f"**Message {i+1}:**")
                col1, col2 = st.columns([1, 4])
                with col1:
                    role = st.selectbox(
                        "Role",
                        ["user", "assistant"],
                        index=0 if msg['role'] == "user" else 1,
                        key=f"role_{i}"
                    )
                with col2:
                    content = st.text_area(
                        "Content",
                        value=msg['content'],
                        key=f"content_{i}",
                        height=100
                    )
                new_messages.append({"role": role, "content": content})
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("💾 Save Changes"):
                    edited_chat['title'] = new_title
                    edited_chat['messages'] = new_messages
                    save_user_chats(username, st.session_state.user_chats)
                    update_user_stats(username)
                    st.success("Chat updated successfully!")
                    st.session_state.editing_chat = None
                    st.rerun()
            with col2:
                if st.button("❌ Cancel"):
                    st.session_state.editing_chat = None
                    st.rerun()
    else:
        # Display current chat messages
        if st.session_state.current_chat['messages']:
            for msg in st.session_state.current_chat['messages']:
                if msg['role'] == 'user':
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(f"**{username}:** {msg['content']}")
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(f"**Nexus AI:** {msg['content']}")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #a0a0a0;">
                <h3>👋 Start a new conversation!</h3>
                <p>Ask me anything and I'll help you with intelligent responses.</p>
            </div>
            """, unsafe_allow_html=True)

        # Chat input
        question = st.chat_input("💡 Type your message here...")
        
        if question and st.session_state.model:
            # Add user message
            st.session_state.current_chat['messages'].append({
                "role": "user",
                "content": question
            })
            
            # Generate AI response
            response = generate_response(st.session_state.model, question, username)
            
            if response:
                # Add AI response
                st.session_state.current_chat['messages'].append({
                    "role": "assistant",
                    "content": response
                })
                
                # Update chat title if first message
                if len(st.session_state.current_chat['messages']) == 2:
                    st.session_state.current_chat['title'] = generate_chat_title(question)
                
                # Auto-save chat
                chat_exists = any(
                    chat['id'] == st.session_state.current_chat['id'] 
                    for chat in st.session_state.user_chats
                )
                
                if not chat_exists:
                    st.session_state.user_chats.append(st.session_state.current_chat.copy())
                else:
                    # Update existing chat
                    for i, chat in enumerate(st.session_state.user_chats):
                        if chat['id'] == st.session_state.current_chat['id']:
                            st.session_state.user_chats[i] = st.session_state.current_chat.copy()
                            break
                
                save_user_chats(username, st.session_state.user_chats)
                update_user_stats(username)
                st.rerun()

        # Save button for current chat
        if st.session_state.current_chat['messages']:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                if st.button("💾 Save Chat", use_container_width=True):
                    chat_exists = any(
                        chat['id'] == st.session_state.current_chat['id'] 
                        for chat in st.session_state.user_chats
                    )
                    
                    if not chat_exists:
                        st.session_state.user_chats.append(st.session_state.current_chat.copy())
                        save_user_chats(username, st.session_state.user_chats)
                        update_user_stats(username)
                        st.success("Chat saved successfully!")
                    else:
                        st.info("Chat is already saved!")

if __name__ == "__main__":
    main()