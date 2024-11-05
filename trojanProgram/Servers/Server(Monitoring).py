import socket
import cv2
import numpy as np

def main():
    # Настройки сервера
    host = '0.0.0.0'  # Принимает соединения от всех интерфейсов
    port = 12345       # Порт для прослушивания

    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Сервер запущен, ждем подключения...")
    conn, addr = server_socket.accept()
    print(f"Подключено к {addr}")

    while True:
        # Получаем данные от клиента
        data = conn.recv(4096)
        if not data:
            break

        # Преобразуем полученные данные в изображение
        image_data = np.frombuffer(data, dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        # Отображаем изображение
        cv2.imshow("Received Screen", image)

        # Выход при нажатии клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
