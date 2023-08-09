import os
import socket
import sqlite3
import threading
from time import sleep
import tqdm
#name of database
dbPath = "TCPSer.db"
#number of user
def countID():
    DB = sqlite3.connect(dbPath)
    cr = DB.cursor()
    cr.execute('SELECT MAX(userID) FROM users')
    numID = cr.fetchone()[0]
    cr.close()
    DB.close()

    if not numID:
        return 0
    else:
        return numID

#print all user
def printUser():
    DB = sqlite3.connect(dbPath)
    cr = DB.cursor()
    query = "SELECT * FROM users"
    cr.execute(query)
    usersList = cr.fetchall()
    cr.close()
    DB.close()
    print('--------------------------------------------------')
    if not usersList:
        print("No users found.")
    else:
        print("List of all users:")
        for user in usersList:
            user_id, user_name, password, first_name, last_name, status = user
            print(f"User ID: {user_id}, User Name: {user_name}, Password: {password} First Name: {first_name}, Last Name: {last_name}, Status: {status}")
    print('--------------------------------------------------')

#admin

def serAdministrator():
    counter = countID()
    user_id = 0

    while True:
        printUser()

        enter = int(input("To add user enter: 1 \n"
                          "To delete user enter: 2 \n"
                          "To block/unblock (user or IP) enter :3 \n"
                          "To update user info enter :4\n "
                          "To exit enter :5 \n"))

        if enter == 1:

            user_name = input("Enter user Name: ")
            password = input("Enter password: ")
            first_name = input("Enter first Name: ")
            last_name = input("Enter last Name: ")

            query = "INSERT INTO users (userID, username, password, firstName, lastName, status) VALUES (?, ?, ?, ?, ?, TRUE)"
            user_id = counter + 1
            counter = counter + 1

            try:
                DB = sqlite3.connect(dbPath)
                cr = DB.cursor()
                cr.execute(query, (user_id, user_name, password, first_name, last_name))
                DB.commit()
                cr.close()
                DB.close()

            except Exception:
                print("wrong formula")
                continue

        elif enter == 2:

            user_id = input("Get me user ID for delete him: ")
            query = "DELETE FROM users WHERE userID = ?"

            try:
                DB = sqlite3.connect(dbPath)
                cr = DB.cursor()
                cr.execute(query, (user_id,))
                DB.commit()
                cr.close()
                DB.close()
                user_id = counter - 1
                counter = counter - 1
            except Exception:
                print("wrong formula")
                continue

            print(f"User with ID {user_id} has been deleted.")

        elif enter == 3:
            y = int(input("To block user enter 1 \n"
                          "To unblock user enter 2 \n"
                          "To block IP enter 3 \n"
                          "To unblock IP enter 4 \n"
                          "To exit enter any other thing\n"))

            if y == 1:

                user_id = input("Enter user id for block: ")
                query = "UPDATE users SET status = False WHERE userID = ?"

                try:
                    DB = sqlite3.connect(dbPath)
                    cr = DB.cursor()
                    cr.execute(query, (user_id,))
                    DB.commit()
                    cr.close()
                    DB.close()
                except Exception:
                    print("wrong formula")
                    continue

                print(f"This user is blocked: {user_id}.")

            elif y == 2:

                user_id = input("Enter user id for unblock: ")
                query = "UPDATE users SET status = TRUE WHERE userID = ?"

                try:
                    DB = sqlite3.connect(dbPath)
                    cr = DB.cursor()
                    cr.execute(query, (user_id,))
                    DB.commit()
                    cr.close()
                    DB.close()
                except Exception:
                    print("wrong formula")
                    continue

                print(f"This user is unblocked: {user_id}.")

            elif y == 3:

                ip_address = input("Enter IP for block: ")
                query = "INSERT INTO ip_blacklist (ipAddress) VALUES (?)"
                try:
                    DB = sqlite3.connect(dbPath)
                    cr = DB.cursor()
                    cr.execute(query, (ip_address,))
                    DB.commit()
                    cr.close()
                    DB.close()
                except Exception:
                    print("wrong formula")
                    continue

                print(f"IP {ip_address} inserted into the black list table with status set to FALSE.")

            elif y == 4:

                try:
                    DB = sqlite3.connect(dbPath)
                    cr = DB.cursor()
                    cr.execute("SELECT * FROM ip_blacklist")
                    IP_list = cr.fetchall()
                    cr.close()
                    DB.close()

                    if not IP_list[0]:
                        print("Records not found .")
                    else:
                        print("IP\t\tStatus")
                        print("-----------------------")
                        for record in IP_list:
                            print(f"{record[0]}")

                except Exception:
                    print("Error while listing records:")
                    continue

                IP = input("Enter IP to unblock: ")
                IP = str(IP)
                try:
                    DB = sqlite3.connect(dbPath)
                    cr = DB.cursor()
                    query = "DELETE FROM ip_blacklist WHERE ipAddress = ?"
                    cr.execute(query, (IP,))
                    DB.commit()
                    cr.close()
                    DB.close()
                except Exception:
                    print("Error while listing records:")
                    continue
            else:
                continue

        elif enter == 4:
            print("what the update you want : ")
            print("1-update user name. \n2- update password. \n3- update first name. \n4- update last name. ")

            z = int(input("Enter your update : "))  # Convert the input to an integer
            user_id = input("Enter users ID for update : ")

            text = ""
            data = ""
            if z == 1:
                text = "username"
                data = input("Enter the new username: ")
            elif z == 2:
                text = "password"
                data = input("Enter the new password: ")
            elif z == 3:
                text = "firstName"
                data = input("Enter the new first name: ")
            elif z == 4:
                text = "lastName"
                data = input("Enter new last name: ")
            else:
                print("Invalid choice.")
                exit()

            try:
                DB = sqlite3.connect(dbPath)
                cr = DB.cursor()
                query = f"UPDATE users SET {text} = ? WHERE userID = ?"
                cr.execute(query, (data, user_id,))
                DB.commit()
                cr.close()
                DB.close()
            except Exception:
                print("wrong formula")
                continue
            print("Update completed successfully.")

        elif enter == 5:
            break


