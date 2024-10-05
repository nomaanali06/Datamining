#!/usr/bin/env python
# coding: utf-8

import selenium
from selenium import webdriver as wb
import time
import math
from tqdm import tqdm
import pandas as pd
import re
import csv

# Initialize WebDriver and open the first URL
links = []
url = 'https://www.zameen.com/Plots/Islamabad_9th_Avenue-3105-1.html'
webD = wb.Chrome('C:/Users/ali/Downloads/Compressed/chromedriver')
webD.get(url)

# Find the list of products and total number of plots
product_info_list = webD.find_elements_by_class_name('ef447dde')
pages = webD.find_element_by_class_name("_2aa3d08d").text

# Extract total plots from pages
d1 = []
tplots = ""
i = 0
while pages[i] != ' ':
    if pages[i].isdigit():
        d1.append(pages[i])
        tplots += pages[i]
    i += 1

tplots = int(tplots)
temp = 0

# Collect the links of plots
for i in product_info_list:
    p1 = product_info_list[temp]
    p2 = p1.find_element_by_tag_name('a')  # Reference href
    links.append(p2.get_property('href'))
    temp += 1
    if len(links) >= tplots:
        break

print(f"Total pages: {pages}")

# Calculate the total number of pages
npages = math.ceil(tplots / 25)
print(f"Total pages needed: {npages}")

# Iterate through additional pages if more than one
if npages > 1:
    for i in range(2, npages + 1):
        url = f'https://www.zameen.com/Plots/Islamabad_Gulberg-1682-{i}.html'
        webD.get(url)
        product_info_list = webD.find_elements_by_class_name('ef447dde')
        temp = 0
        for item in product_info_list:
            p1 = product_info_list[temp]
            p2 = p1.find_element_by_tag_name('a')  # Reference href
            links.append(p2.get_property('href'))
            temp += 1
            if len(links) >= tplots:
                break

print(f"Total links collected: {len(links)}")

# Scrape details of each plot using the collected links
details = []
for link in tqdm(links):
    webD.get(link)
    # Scraping different attributes of the plot
    Time = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[8]/span[2]').text
    Bath = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text
    a_string = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[1]/div/div/span').text

    id1 = [int(word) for word in a_string.split() if word.isdigit()]
    price = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[4]/div[2]/div[1]/div/form/div[1]/div/div[1]/div/div/span[3]').text
    type1 = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[1]/span[2]').text
    area = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[5]/span[2]').text
    purpose = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[6]/span[2]').text
    Location = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[3]/span[2]').text
    Bedroom = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text
    Added = webD.find_element_by_xpath(
        '//*[@id="body-wrapper"]/main/div[4]/div[2]/div[2]/div[1]').text

    # Storing the details in a dictionary
    list1 = {
        "id": id1[0],
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

# Close the WebDriver
webD.close()

# Convert scraped details into a DataFrame
dataset = pd.DataFrame(details)

# Convert price from Lakh or Crore to million
def lactomillion(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0]) / 10
    return million1

def croretomillion(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0]) * 10
    return million1

# Apply conversion on price
for i in range(0, len(dataset['Price'])):
    word = str(dataset['Price'][i])
    abc = str(dataset['Price'][i])
    if 'Lakh' in word:
        dataset.at[i, 'Price'] = lactomillion(abc)
    elif 'Crore' in word:
        dataset.at[i, 'Price'] = croretomillion(abc)

# Convert area from Marla or Kanal to square feet
def marlatosq(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0]) * 25.29
    return million1

def kanaltosq(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0]) * 506
    return million1

# Apply conversion on area
for i in range(0, len(dataset['Area'])):
    word = str(dataset['Area'][i])
    abc = str(dataset['Area'][i])
    if 'Kanal' in word:
        dataset.at[i, 'Area'] = kanaltosq(abc)
    elif 'Marla' in word:
        dataset.at[i, 'Area'] = marlatosq(abc)

# Save the final dataset to a CSV file
with open('zameen.csv', 'a') as f:
    dataset.to_csv(f, header=f.tell() == 0)
