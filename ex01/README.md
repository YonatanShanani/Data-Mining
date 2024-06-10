
# Project Title: Indiegogo Scraper

## Introduction

This project contains a Python script that scrapes project data from the Indiegogo website. The script collects various details about the projects and saves the data in a JSON file.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation

To install and run this project, follow these steps:

1. Clone the repository or download the ZIP file.
2. Extract the contents of the ZIP file if needed.
3. Ensure you have Python installed on your system.

## Usage

### Running the Script

1. Install the required Python libraries using the following command:

    ```bash
    pip install beautifulsoup4 selenium
    ```

2. Ensure you have Chrome WebDriver installed and it is in your system PATH.

3. Run the Python script using the following command:

    ```bash
    python indiegogo_scraper.py
    ```

### Viewing the Output

The script saves the scraped data in a JSON file located in the `output` directory.

## Features

- **Web Scraping:** Collects project data from the Indiegogo website.
- **Data Export:** Saves the collected data in a JSON file.

## Dependencies

Ensure you have the following Python libraries installed:

- `beautifulsoup4`
- `selenium`

You can install these dependencies using the following command:

```bash
pip install beautifulsoup4 selenium
```

Additionally, you need to have Chrome WebDriver installed.

## Configuration

No specific configuration is needed. Ensure that the `SCRAPING_WEBSITE`, `NUM_OF_ITEMS`, and `ENTRIES_FOUND_PER_SCROLL` global variables are set according to your requirements.

## Documentation

### Code Structure

- **Imports:**
    - `json`, `time`, `os`, `re`: Standard Python libraries.
    - `BeautifulSoup`: For parsing HTML.
    - `webdriver`, `By`, `Keys`: For web automation with Selenium.

- **Global Variables:**
    - `SCRAPING_WEBSITE`: URL of the website to scrape.
    - `NUM_OF_ITEMS`: Number of items to scrape.
    - `ENTRIES_FOUND_PER_SCROLL`: Number of items found per scroll.

- **Main Sections:**
    1. **Initialization:** Set up the Selenium WebDriver.
    2. **Scrolling:** Scroll the main page to load more items.
    3. **Scraping:** Collect project URLs and scrape data from each project page.
    4. **Export:** Save the collected data to a JSON file.

### Output Files

The output directory contains the JSON file with the scraped data:

- `output/problem1.json`

## Examples

The script will print details of each project as it is scraped, such as:

```
Project ID: 1
Project URL: https://www.indiegogo.com/projects/example
Project Title: Example Project
Project Text: This is an example project.
Dollars Pledged: 1000
Dollars Goal: 5000
Num Backers: 100
Days To Go: 30
Flexible Goal: True
Creators: John Doe
```

## Troubleshooting

If you encounter issues, ensure that all dependencies are installed and that the Chrome WebDriver is correctly set up. Additionally, check that the website URL and scraping parameters are correctly set.

## Contributors

- Yehonatan Zaritsky
- Yehonatan Shanani
- Shelly Shapira
- Yonah Bar-Shain

## License

This project is licensed under the terms specified in the `LICENSE` file.
