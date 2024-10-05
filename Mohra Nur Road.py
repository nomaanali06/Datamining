#!/usr/bin/env python
# coding: utf-8

import re
import math
import time
import pandas as pd
from tqdm import tqdm
from selenium import webdriver as wb

# Function to convert price from Lakh to Million
def lactomillion(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0]) / 10  # Convert Lakh to Million
    return million1

# Function to convert price from Crore to Million
def croretomillion(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0]) * 10  # Convert Crore to Million
    return million1

# Function to convert area from Marla to Square Feet
def marlatosq(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0]) * 25.29  # Convert Marla to Square Feet
    return million1

# Function to convert area from Kanal to Square Feet
def kanaltosq(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0]) * 506  # Convert Kanal to Square Feet
    return million1

# Initialize the web driver
url = 'https://www.zameen.com/Plots/Islamabad_Mohra_Nur_Road-12800-1.html'
webD = wb.Chrome('C:/Users/ali/Downloads/Compressed/chromedriver')
webD.get(url)

# Get total plots from the first page
product_info_list = webD.find_elements_by_class_name('ef447dde')
pages = webD.find_element_by_class_name("_2aa3d08d").text
tplots = int(''.join(filter(str.isdigit, pages)))  # Extract digits and convert to int
links = []

# Collect links to all plots on the first page
for product in product_info_list:
    p2 = product.find_element_by_tag_name('a')  # Reference link
    links.append(p2.get_property('href'))
    if len(links) >= tplots:
        break

# Calculate the total number of pages
npages = math.ceil(tplots / 25)

# If there are more pages, collect links from those pages
if npages > 1:
    for i in range(2, npages + 1):
        url = f'https://www.zameen.com/Plots/Islamabad_Gulberg-1682-{i}.html'
        webD.get(url)
        product_info_list = webD.find_elements_by_class_name('ef447dde')
        for product in product_info_list:
            p2 = product.find_element_by_tag_name('a')  # Reference link
            links.append(p2.get_property('href'))
            if len(links) >= tplots:
                break

# Gather detailed information about each plot
details = []
for link in tqdm(links):
    webD.get(link)
    time.sleep(1)  # Small delay to allow page to load

    # Extract relevant information using XPath
    try:
        Time = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[8]/span[2]').text
        Bath = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text
        a_string = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[1]/div/div/span').text
        id1 = [int(word) for word in a_string.split() if word.isdigit()]  # Extract numeric IDs
        price = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[2]/div[1]/div/form/div[1]/div/div[1]/div/div/span[3]').text
        type1 = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[1]/span[2]').text
        area = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[5]/span[2]').text
        purpose = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[6]/span[2]').text
        Location = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[3]/span[2]').text
        Bedroom = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text                                       
        Added = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[2]/div[2]/div[1]').text

        # Create a dictionary with plot details
        list1 = {
            "id": id1[0] if id1 else None,
            "Type": type1,
            "Area": area,
            "Price": price,
            "Purpose": purpose,
            "Location": Location,
            "Bedroom": Bedroom,
            "Bath": Bath,
            "Added": Added,
            "time": Time,
            "link": link
        }
        details.append(list1)
    except Exception as e:
        print(f"Error fetching details for {link}: {e}")

# Convert the collected details into a DataFrame
dataset = pd.DataFrame(details)

# Convert price to million format
for i in range(len(dataset['Price'])):
    word = str(dataset['Price'][i])
    if 'Lakh' in word:
        dataset['Price'][i] = lactomillion(word)
    elif 'Crore' in word:
        dataset['Price'][i] = croretomillion(word)

# Convert area to square feet
for i in range(len(dataset['Area'])):
    word = str(dataset['Area'][i])
    if 'Kanal' in word:
        dataset['Area'][i] = kanaltosq(word)
    elif 'Marla' in word:
        dataset['Area'][i] = marlatosq(word)

# Save the dataset to a CSV file
dataset.to_csv('zameen.csv', mode='a', header=not pd.io.common.file_exists('zameen.csv'))

# Close the web driver
webD.quit()
