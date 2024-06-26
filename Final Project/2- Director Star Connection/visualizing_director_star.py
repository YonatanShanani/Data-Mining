import json
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup

BASE_URL = "https://www.superherodb.com"
MALE_VILLAINS_URL = f'{BASE_URL}/characters/male/villains/?set_gender=male&set_side=bad&page_nr='
FEMALE_VILLAINS_URL = f'{BASE_URL}/characters/female/villains/?set_gender=female&set_side=bad&page_nr='


def get_all_villain_links(driver, base_url, max_page):
    all_links = []

    for page_number in range(1, max_page + 1):
        url = f"{base_url}{page_number}"
        driver.get(url)
        time.sleep(1)  # Reduced wait time to 1 second
        driver.execute_script("window.stop();")  # Stop page loading

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        character_links = [BASE_URL + a['href'] for a in soup.select('div.column.col-12 ul.list-md li a')]
        all_links.extend(character_links)

    return all_links


def get_villain_details(driver, url):
    driver.get(url)
    time.sleep(1)  # Reduced wait time to 1 second
    driver.execute_script("window.stop();")  # Stop page loading
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        details = {}

        # Extracting the name from the <h1> tag
        name_tag = soup.select_one('div.columns.profile-titles h1')
        if name_tag:
            details['name'] = name_tag.text.strip()

        # No need to wait further if we have the name
        if 'name' in details:
            # Extracting Universe details from the <h3> tag with the class "fal fa-solar-system"
            universe_tag = soup.select_one('div.columns.profile-titles h3')
            if universe_tag:
                details['universe'] = universe_tag.text.strip()

            # Extracting Place of birth details
            origin_table = soup.select_one('div.column.col-8.col-md-7.col-sm-12 table.profile-table')
            if origin_table:
                for row in origin_table.select('tr'):
                    key = row.select_one('td').text.strip()
                    if key == 'Place of birth':
                        value = row.select('td')[1].text.strip()
                        details[key] = value

        return details
    except Exception as e:
        print(f"Error fetching details for {url}: {e}")
        return {}


def scrape_all_villains(driver, links):
    villains = []
    for link in links:
        details = get_villain_details(driver, link)
        if 'name' in details:
            villain = {
                'name': details['name'],
                'place_of_birth': details.get('Place of birth', 'Unknown'),
                'universe': details.get('universe', 'Unknown')
            }
            print(f"Scraped villain: {villain}")  # Debugging line
            villains.append(villain)
    return villains


def main():
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.video": 2,
        "profile.managed_default_content_settings.audio": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.automatic_downloads": 2,
        "profile.managed_default_content_settings.ads": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)

    male_villain_links = get_all_villain_links(driver, MALE_VILLAINS_URL, max_page=18)
    female_villain_links = get_all_villain_links(driver, FEMALE_VILLAINS_URL, max_page=5)

    all_villain_links = male_villain_links + female_villain_links

    villains_data = scrape_all_villains(driver, all_villain_links)

    output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    os.makedirs(output_directory, exist_ok=True)
    output_path = os.path.join(output_directory, 'villains_data.json')
    with open(output_path, 'w') as f:
        json.dump(villains_data, f, indent=4)

    print(f"Data saved to '{output_path}'")  # Debugging line

    driver.quit()


if __name__ == '__main__':
    main()
