import streamlit as st
import requests
import time
import imaplib
import email
from email.header import decode_header

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AI Spam Classifier | Premium",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- INITIALIZE SESSION STATE ---
if 'fetched_emails' not in st.session_state:
    st.session_state.fetched_emails = []
if 'email_content' not in st.session_state:
    st.session_state.email_content = ""

# --- IMAP FETCHING FUNCTION ---
def fetch_recent_emails(imap_server, email_addr, app_password, limit=5):
    try:
        # Connect to IMAP server using SSL
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_addr, app_password)
        mail.select("inbox")

        # Search for all emails
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            return []

        email_ids = messages[0].split()
        if not email_ids:
            return []
            
        recent_ids = email_ids[-limit:]  # Get the last 'limit' emails
        recent_ids.reverse()  # Newest first

        fetched_emails = []

        for e_id in recent_ids:
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    # Parse bytes to Message object
                    msg = email.message_from_bytes(response[1])
                    
                    # Decode the email subject
                    subject = "No Subject"
                    if msg["Subject"]:
                        decoded = decode_header(msg["Subject"])
                        subject_parts = []
                        for sub, encoding in decoded:
                            if isinstance(sub, bytes):
                                subject_parts.append(sub.decode(encoding if encoding else "utf-8", errors='ignore'))
                            else:
                                subject_parts.append(str(sub))
                        subject = "".join(subject_parts)
                    
                    # Extract email body (plain text preferred)
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                payload = part.get_payload(decode=True)
                                if payload:
                                    body = payload.decode(errors='ignore')
                                    break
                    else:
                        content_type = msg.get_content_type()
                        payload = msg.get_payload(decode=True)
                        if payload and (content_type == "text/plain" or content_type == "text/html"):
                            body = payload.decode(errors='ignore')

                    # Fallback cleanups
                    body_text = body.strip() if body else "Empty body content."
                    fetched_emails.append({
                        "subject": subject,
                        "body": body_text
                    })

        mail.logout()
        return fetched_emails
    except Exception as e:
        raise Exception(f"Failed to connect or fetch: {str(e)}")

# --- CALLBACKS ---
def on_email_select():
    # Find selected email and populate it
    subj = st.session_state.selected_subject
    for e in st.session_state.fetched_emails:
        if e['subject'] == subj:
            st.session_state.email_content = e['body']
            break

