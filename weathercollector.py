URL = "https://www.wunderground.com/history/daily/KBOS/date/2017-5-22"
regatta_info2 = []
import requests
import csv
from bs4 import BeautifulSoup

with open('weather.csv', mode="w") as racefile: 
    race_writer = csv.writer(racefile)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    dir_arrows = soup.find("http://schema.org/Organization")
    print(dir_arrows)
    for regatta in dir_arrows:
        race_writer.writerow(regatta)


