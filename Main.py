import os
import pyfiglet
from colorama import init, Fore
import sys

# Инициализируем colorama для поддержки цветового вывода
init()

# Функция для плавного изменения цвета заголовка
def gradient_color(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    gradient_text = ""
    for i, char in enumerate(text):
        gradient_text += colors[i % len(colors)] + char
    return gradient_text

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

# Выводим заголовок с плавным переходом цвета
print(gradient_color(pyfiglet.figlet_format("ALL HACKING TOOLS", font='starwars')))

# Проверяем, есть ли сохраненное имя
name = load_name_from_file()

if name:
    print(f"Welcome back, {name}!")
else:
    name = input('Enter your name: ')
    save_name_to_file(name)
    print(f'Hello, {name}')

print('1 - phishing tool')
print('2 - PhoneNumber Picker')
print('3 - DDoS Attack')
print('4 - Trojan Program (for Windows)')
print('5 - IpPicker')
print('6 - Exit')

HackToolChoice = input('Enter your number: ')

if HackToolChoice == '1':
    try:
        with open('Phishing/MainPhishing.py', 'r', encoding='utf-8') as file:
            os.system('cls')
            exec(file.read())
    except FileNotFoundError:
        print("Main Phishing file not found.")
    except Exception as e:
        print(f"An error occurred while executing the file: {e}")

elif HackToolChoice == '2':
    try:
        with open('PhoneNumberPicker/Hack_phonenember.py', 'r', encoding='utf-8') as file:
            os.system('cls')
            exec(file.read())
    except FileNotFoundError:
        print("PhoneNumberPicker file not found.")
    except Exception as e:
        print(f"An error occurred while executing the file: {e}")

elif HackToolChoice == '3':
    try:
        with open('DDoSAtack/DDoSAtack.py', 'r', encoding='utf-8') as file:
            os.system('cls')
            exec(file.read())
    except FileNotFoundError:
        print("DDoS Attack file not found.")
    except Exception as e:
        print(f"An error occurred while executing the file: {e}")

elif HackToolChoice == '4':
    try:
        with open('trojanProgram/SetUpTrojan.py', 'r', encoding='utf-8') as file:
            os.system('cls')
            exec(file.read())
    except FileNotFoundError:
        print("Trojan Program file not found.")
    except Exception as e:
        print(f"An error occurred while executing the file: {e}")

elif HackToolChoice == '5':
    try:
        with open('Ip/IpPicker.py', 'r', encoding='utf-8') as file:
            os.system('cls')
            exec(file.read())
    except FileNotFoundError:
        print("IpPicker file not found.")
    except Exception as e:
        print(f"An error occurred while executing the file: {e}")

elif HackToolChoice == '6':
    sys.exit()

else:
    print("Invalid choice.")
