import streamlit as st
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Abhishek | Secure AES Vault", page_icon="🛡️", layout="centered")

# --- PROFESSIONAL "MIDNIGHT" UI STYLING ---
def apply_pro_style():
    st.markdown(
        """
        <style>
        /* Base App Styling - Deep Midnight Blue/Black */
        .stApp {
            background-color: #0d1117;
            background-image: radial-gradient(circle at 2px 2px, #21262d 1px, transparent 0);
            background-size: 32px 32px;
        }

        /* Muted Typography - No pure white to avoid eye strain */
        h1, h2, h3, p, span, label, .stMarkdown {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: #8b949e !important; /* Muted Grey */
        }

        /* Main Title - Soft Silver Gradient */
        .main-title {
            background: linear-gradient(180deg, #f0f6fc, #8b949e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 2.5rem !important;
            margin-bottom: 0px;
        }

        /* Portfolio Branding - Professional Slate Blue */
        .brand-text {
            color: #58a6ff !important; 
            font-weight: 600;
            letter-spacing: 1.2px;
            font-size: 0.8rem;
            text-transform: uppercase;
        }

        /* Quote Styling - Muted Border */
        .quote-container {
            border-left: 3px solid #30363d;
            padding: 12px 20px;
            margin: 25px 0;
            background: rgba(48, 54, 61, 0.2);
            border-radius: 0 8px 8px 0;
            color: #c9d1d9 !important; /* Slightly brighter for readability */
        }

        /* Input Card Styling - Subtle Dark Borders */
        div[data-baseweb="input"] {
            background-color: #0d1117 !important;
            border-radius: 8px !important;
            border: 1px solid #30363d !important;
        }
        
        /* Text Color inside Inputs */
        input {
            color: #c9d1d9 !important;
        }

        /* Button Styling - High Contrast Blue */
        .stButton>button {
            background-color: #238636 !important; /* GitHub Green for "Action" */
            color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: background 0.2s ease !important;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #2ea043 !important;
            border: none !important;
        }

        /* Radio buttons and Upload labels */
        .stRadio label, .stFileUploader label {
            color: #8b949e !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

apply_pro_style()

# --- LOGIC ---
def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

# --- CONTENT ---
st.markdown('<h1 class="main-title">Secure Vault</h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-text">DEVELOPED BY ABHISHEK</p>', unsafe_allow_html=True)

st.markdown(
    '<div class="quote-container">"Guard your digital soul: Secure your files from unauthorized access."</div>', 
    unsafe_allow_html=True
)

# Layout Columns
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("### Configuration")
    password = st.text_input("Master Key", type="password", placeholder="Enter key...")
    mode = st.radio("Mode", ["Encrypt Asset", "Decrypt Asset"])

with col2:
    st.markdown("### File Input")
    uploaded_file = st.file_uploader("Upload Target", help="Processing is handled locally in-browser.")

if uploaded_file and password:
    key = get_key(password)
    file_bytes = uploaded_file.getvalue()
    
    try:
        if "Encrypt" in mode:
            # Process
            filesize = str(len(file_bytes)).zfill(16)
            IV = Random.new().read(16)
            encryptor = AES.new(key, AES.MODE_CBC, IV)
            pad_len = 16 - (len(file_bytes) % 16)
            padded_data = file_bytes + (b' ' * pad_len)
            final_data = filesize.encode('utf-8') + IV + encryptor.encrypt(padded_data)
            
            st.divider()
            st.success("Vault Encryption Successful")
            st.download_button("📥 Download Encrypted Asset", final_data, file_name=f"{uploaded_file.name}.enc")

        else:
            # Process
            filesize = int(file_bytes[:16])
            IV = file_bytes[16:32]
            ciphertext = file_bytes[32:]
            decryptor = AES.new(key, AES.MODE_CBC, IV)
            decrypted_data = decryptor.decrypt(ciphertext)
            final_data = decrypted_data[:filesize]
            
            st.divider()
            st.success("Vault Access Granted")
            st.download_button("📥 Download Original Asset", final_data, file_name=uploaded_file.name.replace(".enc", ""))
            
    except Exception:
        st.error("Authentication Error: Invalid Key or File.")

st.markdown("<br><br><p style='text-align: center; color: #484f58 !important; font-size: 0.75rem;'>AES-256 Bit Encryption | End-to-End Secure Session</p>", unsafe_allow_html=True)
