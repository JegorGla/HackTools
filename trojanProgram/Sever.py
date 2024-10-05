import socket
import struct
import cv2
import numpy as np
from PIL import Image
import io
import pickle
from threading import Thread
import tkinter as tk

conn = None  # Глобальная переменная для сокета

def start_server():
    global conn
    HOST = '0.0.0.0'
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Ожидание подключения...")

    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")

    data = b""
    payload_size = struct.calcsize("!L")

    def update_display():
        nonlocal data
        try:
            while True:
                while len(data) < payload_size:
                    packet = conn.recv(4096)
                    if not packet:
                        raise ConnectionError("Соединение потеряно.")
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                screen_msg_size = struct.unpack("!L", packed_msg_size)[0]

                while len(data) < screen_msg_size:
                    packet = conn.recv(4096)
                    if not packet:
                        raise ConnectionError("Соединение потеряно.")
                    data += packet

                screen_data = data[:screen_msg_size]
                data = data[screen_msg_size:]

                screen_img = Image.open(io.BytesIO(screen_data))
                screen_frame = np.array(screen_img)
                screen_frame = cv2.cvtColor(screen_frame, cv2.COLOR_RGB2BGR)

                while len(data) < payload_size:
                    packet = conn.recv(4096)
                    if not packet:
                        raise ConnectionError("Соединение потеряно.")
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                camera_msg_size = struct.unpack("!L", packed_msg_size)[0]

                while len(data) < camera_msg_size:
                    packet = conn.recv(4096)
                    if not packet:
                        raise ConnectionError("Соединение потеряно.")
                    data += packet

                camera_data = data[:camera_msg_size]
                data = data[camera_msg_size:]

                camera_frame = pickle.loads(camera_data)

                screen_frame_with_text = screen_frame.copy()
                camera_frame_with_text = camera_frame.copy()

                cv2.putText(screen_frame_with_text, f'User: {addr}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(camera_frame_with_text, f'User: {addr}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                cv2.imshow('Remote Screen', screen_frame_with_text)
                cv2.imshow('Camera Feed', camera_frame_with_text)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except ConnectionError as e:
            print(f"Ошибка соединения: {e}")
        finally:
            conn.close()
            server_socket.close()
            cv2.destroyAllWindows()

    def play_video_on_client():
        global conn
        try:
            if conn:
                conn.sendall(b'PLAY_VIDEO')
            else:
                print("Соединение закрыто. Команда не отправлена.")
        except Exception as e:
            print(f"Ошибка при отправке команды: {e}")

    def create_gui():
        root = tk.Tk()
        root.title("Video Control")

        play_button = tk.Button(root, text="Play Video", command=play_video_on_client)
        play_button.pack(pady=20)

        root.mainloop()

    display_thread = Thread(target=update_display)
    display_thread.start()

    create_gui()

if __name__ == '__main__':
    start_server()
