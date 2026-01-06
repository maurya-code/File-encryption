import streamlit as st
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ABHISHEK | CYBER-VAULT", page_icon="☣️", layout="wide")

# --- HACKER UI CSS ---
def apply_hacker_style():
    st.markdown(
        """
        <style>
        /* High-Tech Background */
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), 
                        url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=2000");
            background-size: cover;
            background-attachment: fixed;
        }

        /* Glowing Hacker Text */
        h1, h2, h3, p, label, .stMarkdown {
            color: #00ff41 !important; /* Matrix Green */
            font-family: 'Courier New', Courier, monospace !important;
            text-shadow: 0 0 8px rgba(0, 255, 65, 0.6);
        }

        /* Glassmorphism Containers */
        [data-testid="stVerticalBlock"] > div:has(div.stExpander) {
            background: rgba(0, 20, 0, 0.5);
            border: 1px solid #00ff41;
            border-radius: 10px;
            padding: 15px;
        }

        /* Input Fields */
        div[data-baseweb="input"] {
            background-color: rgba(0, 40, 0, 0.7) !important;
            border: 1px solid #00ff41 !important;
            border-radius: 4px !important;
        }
        input {
            color: #00ff41 !important;
        }

        /* Cyber Button */
        .stButton>button {
            background: transparent !important;
            color: #00ff41 !important;
            border: 2px solid #00ff41 !important;
            border-radius: 0px !important;
            text-transform: uppercase;
            font-weight: bold;
            letter-spacing: 2px;
            width: 100%;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background: #00ff41 !important;
            color: black !important;
            box-shadow: 0 0 20px #00ff41;
        }

        /* File Uploader styling */
        [data-testid="stFileUploadDropzone"] {
            border: 1px dashed #00ff41 !important;
            background: rgba(0, 40, 0, 0.4) !important;
        }
        
        /* Scanline Animation Effect */
        .stApp::before {
            content: " ";
            display: block;
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), 
                        linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
            z-index: 2;
            background-size: 100% 4px, 3px 100%;
            pointer-events: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

apply_hacker_style()

# --- SECURITY ENGINE ---
SIGNATURE = b"VERIFIED_BY_ABHISHEK"

def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

# --- INTERFACE ---
st.markdown('<h1 style="text-align:center;">☣️ CYBER-VAULT v2.0</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#00ff41;">SECURE NODE: ACTIVE | ACCESS: RESTRICTED</p>', unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.write("### [ ENTRY PROTOCOL ]")
    password = st.text_input("Enter Access Key:", type="password", placeholder="****")
    mode = st.radio("Select Command:", ["ENCRYPT_ASSET", "DECRYPT_ASSET"])
    
    st.info("NOTICE: No data is transmitted to external servers. All operations occur within the local encryption buffer.")

with col2:
    st.write("### [ DATA UPLOAD ]")
    uploaded_file = st.file_uploader("Upload Target File:")
    
    if st.button("EXECUTE OPERATION"):
        if not uploaded_file or not password:
            st.error("SYSTEM ERROR: MISSING KEY OR ASSET")
        else:
            key = get_key(password)
            file_bytes = uploaded_file.getvalue()
            
            try:
                if "ENCRYPT" in mode:
                    with st.spinner("INITIATING AES-256 ENCRYPTION..."):
                        filesize = str(len(file_bytes)).zfill(16)
                        IV = Random.new().read(16)
                        encryptor = AES.new(key, AES.MODE_CBC, IV)
                        
                        # Add signature to verify password later
                        payload = SIGNATURE + file_bytes
                        pad_len = 16 - (len(payload) % 16)
                        padded_data = payload + (b' ' * pad_len)
                        
                        final_data = filesize.encode('utf-8') + IV + encryptor.encrypt(padded_data)
                        
                        st.success("ENCRYPTION COMPLETE")
                        st.download_button("📥 DOWNLOAD ENCRYPTED_DATA.ENC", final_data, file_name=f"{uploaded_file.name}.enc")
                
                else:
                    with st.spinner("ATTEMPTING DECRYPTION..."):
                        filesize = int(file_bytes[:16])
                        IV = file_bytes[16:32]
                        ciphertext = file_bytes[32:]
                        
                        decryptor = AES.new(key, AES.MODE_CBC, IV)
                        decrypted_raw = decryptor.decrypt(ciphertext)
                        
                        # Check if signature exists (Correct Password)
                        if decrypted_raw.startswith(SIGNATURE):
                            final_data = decrypted_raw[len(SIGNATURE):len(SIGNATURE)+filesize]
                            st.success("ACCESS GRANTED: SIGNATURE VERIFIED")
                            st.download_button("📥 DOWNLOAD DECRYPTED_FILE", final_data, file_name=uploaded_file.name.replace(".enc", ""))
                        else:
                            st.error("🚫 ACCESS DENIED: INVALID KEY DETECTED")
                            
            except Exception as e:
                st.error("CRITICAL SYSTEM FAILURE: DATA CORRUPTION")

st.markdown("---")
st.markdown('<p style="text-align:center; font-size:0.8rem; opacity:0.7;">MADE BY ABHISHEK | GUARD YOUR DIGITAL SOUL</p>', unsafe_allow_html=True)
