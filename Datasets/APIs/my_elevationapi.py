import requests
import csv
import json
from elevationapi import Elevation

myrequest = 'https://api.open-elevation.com/api/v1/lookup?locations='
counter1 = 0
counter2 = 0
lat=[]
lon=[]
elevation=[]
with open('C:/Users/Samujjwaal Dey/Desktop/BEP/GIGO/DroughLL.csv', 'rt') as csvfile:
        coords_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in coords_reader :
            row = [x.strip() for x in row[0].split(',')]
            lat1 = row[0].strip("ï»¿").replace(" ", "")
            lon1 = row[1].replace(" ", "")
            lat.append(lat1)
            lon.append(lon1)
            e = Elevation()
            axes=(float(lat1),float(lon1))
            elevation.append(str(e.getElevation(axes)))
            print("calculated : ",counter1)
            counter1 = counter1 + 1
            #print(elevation_of_Geneva)

with open('coords_altitude.csv', 'wt') as csvfile:
    altitude_writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(elevation)) :
        altitude_writer.writerow(lat[i]+","+lon[i]+","+elevation[i])
        print("written : ",counter2)
        counter2 = counter2 + 1
##            myrequest = myrequest + lat + ',' + lon
##            #print(myrequest)
##            r = requests.get(myrequest)
##            jsonData = json.loads(r)
##            print(jsonData)
