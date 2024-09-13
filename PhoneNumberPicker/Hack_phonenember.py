import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import random
import requests  # Для проверки через сторонние сервисы
import os
import time

# Список кодов мест для Польши
polish_city_codes = ['12', '22', '42', '52', '61', '71', '81', '91']

# Список кодов мест для России
russian_city_codes = ['495', '499', '812', '863', '862', '861', '831', '843', '844', '846', '343', '351', '347', '342', '381', '383', '3952', '391', '421', '423', '3462']

def generate_phone_number():
    """Генерация случайного номера для Польши или России."""
    city_code = random.choice(polish_city_codes + russian_city_codes)
    
    if city_code in polish_city_codes:
        country_code = "+48"
    elif city_code in russian_city_codes:
        country_code = "+7"
    
    # Генерация номера телефона с выбранным кодом места
    first_seven_numbers = str(random.randint(1000000, 9999999))
    return f"{country_code}{city_code}{first_seven_numbers}"

def generate_valid_number(api_key, numverify_api_key):
    """Генерация действительного номера."""
    while True:
        phone = generate_phone_number()

        # Проверяем, существует ли номер
        result = check_number(phone, api_key, numverify_api_key)
        if "Phone Number" in result:  # Если результат содержит данные о номере
            return phone
        else:
            print("Generated invalid number, trying again...")

def check_number(phone, api_key, numverify_api_key):
    """Проверка номера телефона на существование."""
    try:
        # Проверка через NumVerify
        numverify_result = check_number_with_numverify(phone, numverify_api_key)
        if "Phone Number" in numverify_result:
            return numverify_result

        # Если NumVerify не дал результатов, проверяем с помощью OpenCage
        check_phone = phonenumbers.parse(phone)
        number_location = geocoder.description_for_number(check_phone, "en")
        service_provider = carrier.name_for_number(check_phone, "en")
    
        geocoder_instance = OpenCageGeocode(api_key)
        query = str(number_location)
        result = geocoder_instance.geocode(query)
        
        if not result:
            return "No geocoding result found for this location."

        lat = result[0]['geometry']['lat']
        lng = result[0]['geometry']['lng']
    
        return f"Phone Number: {phone}\nLocation: {number_location}\nService Provider: {service_provider}\nLatitude: {lat}, Longitude: {lng}"
    except phonenumbers.phonenumberutil.NumberParseException:
        return "Phone number does not exist."
    except Exception as e:
        return f"An error occurred: {e}"

def check_number_with_numverify(phone_number, api_key):
    """Проверка номера через NumVerify API."""
    url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}"
    response = requests.get(url)
    data = response.json()
    
    if data['valid']:
        return (f"Phone Number: {data['number']}\n"
                f"Country Code: {data['country_code']}\n"
                f"Location: {data['location']}\n"
                f"Carrier: {data['carrier']}\n"
                f"Line Type: {data['line_type']}")
    else:
        return "Phone number is invalid or not found."

def main():
    api_key = input("Please enter your OpenCage API key: ")
    numverify_api_key = input("Please enter your NumVerify API key: ")

    while True:
        print("\nOptions:")
        print("1. Generate Random Phone Number")
        print("2. Check Phone Number")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            phone = generate_valid_number(api_key, numverify_api_key)
            print(f"Generated Phone Number: {phone}")
            print("Очистка через 10 секунд")
            time.sleep(10)
        elif choice == '2':
            phone = input("Enter the phone number to check: ")
            result = check_number(phone, api_key, numverify_api_key)
            print(result)
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
