import requests
from bs4 import BeautifulSoup
import os
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
    '500px': 'https://500px.com/{}'
}

def search_profile(username):
    found_profiles = []
    for site_name, url in SITES.items():
        profile_url = url.format(username)
        try:
            response = requests.get(profile_url)
            if response.status_code == 200:
                print(Fore.GREEN + f"{site_name} profile for {username} found:")
                print(Fore.GREEN + f"URL: {profile_url}")
                found_profiles.append((site_name, profile_url))
            else:
                print(Fore.RED + f"{site_name} profile for {username} not found.")
        except Exception as e:
            print(Fore.RED + f"Error accessing {site_name}: {e}")
    
    return found_profiles

def main():
    username = input("Enter username or email to search: ")
    found_profiles = search_profile(username)
    
    if found_profiles:
        print("\n" + Fore.GREEN + "Profiles found:")
        for site_name, profile_url in found_profiles:
            print(Fore.GREEN + f"{site_name}: {profile_url}")
    else:
        print(Fore.RED + "No profiles found for the given username.")

if __name__ == "__main__":
    main()
