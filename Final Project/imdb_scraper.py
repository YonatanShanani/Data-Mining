from bs4 import BeautifulSoup
import requests
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Initialize WebDriver
driver = webdriver.Chrome()

# Downloading IMDb top 250 movie's data
url = 'http://www.imdb.com/chart/top'
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time if necessary

# Getting page source and parsing with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
movies = soup.select('td.titleColumn')
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]

# Create an empty list for storing movie information
movie_list = []

# Iterating over movies to extract each movie's details
for index in range(len(movies)):
    # Separating movie into: 'place', 'title', 'year'
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    media_title = movie[len(str(index)) + 1:-7]
    year = re.search(r'\((.*?)\)', movie_string).group(1)
    place = movie[:len(str(index)) - (len(movie))]

    # Splitting the crew into director and actors
    director, actors = crew[index].split('(dir.), ')

    data = {
        "place": place.strip(),
        "media_title": media_title.strip(),
        "rating": ratings[index],
        "year": year,
        "director": director.strip(),
        "actors": actors.strip()
    }
    movie_list.append(data)

# Printing movie details with its rating
for movie in movie_list:
    print(movie['place'], '-', movie['movie_title'], '(' + movie['year'] + ') -',
          'Director:', movie['director'], 'Actors:', movie['actors'], 'Rating:', movie['rating'])

# Create the output directory if it doesn't exist
output_dir = '3-Villians Heatmap/output'
os.makedirs(output_dir, exist_ok=True)

# Exporting data to a JSON file in the output directory
output_file_path = os.path.join(output_dir, 'imdb_movies_and_directors.json')
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(movie_list, f, ensure_ascii=False, indent=4)

# Close the WebDriver
driver.quit()
