import os
from cryptography.fernet import Fernet

# Load the previously generated key
def load_key():
    return open("ransomware_key.key", "rb").read()

# Decrypt a file
def decrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = Fernet(key).decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

# Decrypt all files in a directory
def decrypt_directory(directory_path, key):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            decrypt_file(file_path, key)

if __name__ == "__main__":
    directory_to_decrypt = "test"  # Specify the directory to decrypt
    decryption_key = load_key()
    decrypt_directory(directory_to_decrypt, decryption_key)
    print(f"Files in {directory_to_decrypt} have been decrypted.")