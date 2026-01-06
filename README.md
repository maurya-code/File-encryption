# ☣️ FILE ENCRYPTION CYBER-VAULT v2.0
> **Guard your digital soul: Secure your files from unauthorized access.**

[![Python](https://img.shields.io/badge/Python-3.9+-00ff41?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Cryptography](https://img.shields.io/badge/Security-AES--256-green?style=for-the-badge&logo=lock&logoColor=white)](https://pycryptodome.readthedocs.io/)

---

## 🌐 Live Demo
Access the live deployment on:  👉 **[Link](https://file-encryption.streamlit.app/)**

---

## 📸 System Preview
*Visual confirmation of the Secure Node interface.*

| 🔒 Encryption Interface | 
| :--- | 
| ![Dashboard](https://github.com/maurya-code/File-encryption/blob/main/1.png) | 
| ![2](https://github.com/maurya-code/File-encryption/blob/main/2.png)|
| ![3](https://github.com/maurya-code/File-encryption/blob/main/3.png)|



---

## 🛡️ Core Technology Stack

### ⚡ Encryption Protocol
The engine utilizes **AES-256 (Advanced Encryption Standard)** in **Cipher Block Chaining (CBC)** mode. This provides military-grade security for personal data assets.

### 🔑 Key Derivation (KDF)
We utilize **SHA-256 Hashing** to transform your master password into a 256-bit cryptographic key. This ensures that even simple passwords provide a high level of entropy for the encryption process.

### 🔒 Zero-Knowledge Architecture
- **No Data Persistence:** Files are never stored on a hard drive or database.
- **Client-Side Processing:** All cryptographic operations happen within your current session's memory.
- **Privacy First:** The developer cannot access your files or your master key.

---

### 🎮 Operational Guide

- **Master Key:** Enter a secret password to generate your unique AES key.

- **Targeting:** Upload the file you wish to secure or recover.

- **Execution:** Select ENCRYPT to hide data or DECRYPT to reveal it.

- **Validation:** Our system checks for a cryptographic signature. If the password is wrong, access is strictly denied.

## 🚀 How to Run Locally

### 1. Clone the Node
```bash
git clone [https://github.com/maurya-code/File-encryption.git](https://github.com/maurya-code/File-encryption.git)
cd YOUR_REPO_NAME
