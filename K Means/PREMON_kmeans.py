import random
import math
import numpy as np
import matplotlib.pyplot as plt

#Euclidian Distance between two d-dimensional points
def eucldist(p0,p1):
    dist = 0.0
    for i in range(0,len(p0)):
        dist += (p0[i] - p1[i])**2
    return math.sqrt(dist)


    
#K-Means Algorithm
def kmeans(k,datapoints):

    districts = ["AHMEDNAGAR",	"SHOLAPUR",	"SANGLI","AURANGABAD",	"JALNA",	"BEED",	"OSMANABAD",	"PUNE",	"JALGAON",	"BULDHANA",	"SATARA",	"LATUR",	"DHULE",	"PARBHANI",	"NANDED",	"NASHIK",	"NANDURBAR",	"AMRAOTI",	"WARDHA",	"AKOLA", 	"WASHIM",	"HINGOLI",	"NAGPUR",	"YEOTMAL",	"BHANDARA",	"CHANDRAPUR",	"MUMBAI CITY",	"KOLHAPUR",	"GADCHIROLI",	"GONDIA",	"MUMBAI SUBURBAN",	"THANE",	"RAIGAD",	"SINDHUDURG",	"RATNAGIRI"]


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
            plt.text(x1[i]+.01, y1[i]+.01, districts[i], fontsize=9)

    	elif cluster[i]==1 :
            plt.plot(x1[i],y1[i],'go')
            plt.text(x1[i]+.01, y1[i]+.03, districts[i], fontsize=9)
    #plt.axis(0,10,0,5000)
    plt.show()
    


    
    
#TESTING THE PROGRAM#
if __name__ == "__main__":
    #2D - Datapoints List of n d-dimensional vectors. (For this example I already set up 2D Tuples)
    #Feel free to change to whatever size tuples you want...
    X = np.array([[6.76,423.2],[11.04,1043.3],[7.57,1083.5],[7.96,487.5],[7.64,461.1],[6.51,1582.9],[6.73,713.9],[6.66,1534.1],[6.79,596],[6.45,1836.1],[7.1,1580.9],[7.84,881.5],[9.16,602],[7.35,444.8],[5.31,1730.3],[9.8,767.5],[2.98,1801],[4.87,2088.5],[6.57,1181.3],[6.65,800.1],[8.56,941.9],[6.3,1007.7],[6.85,483.4],[7.59,749.5],[5.34,770.3],[3.33,3193.7],[6.7,3829.6],[5.93,541.2],[5.96,843.1],[6.56,476.8],[6.84,3456.8],[3.75,2409.5],[6.8,995],[7.17,1044.9],[6.42,1083.7]])

    k = 2 # K - Number of Clusters
      
    kmeans(k,X) 
