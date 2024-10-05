#!/usr/bin/env python
# coding: utf-8

# Import necessary libraries
import selenium
from selenium import webdriver as wb
import time
import math
import re  # Add import for regular expressions

# Initialize an empty list to hold plot links
links = []
url = 'https://www.zameen.com/Plots/Islamabad_Akbar_Town-1398-1.html'
webD = wb.Chrome('C:/Users/ali/Downloads/Compressed/chromedriver')  # Path to ChromeDriver
webD.get(url)  # Open the URL

# Get product info elements and page information
product_info_list = webD.find_elements_by_class_name('ef447dde')
pages = webD.find_element_by_class_name("_2aa3d08d").text
d1 = []
tplots = ""
i = 0

# Extract the number of plots from the page text
while pages[i] != ' ':
    if pages[i].isdigit():
        d1.append(pages[i])
        tplots = tplots + pages[i]
    i = i + 1
    
tplots = int(tplots)  # Convert total plots to an integer
temp = 0

# Extract links from the product info list
for i in product_info_list:
    p1 = product_info_list[temp]
    p2 = p1.find_element_by_tag_name('a')  # Get the anchor tag
    links.append(p2.get_property('href'))  # Append the link to the list
    temp = temp + 1
    if len(links) >= tplots:  # Break if we've reached the desired number of links
        break

print(pages)  # Print the page information

# Calculate total number of pages based on plots
d1 = []
tplots = ""
i = 0
while pages[i] != ' ':
    if pages[i].isdigit():
        d1.append((pages[i]))
        tplots = tplots + pages[i]
    i = i + 1

tplots = int(tplots)
npages = math.ceil(tplots / 25)  # Calculate number of pages (assuming 25 plots per page)
print(npages)

# Loop through additional pages if they exist
if npages > 1:
    for i in range(2, npages + 1):
        url = f'https://www.zameen.com/Plots/Islamabad_Gulberg-1682-{i}.html'  # Update URL for each page
        webD = wb.Chrome('C:/Users/ali/Downloads/Compressed/chromedriver')
        webD.get(url)  # Open the new page
        product_info_list = webD.find_elements_by_class_name('ef447dde')  # Get product info elements
        temp = 0
        for i in product_info_list:
            p1 = product_info_list[temp]
            p2 = p1.find_element_by_tag_name('a')
            links.append(p2.get_property('href'))  # Append the new links
            temp = temp + 1 
            if len(links) >= tplots:  # Break if we've reached the desired number of links
                break

# Print the number of links collected
len(links)

# Scrape details from each link
from tqdm import tqdm  # Import tqdm for progress bar
details = []

for i in tqdm(links):
    webD.get(i)  # Open each link
    # Extract relevant data using XPath
    Time = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[8]/span[2]').text
    Bath = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text
    a_string = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[1]/div/div/span').text

    id1 = []
    for word in a_string.split():
        if word.isdigit():  # Collect numeric IDs from a_string
            id1.append(int(word))

    price = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[2]/div[1]/div/form/div[1]/div/div[1]/div/div/span[3]').text
    type1 = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[1]/span[2]').text
    area = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[5]/span[2]').text
    purpose = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[6]/span[2]').text
    Location = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[3]/span[2]').text
    Bedroom = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text                                       
    Added = webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[2]/div[2]/div[1]').text
    
    # Create a dictionary to store scraped data
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
        "link": i  # Append the current link
    }
    details.append(list1)  # Add to the details list

# Close the web driver
webD.close()

# Create a DataFrame from the collected details
import pandas as pd
dataset = pd.DataFrame(details)

# Define functions to convert prices
def lactomillion(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0])
    million1 = million1 / 10
    dataset['Price'][i] = million1 

def croretomillion(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0])
    million1 = million1 * 10
    dataset['Price'][i] = million1 

# Convert prices to million
for i in range(0, len(dataset['Price'])):
    word = str(dataset['Price'][i])
    abc = str(dataset['Price'][i])
    if word.find('Lakh') != -1: 
        lactomillion(abc)
    elif word.find('Crore') != -1:
        croretomillion(abc)

# Print the dataset to check for data consistency
dataset

# Define functions to convert area measurements
def marlatosq(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0])
    million1 = million1 * 25.29
    dataset['Area'][i] = million1 

def kanaltosq(abc):
    million = re.findall(r"[-+]?\d*\.\d+|\d+", abc)
    million1 = float(million[0])
    million1 = million1 * 506
    dataset['Area'][i] = million1 

# Convert area measurements to square feet
for i in range(0, len(dataset['Area'])):
    word = str(dataset['Area'][i])
    abc = str(dataset['Area'][i])
    if word.find('Kanal') != -1: 
        kanaltosq(abc)
    elif word.find('Marla') != -1:
        marlatosq(abc)

# Print the final dataset
dataset

# Save the dataset to a CSV file
import csv
with open('zameen.csv', 'a') as f:
    dataset.to_csv(f, header=f.tell() == 0)
