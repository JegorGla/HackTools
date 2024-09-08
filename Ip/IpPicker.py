import requests
import webbrowser

def get_ip_info(ip):
    url = f"https://ipinfo.io/{ip}/json"  # Используем правильный URL для запроса информации о конкретном IP
    try:
        response = requests.get(url, timeout=5)  # Добавляем тайм-аут для запроса
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка: не удалось получить данные. Код состояния {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
        return None

def open_map(lat, lon):
    map_url = f"https://www.google.com/maps?q={lat},{lon}"
    webbrowser.open(map_url)

if __name__ == "__main__":
    ip = input("Введите IP-адрес: ")
    
    info = get_ip_info(ip)
    
    if info:
        print(f"\nИнформация о IP-адресе {info.get('ip', 'Неизвестно')}:")
        print(f"Город: {info.get('city', 'Неизвестно')}")
        print(f"Регион: {info.get('region', 'Неизвестно')}")
        print(f"Страна: {info.get('country', 'Неизвестно')}")
        print(f"Организация: {info.get('org', 'Неизвестно')}")
        print(f"Местоположение: {info.get('loc', 'Неизвестно')}")
        print(f"Почтовый индекс: {info.get('postal', 'Неизвестно')}")
        print(f"Временная зона: {info.get('timezone', 'Неизвестно')}")

        OpenMap = input("Хотите открыть карту с этим местоположением? (Yes/No): ").strip().lower()
        if OpenMap == "yes":
            loc = info.get('loc', '0,0').split(',')
            if len(loc) == 2:
                lat, lon = loc
                open_map(lat, lon)
        else:
            print("Карта не будет открыта.")
    else:
        print("Не удалось получить информацию о IP-адресе.")
