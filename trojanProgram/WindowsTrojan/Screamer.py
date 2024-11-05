import yt_dlp

def download_video(url, path='.'):
    try:
        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Скачиваю: {url}")
            ydl.download([url])
            print("Скачивание завершено!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
video_url = 'https://youtu.be/5p5d1vflc_g'
download_video(video_url, path=r'C:\Games')
