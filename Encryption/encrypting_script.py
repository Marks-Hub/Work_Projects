from cryptography.fernet import Fernet
import os

def generate_key():
    """Generates a key and saves it to a file"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Key generated and saved as 'secret.key'. Keep this safe!")

def load_key():
    """Loads the key from the current directory"""
    return open("secret.key", "rb").read()

def encrypt_file(filename):
    """Encrypts the file using the generated key"""
    key = load_key()
    f = Fernet(key)
    
    with open(filename, "rb") as file:
        file_data = file.read()
    
    encrypted_data = f.encrypt(file_data)
    
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    print(f"{filename} has been encrypted.")

def decrypt_file(filepath):
    """Decrypts the file back to its original state"""
    key = load_key()
    f = Fernet(key)
    
    with open(filepath, "rb") as file:
        encrypted_data = file.read()
    
    # Decrypting the data
    decrypted_data = f.decrypt(encrypted_data)
    
    with open(filepath, "wb") as file:
        file.write(decrypted_data)
    print(f"Success: {filepath} has been decrypted.")

def encrypt_folder(folder_path):
    key = load_key()
    f = Fernet(key)
    
    # os.walk looks through every file in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Skip the key file itself if it's in the same folder!
            if file == "secret.key":
                continue
                
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, "rb") as incoming_file:
                    data = incoming_file.read()
                
                encrypted_data = f.encrypt(data)
                
                with open(file_path, "wb") as outgoing_file:
                    outgoing_file.write(encrypted_data)
                print(f"Encrypted: {file}")
            except Exception as e:
                print(f"Could not encrypt {file}: {e}")

# --- HOW TO USE ---
# 1. Run generate_key() once if you don't have a key yet.
# 2. Use r"path" to avoid the unicode error.

# Example:
# my_path = r"C:\Users\YourName\Desktop\test.txt"
# encrypt_file(my_path)
# decrypt_file(my_path)

# Usage
# 1. Uncomment generate_key() the first time you run it
#generate_key()

# 2. Specify the file you want to protect
#encrypt_file(r"C:\Users\mokin\Documents\Scripts\Test folder")

#decrypt_file(r"C:\Users\mokin\Desktop\_10bd057b-ae80-4369-8e87-b45b179933f5.jpg")

encrypt_folder(r"C:\Users\mokin\Documents\Scripts\Test folder")