def serverUpDowload(User_ID, socket_info):
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"

    while True:   
        try:
            data_base_ = sqlite3.connect(dbPath)
            cursor = data_base_.cursor()
            query = "SELECT fileName FROM files WHERE userID = ?"
            cursor.execute(query, (User_ID,))
            files_list = cursor.fetchall()
            cursor.close()
            data_base_.close()

        except Exception:
                print("wrong formula")
                continue
        if not files_list:
            sleep(0.1)
            socket_info.send(bytes("1", 'UTF-8'))
            socket_info.send(bytes("No files found.", 'UTF-8'))
        else:
            sleep(0.1)
            socket_info.send(bytes("1", 'UTF-8'))
            socket_info.send(bytes("List of all files:", 'UTF-8'))
            for index, file in enumerate(files_list, 0):
                sleep(0.1)
                socket_info.send(bytes("1", 'UTF-8'))
                socket_info.send(bytes(f"{index} => {file[0]}", 'UTF-8'))

        sleep(0.1)
        socket_info.send(bytes("1", 'UTF-8'))
        socket_info.send(bytes("To upload a file enter: 1 \n"
                               "To download a file enter: 2 \n"
                               "To sign out enter: 3 \n", 'UTF-8'))
        sleep(0.1)
        socket_info.send(bytes("2", 'UTF-8'))
        data = socket_info.recv(2048)
        msg_user = str(data.decode())

        if msg_user == "1":
            # # upload (recv from client)
            BUFFER_SIZE = 1024
            SEPARATOR = "<SEPARATOR>"

            socket_info.send(bytes("3", 'UTF-8'))
            received = socket_info.recv(BUFFER_SIZE).decode()
            filename, file_size = received.split(SEPARATOR)
            if filename == "no_file":
                continue

            data_base_ = sqlite3.connect(dbPath)
            cr = data_base_.cursor()
            query = "INSERT INTO files (userID, fileName) VALUES (?, ?)"
            cr.execute(query, (User_ID, filename))
            data_base_.commit()
            cr.close()
            data_base_.close()
            print(f"New record added successfully.ID:{User_ID}File:{filename}")

            filename = os.path.basename(filename)
            file_size = int(file_size)
            progress = tqdm.tqdm(range(file_size), f"Receiving {filename}", unit="KB", unit_scale=True,
                                 unit_divisor=1024)

            with open(filename, "wb") as f:
                bytes_received = 0
                while bytes_received < file_size:
                    bytes_read = socket_info.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break

                    f.write(bytes_read)
                    bytes_received += len(bytes_read)
                    progress.update(len(bytes_read))

            print("File received successfully.")
            sleep(0.1)
            socket_info.send(bytes("1", 'UTF-8'))
            socket_info.send(bytes("Uploaded Successfully.", 'UTF-8'))

        elif msg_user == "2":

            socket_info.send(bytes("1", 'UTF-8'))
            socket_info.send(bytes("Enter file name to download: ", 'UTF-8'))
            sleep(0.1)
            socket_info.send(bytes("2", 'UTF-8'))
            data = socket_info.recv(2048)
            msg_user = str(data.decode())

            filename = msg_user

            if not os.path.isfile(filename):
                sleep(0.1)
                socket_info.send(bytes("1", 'UTF-8'))
                socket_info.send(bytes("file not found :( ", 'UTF-8'))
                continue

            sleep(0.1)
            socket_info.send(bytes("4", 'UTF-8'))
            file_size = os.path.getsize(filename)
            socket_info.send(f"{filename}{SEPARATOR}{file_size}".encode())

            # start sending the file
            progress = tqdm.tqdm(range(file_size), f"Sending {filename}", unit="B", unit_scale=True,
                                 unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break

                    socket_info.sendall(bytes_read)
                    progress.update(len(bytes_read))

        elif msg_user == "3":
            sleep(0.1)
            socket_info.send(bytes("5", 'UTF-8'))
            socket_info.send(bytes("wrong entry :", 'UTF-8'))
            socket_info.cloce()

            break
        else:
            sleep(0.1)
            socket_info.send(bytes("1", 'UTF-8'))
            socket_info.send(bytes("wrong entry :", 'UTF-8'))
            continue


class ClientThread(threading.Thread):

    def __init__(self, client_Address, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = client_Address

    def run(self):

        counter = countID()
        # global return_IP 
        return_IP=""
        try:
            DB = sqlite3.connect(dbPath)
            cr = DB.cursor()
            Address = str(clientAddress[0])
            query = "SELECT * FROM ip_blacklist WHERE ipAddress=?"
            data = cr.execute(query, (Address,))
            return_IP = data.fetchone()
            cr.close()
            DB.close()
        except sqlite3.Error as e:
            print("SQLite error:", e)
        except Exception as e:
            print("An error occurred:", e)
            # break
            
        if return_IP:
            self.csocket.send(bytes("1", 'UTF-8'))
            self.csocket.send(bytes("you are blocked", 'UTF-8'))
            self.csocket.close()
            return
        else:

            while True:

                msg_sign = "1- sign in.   2- close. "
                sleep(0.1)
                self.csocket.send(bytes("1", 'UTF-8'))
                self.csocket.send(bytes(msg_sign, 'UTF-8'))
                sleep(0.1)
                self.csocket.send(bytes("2", 'UTF-8'))
                data = self.csocket.recv(2048)
                msg2 = data.decode()

                if msg2 == "1":  # sign in
                    #user name
                    self.csocket.send(bytes("1", 'UTF-8'))
                    self.csocket.send(bytes("enter user name ", 'UTF-8'))
                    sleep(0.1)
                    self.csocket.send(bytes("2", 'UTF-8'))
                    data = self.csocket.recv(2048)
                    msg_user = data.decode()
                    #password
                    self.csocket.send(bytes("1", 'UTF-8'))
                    self.csocket.send(bytes("enter password ", 'UTF-8'))
                    sleep(0.1)
                    #rev password
                    self.csocket.send(bytes("2", 'UTF-8'))
                    data = self.csocket.recv(2048)
                    msg_password = data.decode()
                    #if exist
                    DB = sqlite3.connect(dbPath)
                    cr = DB.cursor()
                    query = "SELECT username FROM users WHERE username=?"
                    cr.execute(query, (msg_user,))
                    return_user = cr.fetchone()
                    cr.close()
                    DB.close()

                    if not return_user:
                        sleep(0.1)
                        self.csocket.send(bytes("1", 'UTF-8'))
                        self.csocket.send(bytes("this user name not sign up", 'UTF-8'))
                        continue
                    else:
                        #blok or not
                        DB = sqlite3.connect(dbPath)
                        cr = DB.cursor()
                        query = "SELECT status FROM users WHERE username=?"
                        cr.execute(query, (msg_user,))
                        return_status = cr.fetchone()
                        cr.close()
                        DB.close()

                        if return_status[0] == 0:
                            sleep(0.1)
                            self.csocket.send(bytes("1", 'UTF-8'))
                            self.csocket.send(bytes("this user name is blocked", 'UTF-8'))
                            continue
                        else:
                            #test pasaword
                            DB = sqlite3.connect(dbPath)
                            cr = DB.cursor()
                            query = "SELECT userID FROM users WHERE username=? AND password=?"
                            cr.execute(query, (msg_user, msg_password))
                            return_userinfo = cr.fetchone()
                            cr.close()
                            DB.close()

                            if not return_userinfo:
                                sleep(0.1)
                                self.csocket.send(bytes("1", 'UTF-8'))
                                self.csocket.send(bytes("this user password is wrong", 'UTF-8'))
                                continue
                            else:
                                print(f"your welcome: ID =>{return_userinfo[0]}")
                                sleep(0.1)
                                self.csocket.send(bytes("1", 'UTF-8'))
                                self.csocket.send(bytes(f"your welcome: ID =>{return_userinfo[0]}", 'UTF-8'))
                                serverUpDowload(return_userinfo[0], self.csocket)
                                continue

              
                elif msg2 == "2":

                    sleep(0.1)
                    self.csocket.send(bytes("1", 'UTF-8'))
                    self.csocket.send(bytes(f"User{clientAddress[0]} exit successfully", 'UTF-8'))
                    print(f"User{clientAddress} exit successfully.")
                    self.csocket.close()


while True:
    x = input("To run administrator mode enter :1 \n"
              "To run server mode enter :2 \n"
              "To close this programme enter :3\n")
    x = int(x)
    if x == 1:
        serAdministrator()
        continue
    elif x == 2:

        LOCALHOST = ""
        PORT = 12346
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LOCALHOST, PORT))
        server.listen(5)
        print("Run server.....")
        while True:
            clientsock, clientAddress = server.accept()
            print(f"this user {clientAddress} connecting ..")
            ClientThread(clientAddress, clientsock).start()
    elif x == 3:
        break
    else:
        print("wrong formula")
        continue
