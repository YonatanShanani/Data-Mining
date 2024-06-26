import requests
from bs4 import BeautifulSoup
import json
import os
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_tv_show_links(main_url):
    print("Fetching the main page...")
    response = requests.get(main_url, headers=headers)
    if response.status_code == 403:
        print("Access forbidden, please check your headers or proxy settings.")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    tv_show_links = []

    for div in soup.find_all('div',
                             class_='ipc-poster ipc-poster--base ipc-poster--dynamic-width ipc-sub-grid-item ipc-sub-grid-item--span-2'):
        a_tag = div.find('a', class_='ipc-lockup-overlay')
        if a_tag:
            tv_show_links.append('https://www.imdb.com' + a_tag['href'])

    print(f"Found {len(tv_show_links)} TV show links.")
    return tv_show_links


def get_tv_show_name(tv_show_url):
    response = requests.get(tv_show_url, headers=headers)
    if response.status_code == 403:
        print("Access forbidden, please check your headers or proxy settings.")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    title_tag = soup.find('span', class_='hero__primary-text')
    if title_tag:
        return title_tag.text
    return None


def get_top_characters(tv_show_url):
    print(f"Fetching characters from {tv_show_url}...")
    response = requests.get(tv_show_url, headers=headers)
    if response.status_code == 403:
        print("Access forbidden, please check your headers or proxy settings.")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    characters = []

    for div in soup.find_all('div', class_='sc-bfec09a1-7 gWwKlt'):
        character_list = div.find('div', class_='title-cast-item__characters-list')
        if character_list:
            character_name = character_list.find('span', class_='sc-bfec09a1-4 kvTUwN')
            if character_name:
                characters.append(character_name.text)
            if len(characters) >= 10:
                break

    print(f"Found {len(characters)} characters.")
    return characters


def main():
    main_url = "https://www.imdb.com/search/title/?title_type=tv_series&moviemeter=1,100"
    tv_show_links = get_tv_show_links(main_url)

    tv_show_data = []
    for idx, tv_show_url in enumerate(tv_show_links):
        tv_show_name = get_tv_show_name(tv_show_url)
        if tv_show_name:
            print(f"Processing TV show {idx + 1}/{len(tv_show_links)}: {tv_show_name}")
            characters = get_top_characters(tv_show_url)
            tv_show_data.append({
                'tv_show_name': tv_show_name,
                'characters': characters
            })
        else:
            print(f"Failed to retrieve the name for TV show {idx + 1}")
        time.sleep(2)  # Delay to avoid being blocked

    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)

    # Save the data to a JSON file
    with open('output/tv_shows.json', 'w') as f:
        json.dump(tv_show_data, f, indent=4)

    print("Data saved to output/tv_shows.json")


if __name__ == "__main__":
    main()
