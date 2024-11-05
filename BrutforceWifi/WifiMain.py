import os

print('1 - Regular hack')
print('2 - Bruteforce wifi')
print('PS You can enter " --help" for more information (For example 1 --help)')

def choise():
    return input("> ")  # Возвращаем значение, введенное пользователем

# Получаем выбор пользователя
selected_hack = choise()

if selected_hack == "1":
    exec(open('BrutforceWifi/WifiHack.py', 'r', encoding='utf-8').read())

elif selected_hack == "2":
    exec(open('BrutforceWifi/WifiHack1.py', 'r', encoding='utf-8').read())

if selected_hack == "1 --help":
    print("First, a DDoS attack is carried out on the network until it is turned off, and then the same network (access point) is created to obtain the password.")

elif selected_hack == "2 --help":
    print("Bruteforce wifi help: This method attempts to crack the WiFi password by trying many combinations.")
d