import qrcode
import os

# Ввод сайта от пользователя
site = input("Впишите сайт для создания QR-кода: ")
plik = input("Впишите, как вы хотите назвать файл изображения (с расширением .png): ")

# Функция для генерации QR-кода
def generate_qr(data, filename):
    # Определяем папку для сохранения QR-кода
    folder = "qrCodeGenerate/QRImages"
    
    # Проверяем, существует ли папка, и создаем ее, если нет
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Полный путь к файлу
    full_path = os.path.join(folder, filename)
    
    # Создаем объект QRCode
    qr = qrcode.QRCode(
        version=1,  # Версия QR-кода (размер). 1 — это 21x21, чем выше, тем больше размер.
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Уровень коррекции ошибок
        box_size=10,  # Размер каждого квадрата
        border=4  # Размер границы
    )

    # Добавляем данные в QR-код
    qr.add_data(data)
    qr.make(fit=True)

    # Создаем изображение
    img = qr.make_image(fill='black', back_color='white')

    # Сохраняем изображение
    img.save(full_path)

    print(f"QR-код успешно сохранен как {full_path}")

# Пример использования:
data_to_encode = site  # Данные для кодирования
generate_qr(data_to_encode, plik + ".png")  # Добавляем расширение .png, если его нет
