import urllib.request
from bs4 import BeautifulSoup
import re
from bs4 import Tag
import sys

orig_stdout = sys.stdout
f = open('countries.txt', 'w') #: open file txt file for write list of countries inside them
sys.stdout = f

url = "https://www.worldometers.info/geography/alphabetical-list-of-countries/" #: that`s url of site which having a list of all countries
try: #: try go to site and check if having errors
    page = urllib.request.urlopen(url)
except:
    print("An error occured.")

soup = BeautifulSoup(page, 'html.parser') #: extract all html in web page (notic : thats html code having a our list (countries))
countCountries = soup.find_all('td',attrs={'style':'font-weight: bold; font-size:15px'})
length = len(countCountries) #: get count of all countries in world

for i in range(length): #: loop in numbers of
    get_packPrice = soup.find_all('td',attrs={'style':'font-weight: bold; font-size:15px'})[i].text #: get all td`s having style like font-weight:...
    packPrice = get_packPrice.replace(' ','+') #: replace all spaces in countries name to + (you will self know while i will try to scrapping data from the another site)
    txt = re.sub("\(.*\)", "", packPrice)
    print(txt)
sys.stdout = orig_stdout
f.close()
