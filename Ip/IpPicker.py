import requests

def get_ip_info(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == "__main__":

    ip = input("Ведите ip: ")
    ip = ip # Пример IP-адреса, замените на нужный
    
    info = get_ip_info(ip)
    
    if info and info['status'] == 'success':
        print(f"IP: {info.get('query')}")
        print(f"Город: {info.get('city')}")
        print(f"Регион: {info.get('regionName')}")
        print(f"Страна: {info.get('country')}")
        print(f"Организация: {info.get('org')}")
        print(f"Местоположение: {info.get('lat')}, {info.get('lon')}")
        print(f"Почтовый индекс: {info.get('zip')}")
        print(f"Временная зона: {info.get('timezone')}")
    else:
        print("Не удалось получить информацию о IP-адресе.")
