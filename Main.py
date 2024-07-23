import os
import pyfiglet
from colorama import init, Fore

# Инициализируем colorama для поддержки цветового вывода
init()

# Функция для плавного изменения цвета заголовка
def gradient_color(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    gradient_text = ""
    for i, char in enumerate(text):
        gradient_text += colors[i % len(colors)] + char
    return gradient_text

# Выводим заголовок с плавным переходом цвета
print(gradient_color(pyfiglet.figlet_format("ALL HACKING TOOLS", font='starwars')))

name = input('Enter your name: ')
print('Hello, ', name)

print('1 - phishing tool')
print('2 - PhoneNumber Picker')
print('3 - DDoS Atack')
print('4 - Exit')

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

if HackToolChoice == '2':
    try:
        with open('PhoneNumberPicker/Hack_phonenember.py', 'r', encoding='utf-8') as file:
            os.system('cls')
            exec(file.read())
    except FileNotFoundError:
        print("Main Phishing file not found.")
    except Exception as e:
        print(f"An error occurred while executing the file: {e}")

if HackToolChoice == '3':
    try:
        with open('DDoSAtack/DDoSAtack.py', 'r', encoding='utf-8') as file:
            os.system('cls')
            exec(file.read())
    except FileNotFoundError:
        print("DDoSAtack file not found.")
    except Exception as e:
        print(f"An error occurred while executing the file: {e}")

if HackToolChoice == '4':
    os.exit()