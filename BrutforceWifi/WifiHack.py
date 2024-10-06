import pywifi
import time
import os

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Используем первый доступный интерфейс
    iface.scan()  # Запускаем сканирование Wi-Fi сетей
    time.sleep(5)  # Ждём завершения сканирования
    networks = iface.scan_results()

    if not networks:
        print("Не найдено доступных Wi-Fi сетей.")
        return []

    network_list = []
    for i, network in enumerate(networks):
        ssid = network.ssid
        bssid = network.bssid
        signal = network.signal
        print(f"{i + 1}. SSID: {ssid}, BSSID: {bssid}, Signal: {signal}")
        network_list.append((ssid, bssid, signal))
    
    return network_list

def choose_network(networks):
    while True:
        try:
            choice = int(input("\nВыберите сеть для дальнейших действий (введите номер): ")) - 1
            if 0 <= choice < len(networks):
                selected_network = networks[choice]
                print(f"\nВы выбрали сеть: SSID: {selected_network[0]}, BSSID: {selected_network[1]}")
                return selected_network
            else:
                print("Некорректный выбор. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите номер сети.")

def create_wifi_hotspot(ssid):
    # Устанавливаем точку доступа с тем же SSID и без пароля
    os.system(f'netsh wlan set hostednetwork mode=allow ssid={ssid} key=""')
    os.system('netsh wlan start hostednetwork')
    print(f"Точка доступа {ssid} запущена без пароля.")

def stop_wifi_hotspot():
    os.system('netsh wlan stop hostednetwork')
    print("Точка доступа остановлена.")

if __name__ == "__main__":
    available_networks = scan_wifi()
    if available_networks:
        selected_network = choose_network(available_networks)
        ssid = selected_network[0]  # Получаем SSID выбранной сети
        create_wifi_hotspot(ssid)    # Создаём точку доступа с тем же SSID

        # Остановка точки доступа (если нужно)
        # stop_wifi_hotspot()