# --- CUSTOM CSS ---
def local_css():
    st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp {
        background-color: #0B0F19;
        background-image: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,0.2) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,0.2) 0, transparent 50%);
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Glassmorphism Card Design */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-top: 1rem;
        margin-bottom: 2rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 50%, #F472B6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    .subtitle {
        color: #94A3B8;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
        letter-spacing: 0.01em;
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
        color: #F8FAFC !important;
        border-radius: 12px;
        padding: 1.2rem;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        line-height: 1.6;
    }
    
    .stTextArea textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
        background-color: rgba(15, 23, 42, 0.8) !important;
    }
    
    /* Character Counter */
    .char-counter {
        text-align: right;
        color: #64748B;
        font-size: 0.85rem;
        margin-top: -12px;
        margin-bottom: 20px;
        font-weight: 500;
    }
    
    /* Primary Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 20px 25px -5px rgba(124, 58, 237, 0.4);
        background: linear-gradient(135deg, #4338CA 0%, #6D28D9 100%);
        color: white;
    }
    
    /* Result Cards */
    .result-card {
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-top: 2rem;
        animation: scaleIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        opacity: 0;
        transform: scale(0.9);
    }
    
    .spam-result {
        background: linear-gradient(145deg, rgba(153, 27, 27, 0.8), rgba(127, 29, 29, 0.6));
        border: 1px solid rgba(248, 113, 113, 0.3);
        box-shadow: 0 20px 25px -5px rgba(153, 27, 27, 0.3);
        backdrop-filter: blur(8px);
    }
    
    .spam-result h2 { color: #FECACA !important; font-size: 2.2rem; margin-bottom: 0.5rem; }
    .spam-result p { color: #FCA5A5; font-size: 1.1rem; margin: 0; }
    
    .ham-result {
        background: linear-gradient(145deg, rgba(22, 101, 52, 0.8), rgba(20, 83, 45, 0.6));
        border: 1px solid rgba(74, 222, 128, 0.3);
        box-shadow: 0 20px 25px -5px rgba(22, 101, 52, 0.3);
        backdrop-filter: blur(8px);
    }
    
    .ham-result h2 { color: #D1FAE5 !important; font-size: 2.2rem; margin-bottom: 0.5rem; }
    .ham-result p { color: #6EE7B7; font-size: 1.1rem; margin: 0; }
    
    /* Custom Styling for Expander */
    .streamlit-expanderHeader {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Animations */
    @keyframes scaleIn {
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Custom Footer */
    .custom-footer {
        text-align: center;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: #64748B;
        font-size: 0.9rem;
    }
    
    .custom-footer a {
        color: #8B5CF6;
        text-decoration: none;
        transition: color 0.2s;
    }
    
    .custom-footer a:hover {
        color: #A78BFA;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# --- MAIN CONTENT ---
st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <h1 class='gradient-text'>📧 AI Email Spam Classifier</h1>
        <p class='subtitle'>Powered by Advanced Natural Language Processing</p>
    </div>
""", unsafe_allow_html=True)


# --- EMAIL INBOX CONNECT EXPANDER ---
with st.expander("🔌 Connect to Live Email Inbox (IMAP)"):
    st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Fetch recent emails directly from your inbox to analyze them seamlessly.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        imap_server = st.text_input("IMAP Server", value="imap.gmail.com", help="e.g. imap.gmail.com, imap.mail.yahoo.com")
        email_addr = st.text_input("Email Address", placeholder="your_email@gmail.com")
    with col2:
        imap_port = st.number_input("IMAP Port", value=993, min_value=1, max_value=65535)
        app_password = st.text_input("App Password", type="password", help="If using Gmail, generate a 16-character App Password from Google Account Security. Do not use your primary password.")

    if st.button("Fetch Recent Emails 📩", use_container_width=True):
        if not email_addr or not app_password:
            st.warning("⚠️ Please provide both Email Address and App Password to connect.")
        else:
            with st.spinner("Connecting and retrieving emails..."):
                try:
                    emails = fetch_recent_emails(imap_server, email_addr, app_password)
                    if emails:
                        st.session_state.fetched_emails = emails
                        st.session_state.email_content = emails[0]['body'] # Prefill with first email
                        st.success(f"✅ Successfully fetched {len(emails)} emails!")
                    else:
                        st.warning("🔍 Connection successful, but no emails were found in the inbox.")
                except Exception as e:
                    st.error(f"❌ Connection Failed: {str(e)}")

# Selectbox if emails have been successfully fetched
if st.session_state.fetched_emails:
    st.markdown("<h4 style='color: #E2E8F0; margin-top: 1.5rem;'>Select Fetched Email:</h4>", unsafe_allow_html=True)
    selected_subject = st.selectbox(
        "Select Subject",
        options=[e['subject'] for e in st.session_state.fetched_emails],
        key="selected_subject",
        on_change=on_email_select,
        label_visibility="collapsed"
    )

# --- TEXT ANALYZER SECTION ---
st.markdown("<h4 style='color: #E2E8F0; margin-top: 1.5rem;'>Message Content:</h4>", unsafe_allow_html=True)
message = st.text_area(
    "Email Content",
    value=st.session_state.email_content,
    height=220,
    placeholder="Paste your email content here, or select a fetched email above...",
    label_visibility="collapsed",
    key="email_text_area"
)

# Sync manual text area typing back to session state to prevent loss on rerun
st.session_state.email_content = message

# Character Counter dynamically updated
char_count = len(message)
st.markdown(f"<div class='char-counter'>{char_count} characters</div>", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/predict"

if st.button("Predict ⚡", use_container_width=True):
    if not message.strip():
        st.warning("⚠️ Please enter email content or load one from your inbox before predicting.")
    else:
        with st.spinner("Analyzing linguistic patterns..."):
            # Simulated delay for a premium UX feel (model inference time)
            time.sleep(1.2) 
            
            try:
                payload = {"message": message}
                headers = {"Content-Type": "application/json"}
                
                # API Call to FastAPI
                response = requests.post(API_URL, json=payload, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    result = response.json()
                    prediction = result.get("prediction", "")
                    
                    if prediction.lower() == "spam":
                        st.markdown("""
                            <div class="result-card spam-result">
                                <h2>🚨 SPAM DETECTED</h2>
                                <p>High probability of malicious, promotional, or fraudulent content.</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                            <div class="result-card ham-result">
                                <h2>✅ CLEAN MESSAGE</h2>
                                <p>This message appears safe, legitimate, and clear.</p>
                            </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                else:
                    st.error(f"❌ Server Error: {response.status_code}. The AI model is currently unavailable.")
            
            except requests.exceptions.ConnectionError:
                st.error("🔌 Connection Refused: Ensure the FastAPI backend is running at http://127.0.0.1:8000")
            except requests.exceptions.Timeout:
                st.error("⏳ Timeout: The model inference took too long. Please try again.")
            except Exception as e:
                st.error(f"⚠️ System Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

