import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Style, init

# Инициализация Colorama
init(autoreset=True)

# Список сайтов для поиска
SITES = {
    'GitHub': 'https://github.com/{}',
    'Twitter': 'https://twitter.com/{}',
    'Reddit': 'https://www.reddit.com/user/{}',
    'Instagram': 'https://www.instagram.com/{}/',
    'LinkedIn': 'https://www.linkedin.com/in/{}',
    'Pinterest': 'https://www.pinterest.com/{}/',
    'StackOverflow': 'https://stackoverflow.com/users/story/{}',
    'HackerRank': 'https://www.hackerrank.com/{}',
    'Medium': 'https://medium.com/@{}',
    'VK': 'https://vk.com/{}',
    'Twitch': 'https://www.twitch.tv/{}',
    'Steam': 'https://steamcommunity.com/id/{}',
    'Tumblr': 'https://{}.tumblr.com/',
    'LastFM': 'https://www.last.fm/user/{}',
    'GitLab': 'https://gitlab.com/{}',
    'Flickr': 'https://www.flickr.com/people/{}/',
    'MySpace': 'https://myspace.com/{}',
    'SoundCloud': 'https://soundcloud.com/{}',
    'DeviantArt': 'https://www.deviantart.com/{}',
    'YouTube': 'https://www.youtube.com/c/{}',
    '500px': 'https://500px.com/{}',
    'Facebook': 'https://www.facebook.com/{}'  # Добавление Facebook
}

def extract_phone_numbers(text):
    """Функция для извлечения номеров телефонов из текста"""
    phone_regex = re.compile(r'(?:(?:\+?\d{1,3})?[-.\s]?)?(?:(?:\(?\d{1,4}?\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})')
    phone_numbers = phone_regex.findall(text)
    
    # Обработка номеров для удаления дубликатов и лишних пробелов
    valid_phone_numbers = set()
    for num in phone_numbers:
        cleaned_num = re.sub(r'\D', '', num)  # Удаление всех нецифровых символов
        if 10 <= len(cleaned_num) <= 15:  # Проверка длины
            valid_phone_numbers.add(cleaned_num)  # Используем set для удаления дубликатов

    return list(valid_phone_numbers)

def search_profile(username):
    found_profiles = []
    for site_name, url in SITES.items():
        profile_url = url.format(username)
        try:
            response = requests.get(profile_url)
            if response.status_code == 200:
                print(Fore.GREEN + f"{site_name} profile for '{username}' found:")
                print(Fore.GREEN + f"URL: {profile_url}")
                
                # Извлечение данных о профиле
                soup = BeautifulSoup(response.text, 'html.parser')
                profile_text = soup.get_text()
                phone_numbers = extract_phone_numbers(profile_text)
                
                if phone_numbers:
                    print(Fore.GREEN + f"Phone numbers found: {phone_numbers}")
                else:
                    print(Fore.RED + "No phone numbers found.")
                
                found_profiles.append((site_name, profile_url, phone_numbers))
            else:
                print(Fore.RED + f"{site_name} profile for '{username}' not found.")
        except Exception as e:
            print(Fore.RED + f"Error accessing {site_name}: {e}")
    
    return found_profiles

def main():
    username = input("Enter username or email to search: ")
    found_profiles = search_profile(username)
    
    if found_profiles:
        print("\n" + Fore.GREEN + "Profiles found:")
        for site_name, profile_url, phone_numbers in found_profiles:
            print(Fore.GREEN + f"{site_name}: {profile_url}")
            if phone_numbers:
                print(Fore.GREEN + f"  Phone numbers: {phone_numbers}")
    else:
        print(Fore.RED + "No profiles found for the given username.")

if __name__ == "__main__":
    main()
