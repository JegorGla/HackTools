import cv2
import numpy as np
import socket
import pickle
import struct

# Настройки
HOST = '0.0.0.0'  # Принимаем соединения на любом IP
PORT = 5000  # Порт сервера

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Сервер ожидает подключения...")

# Принимаем соединение от клиента
conn, addr = server_socket.accept()
print(f"Подключено к {addr}")

while True:
    try:
        # Получаем размер сообщения
        message_size = struct.unpack("I", conn.recv(struct.calcsize("I")))[0]
        data = b""
        
        # Получаем все данные
        while len(data) < message_size:
            packet = conn.recv(message_size - len(data))
            if not packet:
                break
            data += packet
        
        # Декодируем кадры
        frame = pickle.loads(data)
        
        # Отображаем кадры
        cv2.imshow('Frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(f"Ошибка: {e}")
        break

# Закрываем соединение
conn.close()
server_socket.close()
cv2.destroyAllWindows()
