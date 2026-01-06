import streamlit as st
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import io

def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

st.set_page_config(page_title="AES File Guard", page_icon="🔐")

st.title("🔐 AES File Guard")
st.info("Securely encrypt or decrypt your files using AES-256. Files are processed in your browser session and not stored on our server.")

# 1. User Inputs
password = st.text_input("Enter Secret Password", type="password", help="This password is used to generate your 256-bit key.")
uploaded_file = st.file_uploader("Upload file to process")
mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"])

if uploaded_file and password:
    key = get_key(password)
    file_bytes = uploaded_file.getvalue()
    
    try:
        if mode == "Encrypt":
            # Encryption Logic
            filesize = str(len(file_bytes)).zfill(16)
            IV = Random.new().read(16)
            encryptor = AES.new(key, AES.MODE_CBC, IV)
            
            # Padding
            pad_len = 16 - (len(file_bytes) % 16)
            padded_data = file_bytes + (b' ' * pad_len)
            
            # Result: Size(16) + IV(16) + Data
            final_data = filesize.encode('utf-8') + IV + encryptor.encrypt(padded_data)
            
            st.success("Encryption Complete!")
            st.download_button(
                label="📥 Download Encrypted File",
                data=final_data,
                file_name=f"{uploaded_file.name}.enc"
            )

        else:
            # Decryption Logic
            filesize = int(file_bytes[:16])
            IV = file_bytes[16:32]
            ciphertext = file_bytes[32:]
            
            decryptor = AES.new(key, AES.MODE_CBC, IV)
            decrypted_data = decryptor.decrypt(ciphertext)
            final_data = decrypted_data[:filesize] # Truncate padding
            
            st.success("Decryption Complete!")
            st.download_button(
                label="📥 Download Original File",
                data=final_data,
                file_name=uploaded_file.name.replace(".enc", "")
            )
    except Exception as e:
        st.error(f"An error occurred. Ensure your password is correct for decryption. Error: {e}")
