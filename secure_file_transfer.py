import os
import socket
from cryptography.fernet import Fernet
import getpass

# Function to generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Function to encrypt a file
def encrypt_file(file_name, key):
    fernet = Fernet(key)
    with open(file_name, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_name + '.enc', 'wb') as file:
        file.write(encrypted_data)
    print(f"File '{file_name}' encrypted as '{file_name}.enc'.")

# Function to decrypt a file
def decrypt_file(file_name, key):
    fernet = Fernet(key)
    with open(file_name, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_name.replace('.enc', ''), 'wb') as file:
        file.write(decrypted_data)
    print(f"File '{file_name}' decrypted.")

# Function to send an encrypted file over a socket
def send_file(file_name, host='localhost', port=5001):
    sock = socket.socket()
    sock.connect((host, port))
    with open(file_name, 'rb') as file:
        sock.sendfile(file, 0)
    print(f"Sent: {file_name}")
    sock.close()

# Function to receive a file
def receive_file(save_as='received_file.enc', host='localhost', port=5001):
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(1)
    print(f"Listening for connections on {host}:{port}...")
    conn, addr = sock.accept()
    print(f"Connection from {addr} received.")
    with open(save_as, 'wb') as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
    print(f"Received file and saved as '{save_as}'.")
    conn.close()
    sock.close()

# Main program
if __name__ == "__main__":
    option = input("Do you want to (s)end a file or (r)eceive a file? ").lower()
    if option == 's':
        file_name = input("Enter the file name to send: ")
        key = generate_key()
        encrypt_file(file_name, key)
        send_file(file_name + '.enc')
        print("File sent successfully.")
    elif option == 'r':
        receive_file()
        key = getpass.getpass("Enter the encryption key: ")
        decrypt_file('received_file.enc', key)
    else:
        print("Invalid option. Please try again.")
