import csv
import math

def Auto_Ownership(filename): 
    '''
    file --> float

    This function calculated the average amount of cars contained in each household, 
    as well as the standard deviation from the mean.

    '''   
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    total_cars = 0 #How many cars there are in total. Initialized as 0
    total_households = 0 #How many households there are in total. Initialized as 0
    max_cars = 4
    H_cars = [i*2 for i in range (0, max_cars + 1)]
    riemann_sum = 0 #Riemann sum used to calculate standard deviation
    vehicle_list = [] #Empty list use to store amunt of vehicles per household
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row
                cars_in_household = int(row[5]) 
                total_cars += cars_in_household
                H_cars[cars_in_household] += 1
                total_households += 1 #increases total household amount by 1
                vehicle_list.append(int(row[5])) #Adds amount of vehicles to vehicle list
                
                
        avg_auto_ownership = int(total_cars)/int(total_households) #Calculates the mean amount of cars per household
            
    for i in range (0, len(vehicle_list), 1): #Goes through the list of cars per household
        riemann_sum += (vehicle_list[i] - avg_auto_ownership)**2 #Calculates the riemann sum part of the standard deviation
        
    standard_deviation = math.sqrt(riemann_sum / total_households) #Calculates standard deviation
    return  standard_deviation

print(Auto_Ownership('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\households.csv'))

def Drivers_License(filename):
    '''
    file --> tuple

    This function calculates the amount of people who have a license and the amount who don't. 
    The first element of the tuple contains the people who have licenses, and the second element contains
    people who don't.

    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    num_with_license = 0
    num_no_license = 0
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row   
                if (row[4] == 'true'):
                    num_with_license += 1
                    
                else:
                    num_no_license += 1
                    
    return (num_with_license, num_no_license)
                    
print(Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\persons.csv'))

def Number_of_Trips(filename):
    '''
    file --> list

    This function calculates the amount of trips that occured every hour during the period of 12am
    to 12am the next day (24 hours). The amount of trips each hour is stored in a list where each element
    represents the hour, starting at 12 am. The data is then saved to a file which will be used for further 
    calculations.

    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    bins = [0 for x in range (0,24)]

    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file  
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                index = float(row[4])//60 % 24
                bins[int(index)] += float(row[6])
                
    

    F=open('C:\\Users\\gusevael\\Downloads\\trip_list_data.csv','a')

    for k in range (0, len(bins), 1):
        F.write(str(bins[k]) + " ")
    F.write("\n")

    F.close()

    return bins

print(Number_of_Trips('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trip_modes.csv'))