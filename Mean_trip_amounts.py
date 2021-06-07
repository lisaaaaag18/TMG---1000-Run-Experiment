import csv
import math
import matplotlib.pyplot as plt

def Mean_Trip_Amounts(filename):
    '''
    file --> tuple
    
    This function reads a file with the amount of trips that occured every hour 
    for 10 runs. It returns a tuple which contains a list of mean trip amounts 
    for every hour, and a list with the standard deviations for every hour.
    It also plots a graph containing all the standard deviations for every hour.
    
    '''
    mean_list = [0 for x in range (0,24)]
    bins = [[] for x in range(0,24)]
    records_processed = 0
    standard_deviation_list = []
   

    with open (filename, 'r') as csvfile:
        file_reader = csv.reader(csvfile, delimiter = ',')

         
        for row in file_reader:
            string = str(row[0])
            x = string.split(' ')
            x.remove('')
            
            for i in range (0,24):
                trips = float(x[i])
                bins[i].append(trips)
                mean_list[i] += trips
                
            records_processed += 1
            
        for i in range (0, 24):
            riemann_sum = 0
            mean_list[i] /= records_processed  
            
            for j in range (0, len(bins[i]), 1):
                riemann_sum += (bins[i][j] - mean_list[i])**2
            standard_deviation = math.sqrt(riemann_sum / records_processed)
            standard_deviation_list.append(standard_deviation)
   
        x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        plt.xticks([0,1, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])

        y = standard_deviation_list 

        
        plt.plot(x, y)
              
        plt.xlabel('Hour')
        plt.ylabel('Standard deviation')
        plt.title('Standard Deviations Per Hour')
              
        plt.show()    
    

    return (mean_list, standard_deviation_list)

print(Mean_Trip_Amounts('trip_list_data.csv'))