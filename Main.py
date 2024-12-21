import os
import pyfiglet
from colorama import init, Fore, Style
import sys
import time
import threading
import random

# Инициализируем colorama
init()

# Флаг для остановки эффекта
train_effect_running = True

# Получение ширины терминала
def get_terminal_size():
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)
    except:
        return 80

# Плавный градиент цвета
def gradient_color(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    gradient_text = ""
    for i, char in enumerate(text):
        gradient_text += colors[i % len(colors)] + char
    return gradient_text + Style.RESET_ALL

# Сохранение имени
def save_name_to_file(name, filename="name.txt"):
    with open(filename, 'w') as f:
        f.write(name)

# Загрузка имени
def load_name_from_file(filename="name.txt"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read().strip()
    return None

# Эффект движения текста
def train_effect(text, color=Fore.GREEN, delay=0.1):
    global train_effect_running
    text = f" {text} "
    while train_effect_running:
        print(color + text, end='\r')
        text = text[1:] + text[0]
        time.sleep(delay)

# Функция для остановки эффекта
def stop_train_effect():
    global train_effect_running
    train_effect_running = False

# Функция отображения меню
def display_menu():
    terminal_width = get_terminal_size()  # Ширина терминала
    border_char = "="
    border_length = terminal_width - 4

    # Рамка сверху
    print(Fore.CYAN + border_char * terminal_width + Style.RESET_ALL)
    
    # Заголовок с центрированием
    title = pyfiglet.figlet_format("ALL HACKING TOOLS", font='starwars')
    for line in title.splitlines():
        print(gradient_color(line.center(terminal_width)))

    # Рамка снизу заголовка
    print(Fore.CYAN + border_char * terminal_width + Style.RESET_ALL)

    # Приветственное сообщение с центрированием
    print(Fore.GREEN + Style.BRIGHT + "Welcome to the Hacking Tools Menu".center(terminal_width) + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + border_char * border_length + Style.RESET_ALL)

    # Список инструментов
    tools = [
        "1 - Phishing tool",
        "2 - PhoneNumber Picker",
        "3 - DDoS Attack",
        "4 - Trojan Program (for Windows)",
        "5 - IpPicker",
        "6 - QRCode Generation",
        "7 - Find User",
        "8 - Bruteforce wifi",
        "9 - Scan ports",
        "10 - Exit"
    ]
    for tool in tools:
        print(f"{tool.center(terminal_width)}")
    
    print(Fore.CYAN + Style.BRIGHT + border_char * border_length + Style.RESET_ALL)

# Функция для анимации загрузки
def loading_screen():
    loading_steps = [
        "Loading system files...",
        "Connecting to network...",
        "Initiating processes...",
        "Configuring modules...",
        "Verifying security keys...",
    ]
    for step in loading_steps:
        print(Fore.GREEN + Style.BRIGHT + step + Style.RESET_ALL)
        time.sleep(2)

# Анимация хакерского ввода/вывода
def hacker_animation():
    fake_code = [
        "sudo apt update",
        "Connecting to the server...",
        "Bypassing security protocols...",
        "Decrypting files...",
        "Success! Files decrypted.",
        "Initiating DDoS attack...",
        "Connection lost...",
        "Trying to brute force login...",
        "Access granted. Welcome.",
    ]

    for _ in range(3):  # Трижды показываем код
        for line in fake_code:
            print(Fore.GREEN + Style.BRIGHT + f"Executing: {line}" + Style.RESET_ALL)
            time.sleep(random.uniform(0.5, 1.5))  # случайная задержка для эффекта

# Основный цикл программы
while True:
    # Показать экран загрузки перед входом
    loading_screen()

    # Анимация хакерского ввода/вывода
    hacker_animation()

    # Проверяем, есть ли сохраненное имя
    name = load_name_from_file()

    # Если имя есть, выводим приветственное сообщение с эффектом
    if name:
        # Запускаем эффект в отдельном потоке
        train_effect_thread = threading.Thread(target=train_effect, args=(f"Welcome back: {name}", Fore.CYAN, 0.1))
        train_effect_thread.start()
    else:
        # Если имени нет, запрашиваем его у пользователя
        name = input('Enter your name: ')
        save_name_to_file(name)
        print(f'Hello, {name}')

    time.sleep(3)
    
    # Останавливаем эффект движения текста
    stop_train_effect()

    # Отображаем меню
    display_menu()

    # Получаем выбор пользователя
    HackToolChoice = input('Enter your number: ')

    # Обрабатываем выбор пользователя
    try:
        if HackToolChoice == '1':
            exec(open('Phishing/MainPhishing.py', 'r', encoding='utf-8').read())

        elif HackToolChoice == '2':
            exec(open('PhoneNumberPicker/Hack_phonenember.py', 'r', encoding='utf-8').read())

        elif HackToolChoice == '3':
            exec(open('DDoSAtack/DDoSAtack.py', 'r', encoding='utf-8').read())

        elif HackToolChoice == '4':
            exec(open('trojanProgram/SetUpTrojan.py', 'r', encoding='utf-8').read())

        elif HackToolChoice == '5':
            exec(open('Ip/IpPicker.py', 'r', encoding='utf-8').read())

        elif HackToolChoice == '6':
            exec(open('qrCodeGenerate/QRGgenerate.py', 'r', encoding='utf-8').read())

        elif HackToolChoice == '7':
            exec(open('UserFinder/FindUser.py', 'r', encoding='utf-8').read())

        elif HackToolChoice == '8':
            exec(open('BrutforceWifi/WifiMain.py', 'r', encoding='utf-8').read())

        elif HackToolChoice == '9':
            exec(open('ScanPort/Scan.py', 'r', encoding='utf-8').read())

        elif HackToolChoice == '10':
            stop_train_effect()  # Остановить эффект перед выходом
            print(Fore.GREEN + "Goodbye!" + Style.RESET_ALL)
            sys.exit()

        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)

    except FileNotFoundError:
        print(Fore.RED + "File not found." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)

    # Небольшая пауза перед повторным отображением меню
    time.sleep(2)
