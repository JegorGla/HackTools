import subprocess

def set_static_ip(interface, ip_address, subnet_mask, gateway):
    try:
        # Установка статического IP
        subprocess.run(f"netsh interface ip set address name=\"{interface}\" static {ip_address} {subnet_mask} {gateway}", check=True, shell=True)
        
        # Установка DNS-сервера (можно изменить на нужный вам DNS)
        subprocess.run(f"netsh interface ip set dns name=\"{interface}\" static 8.8.8.8", check=True, shell=True)
        
        print(f"Статический IP-адрес {ip_address} успешно установлен на интерфейс {interface}.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при установке статического IP: {e}")

# Замените значения ниже на свои
interface_name = "Wi-Fi"  # Имя вашего интерфейса
ip = "192.168.1.69"       # Желаемый статический IP
subnet = "255.255.255.0"   # Маска подсети
gateway = "192.168.1.1"     # Шлюз

set_static_ip(interface_name, ip, subnet, gateway)
