import socket
import threading

# Список для хранения открытых портов
open_ports = []

def scan_port(target_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # Установка таймаута на 1 секунду
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"Порт {port} открыт.")
            open_ports.append(port)


def scan_ports(target_ip, port_range):
    threads = []
    
    for port in port_range:
        thread = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(thread)
        thread.start()  # Запуск потока
    
    for thread in threads:
        thread.join()  # Ожидание завершения всех потоков

if __name__ == "__main__":
    target_ip = input("Введите IP-адрес для сканирования: ")
    port_range = range(1, 65536)  # Сканируем все порты
    scan_ports(target_ip, port_range)
    
    if open_ports:
        print(f"Открытые порты: {open_ports}")
        with open('open_ports.txt', 'w') as f:
            for port in open_ports:
                f.write(f"{port}\n")
        
        choice = input("Хотите подключиться по SSH к открытому порту? (y/n): ").strip().lower()
        if choice == 'y':
            # Запускаем скрипт SSH-подключения
            import subprocess
            subprocess.run(["python", "ScanPort/SSHConnect.py", target_ip])
        else:
            print("Выход из программы.")
    else:
        print("Нет открытых портов.")
