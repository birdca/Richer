import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# # Set up the WebDriver
# driver = webdriver.Chrome('/path/to/chromedriver')
#
# # Go to Google Maps
# driver.get('https://www.google.com/maps')
#
# # Wait for the page to load
# time.sleep(5)
#
# # Load the JSON data from the file
# with open('./restaurant_candidates.json', 'r') as f:
#     data = json.load(f)
#
# # Loop through each object in the data
# print(len(data))
# for index, restaurant in enumerate(data):
#     print('restaurant number:{}'.format(index))
#     print(restaurant)
#     # Find the search box
#     search_box = driver.find_element("name", "q")
#
#     # Clear the search box
#     search_box.clear()
#
#     # Type in the name of the restaurant
#     print(restaurant['name'])
#     search_box.send_keys(restaurant['name'])
#
#     # Submit the search
#     search_box.send_keys(Keys.RETURN)
#
#     # Wait for the results to load
#     time.sleep(5)
#
#     # Try to find a div that contains the text "Find a table"
#     try:
#         find_table = driver.find_element(By.XPATH, "//*[contains(text(), 'Find a table')]")
#         print(f"Found a table for {restaurant['name']}!")
#     except NoSuchElementException:
#         print(f"No table found for {restaurant['name']}.")
#
# # Close the driver
# driver.quit()


def scrape_restaurant_details(start):
    # Set up the WebDriver
    driver = webdriver.Chrome('/path/to/chromedriver')

    # Go to Google Maps
    driver.get('https://www.google.com/maps/@25.03621,121.5647692,13.42z')

    # Wait for the page to load
    time.sleep(5)

    # Load the JSON data from the file
    with open('restaurant_candidates.json', 'r') as f:
        data = json.load(f)

    # Open the CSV file in append mode
    csv_file = open('restaurant_details.csv', 'a', newline='')
    writer = csv.writer(csv_file)

    # Loop through each object in the data
    for index, restaurant in enumerate(data):
        if index < start:
            continue
        print('restaurant number:{}'.format(index))
        print(restaurant)
        # Find the search box
        search_box = driver.find_element("name", "q")

        # Clear the search box
        search_box.clear()

        # Type in the name of the restaurant
        print(restaurant['name'])
        search_box.send_keys(restaurant['name'])

        # Submit the search
        search_box.send_keys(Keys.RETURN)

        # Wait for the results to load
        # time.sleep(10)

        # Try to find the first search result and click on it
        # try:
        #     first_result = driver.find_element_by_xpath("//div[@class='section-result']")
        #     first_result.click()
        #
        #     # Wait for the place details to load
        #     time.sleep(5)

        # Find all the anchor elements on the page
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        anchor_elements = driver.find_elements(By.TAG_NAME, 'a')

        # Extract the link values from the href attributes
        link_values = [element.get_attribute('href') for element in anchor_elements]

        # Print the extracted link values
        for link in link_values:
            print(link)

            # Try to find the element with text "Find a table"
    #     try:
    #         find_table = driver.find_element(By.XPATH, "//*[contains(text(), 'Find a table')]").get_attribute('href')
    #     except NoSuchElementException:
    #         find_table = ""
    #
    #     # Try to find the element with text "Reserve a table" (case insensitive)
    #     try:
    #         reserve_table = driver.find_element(By.XPATH, "//*[contains(text(), 'Reserve a table')]").get_attribute('href')
    #     except NoSuchElementException:
    #         reserve_table = ""
    #
    #     # Find all the website links
    #     websites = ""
    #     website_links = ""
    #     try:
    #
    #         # website_links = driver.find_element(By.XPATH, "//a[starts-with(@href, 'http')]")
    #         website_links = driver.find_element(By.CSS_SELECTOR, "[data-item-id='authority']")
    #         websites = website_links.get_attribute("href")
    #     except NoSuchElementException:
    #         pass
    #
    #     # Filter and extract the valid website link
    #     # websites = ""
    #     # for link in website_links:
    #     #     href = link.get_attribute('href')
    #     #     if all(exclusion not in href for exclusion in ["www.google.com", "maps", "contrib", "support.google.com"]):
    #     #         websites.append(href)
    #
    #     # Extract the location coordinates
    #     location = f"{restaurant['geometry']['location']['lat']},{restaurant['geometry']['location']['lng']}"
    #
    #     # Write the details to the CSV file
    #     writer.writerow([restaurant['name'], restaurant.get('price_level', ''), location, find_table, reserve_table, websites])
    #
    #     # except NoSuchElementException:
    #     #     print(f"No search result found for {restaurant['name']}.")
    #
    # # Close the CSV file
    # csv_file.close()
    #
    # # Close the driver
    # driver.quit()


if __name__ == "__main__":
    scrape_restaurant_details(190)
