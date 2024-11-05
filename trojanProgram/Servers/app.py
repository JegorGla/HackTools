from flask import Flask, request, send_from_directory, jsonify
import os

app = Flask(__name__)

# Укажите папку для загрузок
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создание папки uploads, если она не существует
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Функция для загрузки файла."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Сохранение файла
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({'message': 'File uploaded successfully', 'file_url': f'/uploads/{file.filename}'}), 201

@app.route('/uploads/<path:filename>', methods=['GET'])
def get_file(filename):
    """Функция для получения загруженного файла."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
