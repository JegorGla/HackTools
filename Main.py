import os
import pyfiglet
from colorama import init, Fore, Style
import sys

# Инициализируем colorama для поддержки цветового вывода
init()

# Получение ширины терминала для центрирования
def get_terminal_size():
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(columns)
    except:
        return 80  # Если не удается получить размер терминала, устанавливаем значение по умолчанию

# Функция для плавного изменения цвета заголовка
def gradient_color(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    gradient_text = ""
    for i, char in enumerate(text):
        gradient_text += colors[i % len(colors)] + char
    return gradient_text + Style.RESET_ALL

# Функция для сохранения имени в файл
def save_name_to_file(name, filename="name.txt"):
    with open(filename, 'w') as f:
        f.write(name)

# Функция для загрузки имени из файла
def load_name_from_file(filename="name.txt"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read().strip()
    return None

# Функция для отображения главного меню с рамкой и центрированием
def display_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # Очистка экрана
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

# Выводим заголовок и приветственное сообщение
print(gradient_color(pyfiglet.figlet_format("ALL HACKING TOOLS", font='starwars')))

# Проверяем, есть ли сохраненное имя
name = load_name_from_file()

if name:
    print(f"Welcome back, {name}!")
else:
    name = input('Enter your name: ')
    save_name_to_file(name)
    print(f'Hello, {name}')

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
        sys.exit()

    else:
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)

except FileNotFoundError:
    print(Fore.RED + "File not found." + Style.RESET_ALL)
except Exception as e:
    print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
