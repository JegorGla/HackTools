import random
import string
import time
import androidhelper

def generate_random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def get_available_ssids():
    droid = androidhelper.Android()
    droid.wifiStartScan()
    time.sleep(2)  # Дать время для сканирования
    result = droid.wifiGetScanResults()
    networks = result.result
    ssids = [network['ssid'] for network in networks if network['ssid']]  # Фильтрация пустых SSID
    return ssids

if __name__ == "__main__":
    # Получение доступных SSID
    try:
        ssids = get_available_ssids()
        print("Доступные сети Wi-Fi:")
        for ssid in ssids:
            print(ssid)
        
        # Пример генерации случайного пароля
        if ssids:
            random_password = generate_random_password(12)
            print(f"Пример случайного пароля для первой сети {ssids[0]}: {random_password}")
    except Exception as e:
        print(f"Ошибка получения SSID: {e}")
