import socket
import os
import requests
import colorama
from colorama import Fore
from tqdm import tqdm
import threading
import time
import platform
import yaml

def write_ngrok_config_windows(authtoken, user):
    # Путь к конфигурационному файлу ngrok
    ngrok_config_path = os.path.expanduser(f"C:/Users/{user}/AppData/Local/ngrok/ngrok.yml")

    # Структура конфигурации ngrok
    config_data = {
        "version": "2",
        "authtoken": authtoken,  # Вставьте ваш токен сюда
        "tunnels": {
            "http_tunnel": {
                "proto": "http",
                "addr": 5000  # Порт для HTTP-туннеля
            },
            "tcp_tunnel": {
                "proto": "tcp",
                "addr": 12345  # Порт для TCP-туннеля
            }
        }
    }

    # Запись данных в конфигурационный файл ngrok.yml
    os.makedirs(os.path.dirname(ngrok_config_path), exist_ok=True)
    with open(ngrok_config_path, "w") as config_file:
        yaml.dump(config_data, config_file, default_flow_style=False)
    
    print("Конфигурационный файл ngrok.yml успешно обновлён.")
    print("Теперь запустите ngrok в новой вкладке используя ngrok start --all")

    # # Запускаем ngrok с захватом вывода
    # process = subprocess.Popen(
    #     ["ngrok", "start", "--all"],
    #     stdout=subprocess.PIPE,  # захват стандартного вывода
    #     stderr=subprocess.PIPE,  # захват ошибок
    #     text=True  # чтобы вывод был в текстовом формате
    # )

    # # Чтение и вывод строк из stdout
    # for line in process.stdout:
    #     print(line, end="")  # Вывод в реальном времени
    # # Можно также обрабатывать stderr, если нужно
    # for line in process.stderr:
    #     print(f"Ошибка: {line}", end="")
def write_ngrok_config_linux(authtoken):
    import yaml

def write_ngrok_config_linux(authtoken):
    # Путь к конфигурационному файлу ngrok в Linux
    ngrok_config_path = os.path.expanduser("~/.ngrok2/ngrok.yml")

    # Структура конфигурации ngrok
    config_data = {
        "version": "2",
        "authtoken": authtoken,  # Вставьте ваш токен сюда
        "tunnels": {
            "http_tunnel": {
                "proto": "http",
                "addr": 5000  # Порт для HTTP-туннеля
            },
            "tcp_tunnel": {
                "proto": "tcp",
                "addr": 12345  # Порт для TCP-туннеля
            }
        }
    }

    # Запись данных в конфигурационный файл ngrok.yml
    os.makedirs(os.path.dirname(ngrok_config_path), exist_ok=True)
    with open(ngrok_config_path, "w") as config_file:
        yaml.dump(config_data, config_file, default_flow_style=False)
    
    print("Конфигурационный файл ngrok.yml успешно обновлён.")
    print("Теперь запустите ngrok в новой вкладке.")

def print_commands(os_name, commands):
    print("Доступные команды:")
    for cmd in commands.get(os_name, []):
        print(" -", cmd)

def get_operating_system():
    return platform.system()

def download_file(url, save_path):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            with open(save_path, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(save_path)) as bar:
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    bar.update(len(data))
            print(f"Файл '{save_path}' успешно загружен.")
            return

        except requests.exceptions.ConnectionError:
            print(f"Ошибка соединения при загрузке файла. Попробуйте снова.")
            if attempt == max_retries - 1:
                print("Не удалось загрузить файл после нескольких попыток.")
        
        except requests.exceptions.Timeout:
            print(f"Время ожидания истекло. Повторная попытка...")
            continue

        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась: {str(e)}")
            if attempt == max_retries - 1:
                print("Не удалось загрузить файл после нескольких попыток.")

def download_file_thread(url, save_path):
    # Функция для загрузки файла в отдельном потоке
    thread = threading.Thread(target=download_file, args=(url, save_path))
    thread.start()

