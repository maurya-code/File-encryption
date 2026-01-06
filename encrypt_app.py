import streamlit as st
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AES File Guard | Abhishek", page_icon="🔐")

# --- CUSTOM UI STYLING (Hacker Aesthetic) ---
def apply_custom_style():
    st.markdown(
        """
        <style>
        /* Background Image and Main App styling */
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                        url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80");
            background-size: cover;
            background-attachment: fixed;
        }

        /* Hacker Green Text Colors */
        h1, h2, h3, p, span, label, .stMarkdown {
            color: #00FF41 !important;
            font-family: 'Courier New', Courier, monospace !important;
            text-shadow: 0 0 5px #00FF41;
        }

        /* Style for the Quote */
        .quote-box {
            border-left: 5px solid #00FF41;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            background-color: rgba(0, 255, 65, 0.1);
        }

        /* Input Box Styling */
        .stTextInput>div>div>input {
            background-color: #0d0d0d !important;
            color: #00FF41 !important;
            border: 1px solid #00FF41 !important;
        }

        /* Button Styling */
        .stButton>button {
            background-color: #003b00 !important;
            color: #00FF41 !important;
            border: 2px solid #00FF41 !important;
            width: 100%;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #00FF41 !important;
            color: black !important;
            box-shadow: 0 0 20px #00FF41;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

apply_custom_style()

# --- ENCRYPTION LOGIC ---
def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

# --- UI CONTENT ---
st.title("🔐 AES FILE GUARD")
st.write("### Made with ❤️,🧑‍💻 by Abhishek")

# Your Personal Quote
st.markdown(
    '<div class="quote-box">"Make your files safe from unauthorized access. Guard your digital soul."</div>', 
    unsafe_allow_html=True
)

st.info("System Status: Online. Encryption Engine: AES-256-CBC.")

# User Inputs
password = st.text_input("Enter Secret Access Key", type="password", help="This key generates your 256-bit AES protection.")
uploaded_file = st.file_uploader("Upload File to Secure")
mode = st.radio("Select Protocol:", ["Encrypt", "Decrypt"])

if uploaded_file and password:
    key = get_key(password)
    file_bytes = uploaded_file.getvalue()
    
    try:
        if mode == "Encrypt":
            # Encryption Process
            filesize = str(len(file_bytes)).zfill(16)
            IV = Random.new().read(16)
            encryptor = AES.new(key, AES.MODE_CBC, IV)
            
            # Padding to 16 bytes
            pad_len = 16 - (len(file_bytes) % 16)
            padded_data = file_bytes + (b' ' * pad_len)
            
            # Combined Output
            final_data = filesize.encode('utf-8') + IV + encryptor.encrypt(padded_data)
            
            st.success("✅ ENCRYPTION COMPLETE. DATA SECURED.")
            st.download_button(
                label="📥 DOWNLOAD ENCRYPTED ASSET",
                data=final_data,
                file_name=f"{uploaded_file.name}.enc"
            )

        else:
            # Decryption Process
            filesize = int(file_bytes[:16])
            IV = file_bytes[16:32]
            ciphertext = file_bytes[32:]
            
            decryptor = AES.new(key, AES.MODE_CBC, IV)
            decrypted_data = decryptor.decrypt(ciphertext)
            final_data = decrypted_data[:filesize] 
            
            st.success("🔓 DECRYPTION SUCCESSFUL. ACCESS GRANTED.")
            st.download_button(
                label="📥 DOWNLOAD DECRYPTED FILE",
                data=final_data,
                file_name=uploaded_file.name.replace(".enc", "")
            )
            
    except Exception as e:
        st.error("🚫 ACCESS DENIED: Incorrect key or corrupted data packet.")

st.markdown("<br><hr><center>Secure Node v4.2 | Private Session</center>", unsafe_allow_html=True)
