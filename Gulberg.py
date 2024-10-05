#!/usr/bin/env python
# coding: utf-8

import selenium
from selenium import webdriver as wb
import math
import re
import pandas as pd
from tqdm import tqdm

# Function to convert 'Lakh' and 'Crore' values to 'Million'
def convert_price_to_million(price_str):
    """Convert price in 'Lakh' or 'Crore' to 'Million'."""
    number_str = re.findall(r"[-+]?\d*\.\d+|\d+", price_str)  # Extract numeric values from string
    if number_str:  # If any numbers found
        amount = float(number_str[0])
        if 'Lakh' in price_str:
            return amount / 10  # Convert Lakh to Million
        elif 'Crore' in price_str:
            return amount * 10  # Convert Crore to Million
    return 0.0  # Default if no match found

# Function to scrape plot links from the initial page
def scrape_initial_page(url):
    """Scrape links to plots from the initial page."""
    links = []  # List to hold plot links
    webD = wb.Chrome('C:/Users/ali/Downloads/Compressed/chromedriver')
    webD.get(url)

    # Extract total number of plots
    pages = webD.find_element_by_class_name("_2aa3d08d").text
    total_plots = int(''.join(filter(str.isdigit, pages)))  # Extract digits to get total plots

    # Extract links from the first page
    product_info_list = webD.find_elements_by_class_name('ef447dde')
    for item in product_info_list:
        link = item.find_element_by_tag_name('a').get_property('href')  # Get the plot link
        links.append(link)  # Add to the links list
        if len(links) >= total_plots:  # Stop if we have enough links
            break
    
    # Calculate total pages needed
    npages = math.ceil(total_plots / 25)  # 25 plots per page
    webD.quit()  # Close the driver
    
    return links, npages  # Return links and number of pages

# Function to scrape details from each plot link
def scrape_plot_details(links):
    """Scrape plot details from the given links."""
    details = []  # List to hold plot details
    webD = wb.Chrome('C:/Users/ali/Downloads/Compressed/chromedriver')

    for link in tqdm(links):  # Progress bar for links scraping
        webD.get(link)  # Open the plot link

        # Extract plot details using XPath
        time_added = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[8]/span[2]').text
        bath = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text
        id_str = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[1]/div/div/span').text
        price = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[2]/div[1]/div/form/div[1]/div/div[1]/div/div/span[3]').text
        type1 = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[1]/span[2]').text
        area = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[5]/span[2]').text
        purpose = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[6]/span[2]').text
        location = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[3]/span[2]').text
        bedroom = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text
        added = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[2]/div[2]/div[1]').text

        # Extract numeric ID from the string
        id_number = [int(word) for word in id_str.split() if word.isdigit()]

        # Create a dictionary to hold plot details
        details.append({
            "id": id_number[0] if id_number else None,
            "Type": type1,
            "Area": area,
            "Price": convert_price_to_million(price),  # Convert price to million
            "Purpose": purpose,
            "Location": location,
            "Bedroom": bedroom,
            "Bath": bath,
            "Added": added,
            "time": time_added,
            "link": link
        })

    webD.quit()  # Close the driver
    return details  # Return scraped details

# Main execution starts here
initial_url = 'https://www.zameen.com/Plots/Islamabad_G__8-170-1.html'
links, total_pages = scrape_initial_page(initial_url)

# If there are more pages, scrape links from additional pages
if total_pages > 1:
    for i in range(2, total_pages + 1):
        url = f'https://www.zameen.com/Plots/Islamabad_Gulberg-1682-{i}.html'
        additional_links, _ = scrape_initial_page(url)  # Scrape additional links
        links.extend(additional_links)  # Add to the main list of links

# Scrape detailed information from each plot link
details = scrape_plot_details(links)

# Convert details to a DataFrame
dataset = pd.DataFrame(details)

# Save the dataset to a CSV file
with open('zameen.csv', 'a', newline='') as f:
    dataset.to_csv(f, header=f.tell() == 0, index=False)  # Avoid writing header on append

print("Scraping completed. Data saved to 'zameen.csv'.")
