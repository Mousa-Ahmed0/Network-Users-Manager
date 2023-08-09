import socket
import os
import tqdm
SERVER = "127.0.0.1"
PORT = 12346
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

while True:

    msg = client.recv(1024)
    index = str(msg.decode())

    if index == "1":
        in_data = client.recv(1024)
        print(in_data)
        index = 0
        continue
    elif index == "2":
        move_data = input()
        client.send(bytes(move_data, 'UTF-8'))
        index = 0
        continue
    elif index == "3":
        # upload (send to server)
        filename = input("Enter file name: ")

        if os.path.isfile(filename):

            file_size = os.path.getsize(filename)

            client.send(f"{filename}{SEPARATOR}{file_size}".encode())

            progress = tqdm.tqdm(range(file_size), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:

                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break

                    client.sendall(bytes_read)
                    progress.update(len(bytes_read))
            continue
        else:
            client.send(f"no_file{SEPARATOR}no_file".encode())
            print("file not found..")
            continue

    elif index == "4":
        # download (recv from server)

        received = client.recv(BUFFER_SIZE).decode()
        filename, file_size = received.split(SEPARATOR)

        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        file_size = int(file_size)
        progress = tqdm.tqdm(range(file_size),
                             f"Receiving {filename}", unit="KB", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            bytes_received = 0
            while bytes_received < file_size:
                bytes_read = client.recv(BUFFER_SIZE)
                if not bytes_read:
                    break

                f.write(bytes_read)
                bytes_received += len(bytes_read)
                progress.update(len(bytes_read))

            print("Downloaded Successfully....")
