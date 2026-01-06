import streamlit as st
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Abhishek | Secure AES Vault", 
    page_icon="🛡️", 
    layout="centered"
)

# --- PROFESSIONAL UI STYLING ---
def apply_pro_style():
    st.markdown(
        """
        <style>
        /* Main Background */
        .stApp {
            background-color: #0d1117;
            background-image: radial-gradient(circle at 2px 2px, #21262d 1px, transparent 0);
            background-size: 32px 32px;
        }

        /* Modern Typography */
        h1, h2, h3, p, span, label, .stMarkdown {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
            color: #c9d1d9 !important;
        }

        /* Title Styling */
        .main-title {
            background: linear-gradient(90deg, #ffffff, #8b949e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 2.8rem !important;
            margin-bottom: 5px;
        }

        /* Branding Accent */
        .dev-tag {
            color: #58a6ff !important;
            font-weight: 600;
            letter-spacing: 1.5px;
            font-size: 0.9rem;
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        /* The Quote Box */
        .quote-box {
            border-left: 4px solid #58a6ff;
            padding: 15px 25px;
            margin: 20px 0;
            background: rgba(88, 166, 255, 0.1);
            border-radius: 0 8px 8px 0;
            font-style: italic;
        }

        /* Improved Input Boxes */
        div[data-baseweb="input"] {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            border-radius: 8px !important;
        }

        /* Premium Button */
        .stButton>button {
            background: linear-gradient(180deg, #1f6feb 0%, #1158c7 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 20px !important;
            font-weight: 600 !important;
            width: 100%;
            transition: 0.2s all ease;
        }
        
        .stButton>button:hover {
            opacity: 0.9;
            transform: scale(1.01);
            box-shadow: 0 4px 12px rgba(31, 111, 235, 0.4);
        }

        /* Clean Divider */
        hr { border-top: 1px solid #30363d !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

apply_pro_style()

# --- CORE CRYPTO FUNCTIONS ---
def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

# --- HEADER SECTION ---
st.markdown('<h1 class="main-title">Secure Vault</h1>', unsafe_allow_html=True)
st.markdown('<p class="dev-tag">Developed by Abhishek</p>', unsafe_allow_html=True)

st.markdown(
    '<div class="quote-box">"Guard your digital soul: Secure your files from unauthorized access."</div>', 
    unsafe_allow_html=True
)

# --- USER INTERFACE COLUMNS ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### Configuration")
    password = st.text_input("Master Key", type="password", placeholder="Secret password...")
    mode = st.radio("Operation Mode", ["🔒 Encrypt File", "🔓 Decrypt File"])

with col2:
    st.markdown("### Asset Upload")
    uploaded_file = st.file_uploader("Drop file here", help="Files are processed in-memory for security.")

# --- PROCESSING LOGIC ---
if uploaded_file and password:
    key = get_key(password)
    file_bytes = uploaded_file.getvalue()
    
    try:
        if "Encrypt" in mode:
            # Prepare Metadata
            filesize = str(len(file_bytes)).zfill(16)
            IV = Random.new().read(16)
            encryptor = AES.new(key, AES.MODE_CBC, IV)
            
            # Apply Padding
            pad_len = 16 - (len(file_bytes) % 16)
            padded_data = file_bytes + (b' ' * pad_len)
            
            # Final Construction: Size + IV + Data
            final_data = filesize.encode('utf-8') + IV + encryptor.encrypt(padded_data)
            
            st.divider()
            st.success("Vault Encryption Successful")
            st.download_button(
                label="Download Encrypted Asset",
                data=final_data,
                file_name=f"{uploaded_file.name}.enc",
                mime="application/octet-stream"
            )

        else:
            # Parse Metadata
            filesize = int(file_bytes[:16])
            IV = file_bytes[16:32]
            ciphertext = file_bytes[32:]
            
            decryptor = AES.new(key, AES.MODE_CBC, IV)
            decrypted_data = decryptor.decrypt(ciphertext)
            
            # Remove Padding
            final_data = decrypted_data[:filesize]
            
            st.divider()
            st.success("Vault Access Granted")
            st.download_button(
                label="Download Original Asset",
                data=final_data,
                file_name=uploaded_file.name.replace(".enc", ""),
                mime="application/octet-stream"
            )
            
    except Exception:
        st.error("Authentication Error: Invalid Master Key or Corrupt Packet.")

# --- FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #8b949e !important; font-size: 0.8rem;'>"
    "Industry Standard AES-256-CBC Protection | Secure Client-Side Session"
    "</p>", 
    unsafe_allow_html=True
)
