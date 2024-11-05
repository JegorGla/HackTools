import os
import time
import subprocess
import threading

def compile_rat_script():
    """Компилирует RatScript (здесь просто создаем файл)."""
    script_name = "trojanProgram/Servers/Server(CMD).py"  # Имя вашего RatScript
    
    # Логика компиляции. Здесь можно добавить свой код компиляции
    print(f"Компилируем {script_name}...")
    time.sleep(2)  # Симуляция времени компиляции
    
    # Создаем простой файл скрипта для примера
    with open(script_name, 'w') as f:
        f.write("# Это скомпилированный скрипт RatScript\nprint('Скрипт запущен!')\n")
    
    print(f"{script_name} успешно скомпилирован.")

def run_flask_server():
    """Запускает Flask сервер."""
    flask_server = "trojanProgram/Servers/app.py"  # Имя вашего Flask сервера
    
    if os.path.exists(flask_server):
        print(f"Запускаем Flask сервер...")
        subprocess.run(["python", flask_server])  # Запускаем сервер
    else:
        print(f"Файл {flask_server} не найден. Пожалуйста, сначала убедитесь, что он существует.")

def run_rat_script():
    """Запускает RatScript."""
    script_name = "trojanProgram/Servers/Server(CMD).py"  # Имя вашего RatScript
    
    if os.path.exists(script_name):
        print(f"Запускаем {script_name}...")
        subprocess.run(["python", script_name])  # Запускаем скрипт
    else:
        print(f"Файл {script_name} не найден. Пожалуйста, сначала скомпилируйте его.")

def main():
    while True:
        print('1 - Компилировать мой RatScript')
        print('2 - Запустить Flask сервер и RatScript')
        print('3 - Выход')
        choice = input("Выберите, что вы хотите сделать: ").strip()

        if choice == '1':
            compile_rat_script()
        elif choice == '2':
            # Запускаем Flask сервер и RatScript в отдельных потоках
            flask_thread = threading.Thread(target=run_flask_server)
            rat_script_thread = threading.Thread(target=run_rat_script)

            flask_thread.start()
            rat_script_thread.start()

            # Ожидаем завершения потоков
            flask_thread.join()
            rat_script_thread.join()
        elif choice == '3':
            print("Выход...")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
