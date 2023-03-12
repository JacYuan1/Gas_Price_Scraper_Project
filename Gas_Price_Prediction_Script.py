# Import the requests, BeautifulSoup libraries, datetime library, and os library
import os
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# Discord Bot Token obtained from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Discord Channel ID to upload file to and obtained from environment variables
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# Set the city names (These are the cities that you want to get the gas prices for and do not have to be capitalized, you can add more and you can also change the names to whatever you want. Please see the readme for more information.)
City1 = "toronto"

City2 = "mississauga"

City3 = "oakville"

# Set the date string using the current date in the format "Weekday, Month Day, Year"
date_str = datetime.now().strftime("%A, %B %d, %Y")

# Make a GET request to the URL and store the response content
response = requests.get("https://gaswizard.ca/gas-price-predictions/")

# Create a BeautifulSoup object from the response content, using the "html.parser" parser
soup = BeautifulSoup(response.content, "html.parser")

# Find all table rows with the "tr" tag and store them in the city_price_rows list
city_price_rows = soup.find_all("tr")

# Initialize an empty list to store the parsed data (This also contains all the scraped data.)
output = []

# Initialize another empty list to store the final output data
final_output = []

# Loop through each row in city_price_rows
for row in city_price_rows:
    # Find the first "td" element with the "gwgp-cityname" class and the first "td" element with the "gwgp-price" class
    city_element = row.find("td", class_="gwgp-cityname")
    price_element = row.find("td", class_="gwgp-price")
    
    # Check if both city_element and price_element exist
    if city_element and price_element:
        # Extract the city name by removing the last 2 characters from the text of city_element
        city = city_element.text[:-2]
        # Extract the price by getting the text of price_element
        price = price_element.text
        # Append a formatted string with the city name and price to the output list
        output.append(f"{city}: {price}")

# Loop through each item in the output list
for item in output:
    # Check if the item contains the strings contain capitalization of City1, City2, or City3; can add more cities here.
    if City1.title() in item or City2.title() in item or City3.title() in item:
        # If it does, append the item to the final_output list
        final_output.append(item)

# Create the multipart/form-data request
headers = {"Authorization": f"Bot {BOT_TOKEN}"}

# Create the file data
data = {"content": f"Gas Prices for {date_str}\n" + "-----------------------------------------\n" + "\n".join(final_output)}

# Send the request to the Discord API
response = requests.post(f"https://discord.com/api/v8/channels/{CHANNEL_ID}/messages", headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    print("File successfully uploaded to Discord.")
else:
    print(f"Failed to upload file to Discord. Response: {response.content}")