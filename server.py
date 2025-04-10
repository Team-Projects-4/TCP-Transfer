import socket
import os

HOST = '0.0.0.0'         # Listen on all network interfaces
PORT = 50000            # Arbitrary chosen port
IMAGES_DIR = '/home/team4/repos/TCP-Transfer/imageSRC'

def send_directory_contents(conn):
    """
    Sends all files in IMAGES_DIR to the connected client.
    Protocol:
      1) Number of files (int)
      2) For each file:
         a) Filename length (int)
         b) Filename (string, bytes)
         c) File size (int)
         d) File content (bytes)
    """
    files = [f for f in os.listdir(IMAGES_DIR) if os.path.isfile(os.path.join(IMAGES_DIR, f))]
    conn.sendall(len(files).to_bytes(4, 'big'))  # Send the number of files as 4 bytes

    for filename in files:
        filepath = os.path.join(IMAGES_DIR, filename)
        with open(filepath, 'rb') as f:
            file_data = f.read()

        # 1) Send filename length
        conn.sendall(len(filename).to_bytes(4, 'big'))
        # 2) Send filename bytes
        conn.sendall(filename.encode('utf-8'))
        # 3) Send file size
        conn.sendall(len(file_data).to_bytes(8, 'big'))
        # 4) Send file content
        conn.sendall(file_data)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")
            with conn:
                send_directory_contents(conn)
            print("Finished sending files, closing connection")

if __name__ == "__main__":
    main()
