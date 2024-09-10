from scapy.all import ARP, Ether, srp

def scan_network(ip_range):
    # Создаём запрос ARP для указанного диапазона IP-адресов
    arp_request = ARP(pdst=ip_range)
    # Создаём Ethernet-кадр для широковещательной рассылки
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Объединяем кадр Ethernet и ARP-запрос
    arp_request_broadcast = broadcast/arp_request
    # Отправляем пакет и получаем ответ
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    devices = []
    for sent, received in answered_list:
        # Для каждого ответа добавляем IP и MAC адрес устройства
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices

def print_devices(devices):
    print("Найденные устройства в сети:")
    print("IP-адрес\t\tMAC-адрес")
    for device in devices:
        print(f"{device['ip']}\t{device['mac']}")

if __name__ == "__main__":
    # Укажите диапазон IP-адресов в зависимости от вашей сети
    # Например, 192.168.1.1/24 для локальной сети
    ip_range = "192.168.1.26/24"
    devices = scan_network(ip_range)
    print_devices(devices)