def send_keep_alive(client_socket, interval=60):
    while True:
        time.sleep(interval)
        try:
            client_socket.send("KEEP_ALIVE".encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError):
            print("Соединение с клиентом потеряно.")
            break

def start_server():
    colorama.init(autoreset=True)
    print(Fore.RED + "Не забудьте запустить ngrok и app.py в директории сервера.")
    if os_name == "Windows":
        user = os.getlogin()

        # Запрашиваем authtoken и настраиваем конфигурацию ngrok
        authtoken = input("Введите ваш authtoken для ngrok: ")
        write_ngrok_config_windows(authtoken, user)  # Записываем конфиг

    if os_name == "Linux":
        authtoken = input("Введите ваш authtoken для ngrok: ")
        write_ngrok_config_linux(authtoken)  # Записываем конфиг

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)
    print("Сервер запущен, ждем подключения...")

    client_socket, addr = server_socket.accept()
    print(f"Подключено к {addr}")

    os_name = get_operating_system()
    print(f"ОС клиента: {os_name}")

    keep_alive_thread = threading.Thread(target=send_keep_alive, args=(client_socket,))
    keep_alive_thread.daemon = True
    keep_alive_thread.start()

    commands = {
        "Windows": [
            "dir - показує вміст поточної директорії",
            "cd <шлях> - змінює поточну директорію",
            "ipconfig - мережеві інтерфейси",
            "cls - очищення екрану",
            "ping <адреса> - перевірка доступності",
            "mkdir <папка> - нова директорія",
            "exit - завершує роботу",
            "copy <файл1> <файл2> - копіює файл",
            "del <файл> - видаляє файл",
            "move <файл> <папка> - переміщує файл",
            "tasklist - список запущених процесів",
            "taskkill /IM <ім'я процесу> - завершити процесс",
            "chkdsk - проверка диска",
            "shutdown /s - вимкнення комп'ютера",
            "systeminfo - информация про систему",
        ],
        "Linux": [
            "ls - перегляд вмісту каталогу",
            "cd <шлях> - зміна каталогу",
            "rm <файл> - видалення файлів",
            "clear - очищення екрану",
            "mkdir <каталог> - створення каталогу",
            "exit - завершує роботу",
            "cp <файл1> <файл2> - копіює файл",
            "mv <файл> <каталог> - переміщує файл",
            "touch <файл> - створення нового файлу",
            "chmod <права> <файл> - зміна прав доступу",
            "ps - список запущених процесів",
            "kill <PID> - завершити процес",
            "shutdown - вимкнення системи",
            "ifconfig - налаштування мережевих інтерфейсов",
        ]
    }
    
    print_commands(os_name, commands)
    
    while True:
        try:
            command = input("\nВведите команду: ")
            if command.lower() == 'exit':
                client_socket.send(command.encode('utf-8'))
                break
            elif command.lower() in ['cls', 'clear']:
                os.system('cls' if os_name == "Windows" else 'clear')
                print_commands(os_name, commands)
                continue
            elif command.startswith('curl '):
                url = command.split(' ', 1)[1]
                save_directory = input("Введите путь для сохранения файла (или нажмите Enter): ")
                if not save_directory:
                    save_directory = os.path.expanduser("~/Downloads") if os_name == "Linux" else 'C:\\Downloads'
                elif not os.path.exists(save_directory):
                    print(f"Создание директории '{save_directory}'.")
                    os.makedirs(save_directory)

                filename = os.path.join(save_directory, os.path.basename(url))
                download_file_thread(url, filename)  # Загрузка в отдельном потоке
                continue

            client_socket.send(command.encode('utf-8'))

            response = ""
            while True:
                part = client_socket.recv(4096).decode('utf-8', errors='replace')
                if "END_OF_MSG" in part:
                    response += part.replace("END_OF_MSG", "")
                    break
                response += part

            if response.strip() != "KEEP_ALIVE":
                print(f"Ответ клиента:\n{response}")

        except (BrokenPipeError, ConnectionResetError):
            print("Соединение с клиентом потеряно.")
            break

    server_socket.close()

if __name__ == "__main__":
    start_server()
