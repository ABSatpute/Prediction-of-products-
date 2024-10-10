import time
from random import randint

from bs4 import BeautifulSoup
import requests
import pandas as pd
URL = "https://www.flipkart.com/search?q=smartwatch&sid=ajy%2Cbuh&as=on&as-show=on&otracker=AS_QueryStore_HistoryAutoSuggest_1_10_na_na_na&otracker1=AS_QueryStore_HistoryAutoSuggest_1_10_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=smartwatch%7CSmart+Watches&requestId=a9a5605d-4973-49fb-a80a-53e7f13c3dcc&as-searchtext=smartwatch"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

# HTTP Request
webpage = requests.get(URL, headers=HEADERS)
#print(webpage)
# print(webpage.content)
# print(type(webpage.content))

# Parse the HTML content
soup = BeautifulSoup(webpage.content, "html.parser")
# print(soup)
links = soup.find_all("a",attrs={'class':'WKTcLC'})
# print(links)
# print(links[0])
link=links[0].get('href')
product_list="https://flipkart.com" + link
# print(product_list)
new_webpage = requests.get(product_list,headers=HEADERS)
# print(new_webpage)
new_soup = BeautifulSoup(new_webpage.content, "html.parser")
# print(new_soup)
print(new_soup.find("span",attrs={'class':'VU-ZEz'}).text)
print(new_soup.find("div",attrs={'class':'Nx9bqj CxhGGd'}).text)
print(new_soup.find("div",attrs={'class':'XQDdHH'}).text )
span_element= new_soup.find("span",attrs={'class':'Wphh3N'})
#print(span_element)

ratingsReviews_text = span_element.contents[0].text.strip()
ratingsReviews_text = span_element.contents[0].text.strip()

print(ratingsReviews_text.strip())


# Extract ratings and reviews text
ratings_and_reviews_text = span_element.text.strip()

# Split the ratings and reviews text based on " & "
# ratings_text, reviews_text = ratings_and_reviews_text.split(" & ")
# print(ratings_and_reviews_text)
# Print the extracted information
# print("Ratings:", ratings_text)
# print("Reviews:", reviews_text)


