import socket
import os

SERVER_IP = '192.168.1.10'  # Replace with the Pi's IP
PORT = 50000
SAVE_DIR = './received_images'  # Client will store received images here

def receive_directory_contents(sock):
    """
    Receives all files from the server and saves them in SAVE_DIR.
    Protocol must match what server.py sends.
    """
    # Ensure the SAVE_DIR exists
    os.makedirs(SAVE_DIR, exist_ok=True)

    # 1) Read the 4 bytes indicating number of files
    data = sock.recv(4)
    num_files = int.from_bytes(data, 'big')
    print(f"Expecting {num_files} files...")

    for _ in range(num_files):
        # 2) Read filename length (4 bytes)
        data = sock.recv(4)
        fname_len = int.from_bytes(data, 'big')

        # 3) Read filename
        filename = sock.recv(fname_len).decode('utf-8')

        # 4) Read file size (8 bytes)
        data = sock.recv(8)
        file_size = int.from_bytes(data, 'big')

        # 5) Read file content
        file_data = b''
        remaining = file_size
        while remaining > 0:
            chunk = sock.recv(min(4096, remaining))
            if not chunk:
                break
            file_data += chunk
            remaining -= len(chunk)

        # Save the file
        save_path = os.path.join(SAVE_DIR, filename)
        with open(save_path, 'wb') as f:
            f.write(file_data)
        print(f"Received and saved {filename} ({file_size} bytes)")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Connecting to {SERVER_IP}:{PORT}...")
        s.connect((SERVER_IP, PORT))
        print("Connected. Receiving files...")
        receive_directory_contents(s)
        print("All files received successfully.")

if __name__ == "__main__":
    main()
