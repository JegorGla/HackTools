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

HackToolChoice = input('Enter your number: ')

if HackToolChoice == '1':
    try:
        with open('Phishing/MainPhishing.py', 'r') as file:
            os.system('clear')
            exec(file.read())
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка при выполнении файла: {e}")
