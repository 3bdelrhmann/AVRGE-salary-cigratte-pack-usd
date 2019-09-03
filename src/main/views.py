from django.shortcuts import render
import urllib.request
from bs4 import BeautifulSoup
import re
from bs4 import Tag

# Create your views here.
def result(request):
    f = open("./countries/countries.txt", "r")
    for x in f:
      country_name = x.rstrip()
      url = "https://www.numbeo.com/cost-of-living/country_result.jsp?country="+str(country_name)+"&displayCurrency=USD"
      page = urllib.request.urlopen(url)

      soup = BeautifulSoup(page, 'html.parser')

      try: #: try go to site and check if having errors
        avgSalary = soup.find(lambda t: t.text.strip()=='Average Monthly Net Salary (After Tax)').parent.select('td')
        packPrice = soup.find(lambda t: t.text.strip()=='Cigarettes 20 Pack (Marlboro)').parent.select('td')
        country = soup.find('span',attrs={'class':'purple_light'}).text
        for average, salary, ciggrates ,price in zip(avgSalary, avgSalary[1:],packPrice,packPrice[1:2]):
            salary = salary.text
            packetPrice = price.text

      except:
        if 'have that country in the database' in soup.text:
            print("country not found.")

    context = {
        'packetPrice':packetPrice,
        'salary':salary,
        'country_name':country,
    }
    return render(request,'main/index.html',context)
