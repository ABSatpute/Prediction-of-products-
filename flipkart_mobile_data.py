import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime
import time
import random

# Initialize lists
Product_name = []
Price = []
Description = []
Ratings = []
Timestamps = []

# Base URL without page number
base_url = "https://www.flipkart.com/search?q=mobiles+under+50000&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_8_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_8_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=mobiles+under+50000&requestId=23fe398a-e6db-45d7-b519-5a40e5668d61&page="


def fetch_page(url, headers):
    backoff_time = 1
    while True:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as e:
            if r.status_code == 429:
                print(f"Rate limit exceeded. Waiting {backoff_time} seconds before retrying...")
                time.sleep(backoff_time)
                backoff_time *= 2
                if backoff_time > 64:
                    raise
            else:
                raise
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}. Retrying...")
            time.sleep(backoff_time)
            backoff_time *= 2
            if backoff_time > 64:
                raise


# Rotate User-Agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# Use session for persistent connections
session = requests.Session()

for i in range(1, 100):  # Adjust the range if necessary
    url = base_url + str(i)
    HEADERS = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US, en;q=0.5'
    }

    # Record the start time
    start_time = datetime.now()

    try:
        print(f"Scraping page {i}...")
        r = fetch_page(url, HEADERS)
        soup = BeautifulSoup(r.text, "lxml")
        box = soup.find("div", class_="DOjaWF YJG4Cf")

        if box is None:
            print(f"No content found on page {i}.")
            break  # Exit loop if no content is found

        names = box.find_all("div", class_="KzDlHZ")
        prices = box.find_all("div", class_="Nx9bqj _4b5DiR")
        desc = box.find_all("ul", class_="G4BRas")
        rating = box.find_all("div", class_="XQDdHH")

        for j in range(len(names)):
            Product_name.append(names[j].text)

            if j < len(prices):
                Price.append(prices[j].text)
            else:
                Price.append(np.nan)

            if j < len(desc):
                Description.append(desc[j].text)
            else:
                Description.append(np.nan)

            if j < len(rating):
                Ratings.append(rating[j].text)
            else:
                Ratings.append(np.nan)

            Timestamps.append(start_time)

        print(f"Scraped page {i}: {len(Product_name)} products found.")

    except Exception as e:
        print(f"An error occurred on page {i}: {e}")

    # Sleep for 2 seconds before loading the next page
    time.sleep(random.uniform(2, 5))  # Randomize delay to mimic human behavior

# Create a DataFrame with timestamps
data = pd.DataFrame({
    'Product Name': Product_name,
    'Price': Price,
    'Description': Description,
    'Ratings': Ratings,
    'Timestamp': Timestamps
})

# Save DataFrame to CSV
output_path = "D:\\Web Scraping\\Scraped_Data1.csv"
data.to_csv(output_path, index=False)

print(f"Data saved to {output_path}")
