import csv
import math

def Mean_Trip_Amounts(filename):
    is_first_row = True
    counter = 0
    total_trips = 0
    mean_list = []
    i = 0
    string_length = 1

    with open (filename, 'r') as csvfile:
        file_reader = csv.reader(csvfile, delimiter = ',')

        while i < string_length:
         
            for row in file_reader:
            
                string = str(row[0])
                x = string.split(' ')
                x.remove('')
                print(x)
                string_length = len(x)
                total_trips += float(x[i])
                counter += 1
        
            mean = total_trips / counter
            mean_list.append(mean)
            i += 1
 


        
        #mean = total_trips / counter

    return mean_list

print(Mean_Trip_Amounts('C:\\Users\\gusevael\\Downloads\\trip_list_data.csv'))
