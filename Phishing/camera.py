import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Camera App")

        self.video_source = 0  # выбор источника видео, например, 0 для встроенной камеры

        self.vid = CameraVideoCapture(self.video_source)

        # Видео
        self.video_label = tk.Label(window)
        self.video_label.pack(padx=10, pady=10)

        # Кнопки
        self.btn_screenshot = tk.Button(window, text="Сделать скриншот", command=self.take_screenshot)
        self.btn_screenshot.pack(pady=5)

        self.btn_record = tk.Button(window, text="Запись", command=self.toggle_record)
        self.btn_record.pack(pady=5)

        self.btn_exit = tk.Button(window, text="Выход", command=self.exit_app)
        self.btn_exit.pack(pady=5)

        self.is_recording = False
        self.out = None
        self.record_filename = ""

        self.update_video()

    def toggle_record(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.btn_record.config(text="Стоп запись")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.record_filename = f"record_{timestamp}.avi"
            self.out = cv2.VideoWriter(self.record_filename, cv2.VideoWriter_fourcc(*'XVID'), 25, (640, 480))
        else:
            self.btn_record.config(text="Запись")
            if self.out is not None:
                self.out.release()
                self.out = None
                messagebox.showinfo("Запись завершена", f"Видео сохранено как {self.record_filename}")

    def take_screenshot(self):
        ret, frame = self.vid.get_frame()
        if ret:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.png"
            cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Скриншот", f"Скриншот сохранён как {filename}")

    def update_video(self):
        # Захват кадра с камеры
        ret, frame = self.vid.get_frame()

        if ret:
            # Преобразование кадра в формат tkinter
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.video_label.config(image=self.photo)

        # Обновление каждые 20 миллисекунд
        self.video_label.after(20, self.update_video)

        # Запись видео, если включена
        if self.is_recording:
            if self.out is None:
                # Создание объекта записи видео
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"record_{timestamp}.avi"
                self.out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 25, (640, 480))

            if ret:
                self.out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def exit_app(self):
        if self.is_recording:
            self.toggle_record()

        self.window.quit()

class CameraVideoCapture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Невозможно открыть камеру", video_source)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (False, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Запуск приложения
def start_camera_window():
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_camera_window()
