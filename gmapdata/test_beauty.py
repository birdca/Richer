import requests
from bs4 import BeautifulSoup

url = "https://www.google.com/maps/place/%E5%A4%A7%E9%80%A3%E9%A2%A8%E5%91%B3%E9%A4%A8/@25.0272828,121.5411104,17z/data=!3m2!4b1!5s0x3442aa2c1310c087:0x82ea7c7f4fc12ea1!4m6!3m5!1s0x3442aa2c135ca9a7:0x6edab384883d0090!8m2!3d25.027278!4d121.5436853!16s%2Fg%2F1tl_jdp3?entry=ttu"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.text, "html.parser")

# Find all the anchor tags (a) containing href attributes
anchors = soup.find_all("a", href=True)

# Extract the URLs
urls = [anchor["href"] for anchor in anchors]

# Print the URLs
for url in urls:
    print(url)
