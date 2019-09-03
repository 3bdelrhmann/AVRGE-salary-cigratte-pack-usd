from django.shortcuts import render
import urllib.request
from bs4 import BeautifulSoup
import re
from bs4 import Tag

# Create your views here.
def result(request):
    f = open("./countries/countries.txt", "r")
    countries  = []
    salaryList = []
    packList   = []
    for x in f:
      country_name = x.rstrip()
      url = "https://www.numbeo.com/cost-of-living/country_result.jsp?country="+str(country_name)+"&displayCurrency=USD"
      try:
        page = urllib.request.urlopen(url)
      except:
        print("An error occured.")

      soup = BeautifulSoup(page, 'html.parser')
      if 'have that country in the database' in soup.text or 'No data for this country' in soup.text:
          print('Not Found Country:::')
      else:
          print(country_name)
          avgSalary = soup.find(lambda t: t.text.strip()=='Average Monthly Net Salary (After Tax)').parent.select('td')
          packPrice = soup.find(lambda t: t.text.strip()=='Cigarettes 20 Pack (Marlboro)').parent.select('td')
          country = soup.find('span',attrs={'class':'purple_light'}).text
          countries.append(country)
          for average, salary, ciggrates ,price in zip(avgSalary, avgSalary[1:],packPrice,packPrice[1:2]):
            sal = salary.text
            prc = price.text
            salaryList.append(sal)
            packList.append(prc)

    myData = zip(countries,salaryList,packList)
    context = {
                'myData':myData,
                }
    return render(request,'main/index.html',context)
