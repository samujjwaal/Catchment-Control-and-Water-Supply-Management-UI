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
    X = np.array([[5.1,423.2],[8.24,1043.3],[5.28,1083.5],[5.25,487.5],[3.36,461.1],[3.74,1582.9],[4.65,713.9],[3.57,1534.1],[5,596],[3.08,1836.1],[3.15,1580.9],[3.86,881.5],[7.16,602],[4.56,444.8],[3.03,1730.3],[5.26,767.5],[2.34,1801],[3.8,2088.5],[3.7,1181.3],[3.68,800.1],[6.16,941.9],[3.98,1007.7],[4.45,483.4],[4.38,749.5],[3.34,770.3],[1.52,3193.7],[4.47,3829.6],[3.61,541.2],[3.56,843.1],[4.08,476.8],[4.28,3456.8],[1.8,2409.5],[3.8,995],[3.59,1044.9],[3.92,1083.7]])

    k = 2 # K - Number of Clusters
      
    kmeans(k,X) 
