from django.shortcuts import render
import urllib.request
from bs4 import BeautifulSoup
import re
from bs4 import Tag
import time

# Create your views here.
def result(request):
    start_time = time.time()
    f = open("./countries/countries.txt", "r")
    countries  = []
    avgVSpack  = []
    avgSalary  = []
    for x in f:
      country = x.rstrip()
      url = "https://www.numbeo.com/cost-of-living/country_result.jsp?country={}&displayCurrency=USD".format(country)
      page = urllib.request.urlopen(url)
      soup = BeautifulSoup(page, 'html.parser')
      if 'Average Monthly Net Salary' in soup.text :
          get_avgSalary = soup.find(lambda t: t.text.strip()=='Average Monthly Net Salary (After Tax)').parent.select('td')
          get_packPrice = soup.find(lambda t: t.text.strip()=='Cigarettes 20 Pack (Marlboro)').parent.select('td')
          country = soup.find('span',attrs={'class':'purple_light'}).text
          countries.append(country)
          for salary,price in zip(get_avgSalary[1:],get_packPrice[1:2]):
            salary = salary.text
            packPrice = price.text
            if soup.find('option',{'selected':'selected','value':'USD'}):
                filter_salry = salary.replace('$','').strip().replace(',','')
                filter_price = packPrice.replace('$','').strip()
                if filter_price == '?' or filter_salry == '?':
                    filter_price = 0
                    filter_salry = 0
                else:
                    ConvertSalToFloating = float(filter_salry)
                    ConverPriceToFloating = float(filter_price)
                    Avrg_Pack_Price_In_Country = round(ConvertSalToFloating,2)/round(ConverPriceToFloating,2)
                    avrgWithStr = str(Avrg_Pack_Price_In_Country)
                    avgVSpack.append(avrgWithStr[:6])
                    avgSalary.append(salary)
                    print(country)
            else:
                pass
      else:
          pass
    myData = zip(countries,avgVSpack,avgSalary)
    context = {
                'myData':myData,
                }
    return render(request,'main/index.html',context)
