##############################################################################################
###                             K-Means Python Implementation                              ###
###    http://konukoii.com/blog/2017/01/15/5-min-tutorial-k-means-clustering-in-python/    ###
##############################################################################################

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import csv

#Euclidian Distance between two d-dimensional points
def eucldist(p0,p1):
    dist = 0.0
    for i in range(0,len(p0)):
        dist += (p0[i] - p1[i])**2
    return math.sqrt(dist)


    
#K-Means Algorithm
def kmeans(k,datapoints,lables):

    #districts = ["AHMEDNAGAR",	"SHOLAPUR",	"SANGLI","AURANGABAD",	"JALNA",	"BEED",	"OSMANABAD",	"PUNE",	"JALGAON",	"BULDHANA",	"SATARA",	"LATUR",	"DHULE",	"PARBHANI",	"NANDED",	"NASHIK",	"NANDURBAR",	"AMRAOTI",	"WARDHA",	"AKOLA", 	"WASHIM",	"HINGOLI",	"NAGPUR",	"YEOTMAL",	"BHANDARA",	"CHANDRAPUR",	"MUMBAI CITY",	"KOLHAPUR",	"GADCHIROLI",	"GONDIA",	"MUMBAI SUBURBAN",	"THANE",	"RAIGAD",	"SINDHUDURG",	"RATNAGIRI"]


    # d - Dimensionality of Datapoints
    d = len(datapoints[0]) 
    
    #Limit our iterations
    Max_Iterations = 1000
    i = 0
    
    cluster = [0] * len(datapoints)
    prev_cluster = [-1] * len(datapoints)
    
    #Randomly Choose Centers for the Clusters
    cluster_centers = []
    for i in range(0,k):
        new_cluster = []
        #for i in range(0,d):
        #    new_cluster += [random.randint(0,10)]
        cluster_centers += [random.choice(datapoints)]
        
        
        #Sometimes The Random points are chosen poorly and so there ends up being empty clusters
        #In this particular implementation we want to force K exact clusters.
        #To take this feature off, simply take away "force_recalculation" from the while conditional.
        force_recalculation = False
    
    while (cluster != prev_cluster) or (i > Max_Iterations) or (force_recalculation) :
        
        prev_cluster = list(cluster)
        force_recalculation = False
        i += 1
    
        #Update Point's Cluster Alligiance
        for p in range(0,len(datapoints)):
            min_dist = float("inf")
            
            #Check min_distance against all centers
            for c in range(0,len(cluster_centers)):
                
                dist = eucldist(datapoints[p],cluster_centers[c])
                
                if (dist < min_dist):
                    min_dist = dist  
                    cluster[p] = c   # Reassign Point to new Cluster
        
        
        #Update Cluster's Position
        for k in range(0,len(cluster_centers)):
            new_center = [0] * d
            members = 0
            for p in range(0,len(datapoints)):
                if (cluster[p] == k): #If this point belongs to the cluster
                    for j in range(0,d):
                        new_center[j] += datapoints[p][j]
                    members += 1
            
            for j in range(0,d):
                if members != 0:
                    new_center[j] = new_center[j] / float(members) 
                
                #This means that our initial random assignment was poorly chosen
                #Change it to a new datapoint to actually force k clusters
                else: 
                    new_center = random.choice(datapoints)
                    force_recalculation = True
                    print ("Forced Recalculation...")
                    
            
            cluster_centers[k] = new_center
    
        
    print ("======== Results ========")
    print ("Clusters", cluster_centers)
    print ("Iterations",i)
    print ("Assignments", cluster)
    
    x1 = []
    y1= []
    for z in datapoints :
    	x1.append(z[0])
    	y1.append(z[1])
##    print(len(x1))
##    print(len(y1))
##    print(len(cluster))
    for i in range(len(x1)) :
    	if cluster[i]==0 :
            plt.plot(x1[i],y1[i],'ro')
            #plt.text(x1[i]+.01, y1[i]+.01, lables[i], fontsize=9)

    	elif cluster[i]==1 :
            plt.plot(x1[i],y1[i],'go')
            #plt.text(x1[i]+.01, y1[i]+.03, lables[i], fontsize=9)
    #plt.axis(0,10,0,5000)
    plt.show()
    


    
    
#TESTING THE PROGRAM#
if __name__ == "__main__":
    #2D - Datapoints List of n d-dimensional vectors. (For this example I already set up 2D Tuples)
    #Feel free to change to whatever size tuples you want...
    #X = np.array([[6.76,423.2],[11.04,1043.3],[7.57,1083.5],[7.96,487.5],[7.64,461.1],[6.51,1582.9],[6.73,713.9],[6.66,1534.1],[6.79,596],[6.45,1836.1],[7.1,1580.9],[7.84,881.5],[9.16,602],[7.35,444.8],[5.31,1730.3],[9.8,767.5],[2.98,1801],[4.87,2088.5],[6.57,1181.3],[6.65,800.1],[8.56,941.9],[6.3,1007.7],[6.85,483.4],[7.59,749.5],[5.34,770.3],[3.33,3193.7],[6.7,3829.6],[5.93,541.2],[5.96,843.1],[6.56,476.8],[6.84,3456.8],[3.75,2409.5],[6.8,995],[7.17,1044.9],[6.42,1083.7]])
    lat=[]
    lon=[]
    elevation=[]
    temperature=[]
    pressure=[]
    humidity=[]
    counter1=0
    counter2=0
    with open('coords_altitude.csv', 'rt') as csvfile:
        coords_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in coords_reader :
            #row = [x.strip() for x in row[0].split(',')]
            #print(row)
            lat1 = row[0].strip("ï»¿").replace(" ", "")
            lon1 = row[1].replace(" ", "")
            elevation1=row[2].replace(" ", "")
            lat.append(float(lat1))
            lon.append(float(lon1))
            elevation.append(float(elevation1))
            counter1=counter1+1
            print("got altitude :",counter1)

    with open('coords_weather.csv', 'rt') as csvfile:
            weather_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in weather_reader :
                #row = [x.strip() for x in row[0].split(',')]
                lat1 = row[0].strip("ï»¿").replace(" ", "")
                lon1 = row[1].replace(" ", "")
                temperature1 =row[2].replace(" ", "")
                pressure1=row[3].replace(" ", "")
                humidity1=row[4].replace(" ", "")
    ##            lat.append(lat1)
    ##            lon.append(lon1)
    ##            elevation.append(elevation1)
                temperature.append(float(temperature1))
                pressure.append(float(pressure1))
                humidity.append(float(humidity1))
                counter2=counter2+1
                print("got weather :",counter2)

    k = 2 # K - Number of Clusters
    X = list(zip(elevation,temperature))
    lables=list(zip(lat,lon))
    kmeans(k,X,lables) 
