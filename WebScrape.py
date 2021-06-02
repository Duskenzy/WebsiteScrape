"""
WebScrape script

script for receiving data from the Pawnbat site.
Download Pawn shops certain informations from the California area from the website.
There are several pages, because there are a lot of Pawn shops, so I had to get the number of the last page.
Range is from first page to the last page and this way it reads all pages one by one
and receives data from them and saves the data to an xlsx file.
"""

import requests
from bs4 import BeautifulSoup
import pandas
import re
import xlsxwriter

r = requests.get("https://pawnbat.com/pawn-shops/CA/page-1/")   
c = r.content                                                   
soup = BeautifulSoup(c,"html.parser")                   
all = soup.find_all("div",{"class":"seller"})

# gets the number from the last page 
paging =soup.find_all("div", {"class":"paginal"})[-1].text      
take_num = re.findall('\d+', paging)                            
last_page = int(take_num[-1])                               


l = []                                                          
for page in range(1, (last_page + 1), 1):       
    print("https://pawnbat.com/pawn-shops/CA/page-" + str(page) + "/")              # nicely shows us the current page from which is receiving informations
    r = requests.get("https://pawnbat.com/pawn-shops/CA/page-" + str(page) + "/") 
    c = r.content  
    soup = BeautifulSoup(c, "html.parser")  
    all = soup.find_all("div", {"class": "seller"})
    for item in all:
        d={}                                            
        d["Name"]=item.find_all("a")[0].text            
        d["Address"] = item.find_all("td")[0].text      
        try:
            d["Phone Number"] = item.find_all("a")[1].text  # some Pawn Shops do not have a phone number 
        except:                                             # if its available, we will receive the number and when its not there then None
            d["Phone Number"] = None
        for link in item.find_all('tr'):                    # for loop is to get the Pawn shop's URL but in some cases the URL is missing
            for next in link.find_all('a', href=True):      # in html page under one element is URL and also Phone Number and we need only URL 
                if "http" in next['href']:
                    d["Website"] = next['href']
                else:
                    d["Website"] = None                     # if Website is available, we will receive the URL and when its not there then None

        l.append(d)                                     

df=pandas.DataFrame(l)                                  
writer = pandas.ExcelWriter('Output.xlsx', engine='xlsxwriter')
df.to_excel(writer,'California')
writer.save()
