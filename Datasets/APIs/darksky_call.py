  import requests
import csv
import json
from darksky import forecast
from datetime import datetime as dt

key = "e53a7fb47f4d7ba0b9ed61f4ff7d2fed"


counter1 = 0
counter2 = 0
lat=[]
lon=[]
humidity=[]
temperature=[]
years=[1996,2001,2006,2011,2016]
months = [1,4,7,10]

with open('latlong.csv', 'rt') as csvfile:
        coords_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in coords_reader :
                counter1 = counter1+1
                if counter1< 36 :
                        print(counter1,row[1],row[2])
                        lat.append(float(row[1]))
                        lon.append(float(row[2]))

for i in range(len(lat)) :
        for j in range(len(years)) :
                for k in range(len(months)) :
                        t = dt(years[j],months[k],15,12)
                        call_it = forecast(key,lat[i],lon[i],time=t)
                        humidity.append(call_it.humidity)
                        temperature.append(call_it.temperature)	

with open('district_humidity.csv', 'wt') as csvfile:
        humidity_writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(lat)) :
                humidity_writer.writerow(lat[i],lon[i],humidity[i],temperature[i])
                print("written : ",counter2)
                counter2 = counter2 + 1

