import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# URL вашего сайта
url = input("Введите URL вашего сайта для нагрузочного тестирования: ")
number_of_requests = int(input("Введите количество запросов: "))

# Функция для отправки запроса
def send_request():
    try:
        response = requests.get(url)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

# Создаем пул потоков для параллельного выполнения
def generate_traffic(num_requests):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        for future in as_completed(futures):
            status, result = future.result()
            if status:
                print(f'Successfully accessed {url} with status code {status}')
            else:
                print(f'Request error: {result}')

# Запускаем генерацию трафика
if __name__ == "__main__":
    generate_traffic(number_of_requests)
