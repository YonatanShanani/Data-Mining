### IMPORTS ###
import json, time, os, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

### GLOBAL ARGS ###
SCRAPING_WEBSITE = "https://www.indiegogo.com/explore/home?project=all&project=all&sort=trending"
NUM_OF_ITEMS = 300

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.get(SCRAPING_WEBSITE)
driver.implicitly_wait(5)

body = driver.find_element(By.CSS_SELECTOR, 'body')

# Scroll and click "Show More" button to load more items
for i in range(NUM_OF_ITEMS // 12):  # Adjust this divisor based on the average items loaded per click/scroll
    try:
        show_more_button = driver.find_element(By.XPATH, '//button[@gogo_test="show_more"]')
        if show_more_button:
            show_more_button.click()
            time.sleep(1)  # Wait for the page to load new content
    except Exception as e:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # Wait for the page to load new content
    print(f"Loading more items... Iteration {i+1}")

# Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all project URLs
project_links = []
for a in soup.select('a[href*="/projects/"]'):
    href = a['href']
    if href.startswith('/projects/'):
        project_links.append(f"https://www.indiegogo.com{href}")

# Print the number of project links found for debugging
print(f"Number of project links found: {len(project_links)}")

records = []
for idx, project_url in enumerate(project_links[:NUM_OF_ITEMS], start=1):
    try:
        driver.get(project_url)
        driver.implicitly_wait(3)
        project_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extracting data from the individual project page
        project_title_div = project_soup.find('div', class_='basicsSection-title')
        project_title = project_title_div.get_text(strip=True) if project_title_div else 'N/A'

        project_text_div = project_soup.find('div', class_='basicsSection-tagline')
        project_text = project_text_div.get_text(strip=True) if project_text_div else 'N/A'

        dollars_pledged_div = project_soup.find('div', class_='basicsGoalProgress-amountTowardsGoal')
        dollars_pledged_text = dollars_pledged_div.get_text(strip=True) if dollars_pledged_div else 'N/A'
        dollars_pledged = re.findall(r'\d+', dollars_pledged_text.replace(',', ''))
        dollars_pledged = dollars_pledged[0] if dollars_pledged else 'N/A'

        # Extracting the correct DollarsGoal
        dollars_goal_div = project_soup.find('span', class_='basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised')
        dollars_goal_text = dollars_goal_div.get_text(strip=True) if dollars_goal_div else 'N/A'
        dollars_goal_matches = re.findall(r'of ₪(\d+)', dollars_goal_text.replace(',', ''))
        dollars_goal = dollars_goal_matches[0] if dollars_goal_matches else 'N/A'

        num_backers_div = project_soup.find('span', class_='basicsGoalProgress-claimedOrBackers')
        num_backers_text = num_backers_div.get_text(strip=True) if num_backers_div else 'N/A'
        num_backers = re.findall(r'\d+', num_backers_text)
        num_backers = num_backers[0] if num_backers else 'N/A'

        days_to_go_div = project_soup.find('div', class_='basicsGoalProgress-progressDetails-detailsTimeLeft')
        days_to_go = re.findall(r'\d+', days_to_go_div.get_text(strip=True))[0] if days_to_go_div else 'InDemand'

        flexible_goal_div = project_soup.find('span', class_='basicsGoalProgress-progressDetails-detailsGoal-goalPopover')
        flexible_goal = 'True' if flexible_goal_div and 'Flexible Goal' in flexible_goal_div.get_text(strip=True) else 'False'

        creators_div = project_soup.find('div', class_='basicsCampaignOwner-details-name')
        creators_text = creators_div.get_text() if creators_div else 'N/A'
        creators = creators_text.split('\n')[1].strip() if '\n' in creators_text else creators_text.strip()

        # Debugging print statements
        print(f"Project ID: {idx}")
        print(f"Project URL: {project_url}")
        print(f"Project Title: {project_title}")
        print(f"Project Text: {project_text}")
        print(f"Dollars Pledged: {dollars_pledged}")
        print(f"Dollars Goal: {dollars_goal}")
        print(f"Num Backers: {num_backers}")
        print(f"Days To Go: {days_to_go}")
        print(f"Flexible Goal: {flexible_goal}")
        print(f"Creators: {creators}")

        records.append({
            'id': str(idx),
            'url': project_url,
            'Creators': creators,
            'Title': project_title,
            'Text': project_text,
            'DollarsPledged': dollars_pledged,
            'DollarsGoal': dollars_goal,
            'NumBackers': num_backers,
            'DaysToGo': days_to_go,
            'FlexibleGoal': flexible_goal
        })
    except Exception as e:
        print(f"Error extracting project {project_url}: {e}")

# Structure the data as specified
data = {
    "records": {
        "record": records
    }
}

# Define the output directory outside the current folder
output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')
os.makedirs(output_directory, exist_ok=True)

# Export data to JSON in the output directory
output_path = os.path.join(output_directory, 'problem1.json')
with open(output_path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"Data successfully saved to {output_path}")
