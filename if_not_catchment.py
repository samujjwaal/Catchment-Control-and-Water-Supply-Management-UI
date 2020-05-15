import pyodbc
from math import sin, cos, sqrt, atan2, radians
lat1 = radians(19.99512)
lon1 = radians(73.79731)
#lat2 = radians(52.406374)
#lon2 = radians(16.9251681)

# approximate radius of earth in km
R = 6373.0
#distance = R * c
count=0
#print("Result:", distance)
#print("Should be:", 278.546, "km")
connection = pyodbc.connect(driver="{SQL Server}",server='sagdb.database.windows.net',database='sag',uid='sag',pwd='db@12345678')
cursor = connection.cursor()
#cursor1 = connection.cursor()
cursor.execute("SELECT * from UniqueLatLong ")
row_set = cursor.fetchall()
g=0
for row in row_set :
    lat2=radians(row[1])
    lon2=radians(row[2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    if distance<=50:
        
        #print(distance," ",row[1]," ",row[2])
        
            
        cursor.execute("SELECT SUM(catchment2) AS SUM_CATCHMENT FROM VariedRainfall WHERE YEAR_OBS>=2013 AND LAT=(?) AND LON =(?) GROUP BY LAT,LON;",row[1],row[2]  )          
        row1_set=cursor.fetchall()
        
        
        for row1 in row1_set :
            if row1[0] > 0 :
                print("LAT : ",row[1],"LONG : ",row[2],"Catchment_sum : ",row1[0],"distance : ",distance)
                g=g+1
            
print("Count : ",g)
            
        
    
    


