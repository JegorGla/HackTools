from moviepy.editor import VideoFileClip
import tkinter as tk
from threading import Thread

def play_video(video_path):
    def run_video():
        # Загрузка видеофайла
        clip = VideoFileClip(video_path)
        
        # Воспроизведение видео
        clip.preview(fullscreen=True)

    # Создаем и запускаем поток для воспроизведения видео
    video_thread = Thread(target=run_video)
    video_thread.start()
