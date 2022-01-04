#!/usr/bin/env python
# coding: utf-8

# In[2]:


import selenium
from selenium import webdriver as wb
import time
import math


# In[3]:


links=[]
url='https://www.zameen.com/Plots/Islamabad_Gulberg-1682-1.html'
webD = wb.Chrome('C:/Users/ali/Downloads/Compressed/chromedriver')
webD.get(url)
#webD.refresh()
product_info_list=webD.find_elements_by_class_name('ef447dde')
pages = webD.find_element_by_class_name("_2aa3d08d").text
d1=[]
tplots=""
i=0
while(pages[i]!=' '):
    if pages[i].isdigit():
        d1.append((pages[i]))
        tplots=tplots+pages[i]
    i=i+1
    
tplots=int(tplots)    
temp=0
for i in product_info_list:
    p1=product_info_list[temp]
    p2=p1.find_element_by_tag_name('a')   #for reference h ref
    links.append(p2.get_property('href'))
    temp=temp+1
    if(len(links)>=tplots):
        break
    


print(pages) 


# In[ ]:





# In[4]:


d1=[]
tplots=""
i=0
while(pages[i]!=' '):
    if pages[i].isdigit():
        d1.append((pages[i]))
        tplots=tplots+pages[i]
    i=i+1

tplots=int(tplots)
npages=math.ceil(tplots/25)
print(npages)


# In[ ]:


if(npages>1):
    for i in range(2,npages+1):
        url='https://www.zameen.com/Plots/Islamabad_Gulberg-1682-'+ str(i)+'.html'
        webD = wb.Chrome('C:/Users/ali/Downloads/Compressed/chromedriver')
        webD.get(url)
        #webD.refresh()
        product_info_list=webD.find_elements_by_class_name('ef447dde')
        temp=0
        for i in product_info_list:
            p1=product_info_list[temp]
            p2=p1.find_element_by_tag_name('a')   #for reference h ref
            links.append(p2.get_property('href'))
            temp=temp+1 
            if(len(links)>=tplots):
               break
        
    


# In[ ]:


len(links)


# In[ ]:


from tqdm import tqdm
details=[]

for i in tqdm(links):
    webD.get(i)
    
    Time=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[8]/span[2]').text
    Bath=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text
    a_string=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[1]/div/div/span').text

    id1 = []
    for word in a_string.split():
         if word.isdigit():
            id1.append(int(word))
    price=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[2]/div[1]/div/form/div[1]/div/div[1]/div/div/span[3]').text
    type1=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[1]/span[2]').text
    area=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[5]/span[2]').text
    purpose=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[6]/span[2]').text
    Location=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[3]/span[2]').text
    Bedroom=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[4]/div/div[2]/ul/li[7]/span[2]').text                                       
    Added=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[2]/div[2]/div[1]').text
    #time.sleep(5)
    #months1=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[8]/div/div[2]/div/div[1]/div[1]/div/div[1]/ul/li[2]/ul/li[1]/span[2]').text
    #months2=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[8]/div/div[2]/div/div[1]/div[1]/div/div[1]/ul/li[2]/ul/li[2]/span[2]').text
    #months3=webD.find_element_by_xpath('//*[@id="body-wrapper"]/main/div[4]/div[1]/div[8]/div/div[2]/div/div[1]/div[1]/div/div[1]/ul/li[2]/ul/li[3]/span[2]').text
    
    
    list1={"id":id1[0],
    "Type":type1,
      "Area":area,
      "Price":price,
      "Purpose":purpose,
      "Location":Location,
      "Bedroom":Bedroom,
      "Bath":Bath,
      "Added":Added,
           "time":Time,
     # "6months":months1,
     # "12months":months2,
      # "24months":months3,
       "link":i
      
      }
    details.append(list1)
    
    


# In[ ]:


webD.close()


# In[ ]:


import pandas as pd
dataset=pd.DataFrame(details)


# In[ ]:


def lactomillion(abc):
        million = re.findall(r"[-+]?\d*\.\d+|\d+",abc )
        million1=float(million[0])
        million1=million1/10
        dataset['Price'][i]=million1 
        
def croretomillion(abc):
        million = re.findall(r"[-+]?\d*\.\d+|\d+",abc )
        million1=float(million[0])
        million1=million1*10
        dataset['Price'][i]=million1 
                


# In[ ]:


import re

for i in range(0,len(dataset['Price'])):
    word = str(dataset['Price'][i])
    abc=str(dataset['Price'][i])
    if (word.find('Lakh') != -1): 
            lactomillion(abc)

            
    elif (word.find('Crore') != -1): {
            croretomillion(abc)
     }


# In[ ]:




