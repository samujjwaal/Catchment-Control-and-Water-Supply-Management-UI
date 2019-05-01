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
    X = np.array([[5.33,423.2],[8.06,1043.3],[4.66,1083.5],[5.12,487.5],[2.49,461.1],[3.65,1582.9],[4.22,713.9],[2.88,1534.1],[5.01,596],[2.07,1836.1],[1.74,1580.9],[2.89,881.5],[7.04,602],[4.29,444.8],[2.31,1730.3],[5.04,767.5],[1.42,1801],[2.59,2088.5],[3.17,1181.3],[3.3,800.1],[5.41,941.9],[3.65,1007.7],[4.26,483.4],[4.31,749.5],[3.23,770.3],[0.66,3193.7],[2.63,3829.6],[3.93,541.2],[3.37,843.1],[2.66,476.8],[5.04,3456.8],[0.88,2409.5],[3.01,995],[2.84,1044.9],[3.14,1083.7]])

    k = 2 # K - Number of Clusters
      
    kmeans(k,X) 
