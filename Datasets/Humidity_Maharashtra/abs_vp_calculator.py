import csv
import numpy

counter1 = 0
counter2 = 0
Jan=[]
Feb=[]
Mar=[]
Apr=[]
May=[]
Jun=[]
Jul=[]
Aug=[]
Sep=[]
Oct=[]
Nov=[]
Dec=[]


with open('Ahmednagar_temp.csv', 'rt') as csvfile:
        coords_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in coords_reader :
            #print("row : ",row)
            Jan.append(float(row[0]))
            Feb.append(float(row[1]))
            Mar.append(float(row[2]))
            Apr.append(float(row[3]))
            May.append(float(row[4]))
            Jun.append(float(row[5]))
            Jul.append(float(row[6]))
            Aug.append(float(row[7]))
            Sep.append(float(row[8]))
            Oct.append(float(row[9]))
            Nov.append(float(row[10]))
            Dec.append(float(row[11]))
            #print("calculated : ",counter1)
            counter1 = counter1 + 1

Es = numpy.zeros(shape=(len(Jan),12))
print(Es)
all_temp = list(zip(Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec))
print(all_temp[0][0])

for i in range(len(Jan)):
    for j in range(12):
        Es[i][j] = 6.11 * 10 **((7.5*all_temp[i][j])/(237.3 + all_temp[i][j]))

Jan1=[]
Feb1=[]
Mar1=[]
Apr1=[]
May1=[]
Jun1=[]
Jul1=[]
Aug1=[]
Sep1=[]
Oct1=[]
Nov1=[]
Dec1=[]
counter1=0
E = numpy.zeros(shape=(len(Jan),12))
with open('Ahmednagar_vp.csv', 'rt') as csvfile:
        coords_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in coords_reader :
            Jan1.append(float(row[0]))
            Feb1.append(float(row[1]))
            Mar1.append(float(row[2]))
            Apr1.append(float(row[3]))
            May1.append(float(row[4]))
            Jun1.append(float(row[5]))
            Jul1.append(float(row[6]))
            Aug1.append(float(row[7]))
            Sep1.append(float(row[8]))
            Oct1.append(float(row[9]))
            Nov1.append(float(row[10]))
            Dec1.append(float(row[11]))
            print("calculated : ",counter1)
            counter1 = counter1 + 1

vp = list(zip(Jan1,Feb1,Mar1,Apr1,May1,Jun1,Jul1,Aug1,Sep1,Oct1,Nov1,Dec1))

for i in range(len(Jan)):
    for j in range(12):
        E[i][j] = (vp[i][j]/Es[i][j])*100
counter2=0
with open('Ahmednagar_humidity.csv', 'wt') as csvfile:
    altitude_writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(Jan)) :
        altitude_writer.writerow(E[i])
        print("written : ",counter2)
        counter2 = counter2 + 1
