import csv
import math

def Read_Files(filename):    
    IsFirstRow = True #Flag to check if the row in the file is the first row. Initialized as true
    Total_Cars = 0 #How many cars there are in total. Initialized as 0
    Total_Households = 0 #How many households there are in total. Initialized as 0
    max_cars = 4
    H_cars = [i*2 for i in range (0, max_cars + 1)]
    Riemann_Sum = 0 #Riemann sum used to calculate standard deviation
    Vehicle_List = [] #Empty list use to store amunt of vehicles per household
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (IsFirstRow == True): #Checks if the row is the first row
                IsFirstRow = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row
                cars_in_household = int(row[5]) 
                Total_Cars += cars_in_household
                H_cars[cars_in_household] += 1
                Total_Households += 1 #increases total household amount by 1
                Vehicle_List.append(int(row[5])) #Adds amount of vehicles to vehicle list
                
                
        Avg_Auto_Ownership = int(Total_Cars)/int(Total_Households) #Calculates the mean amount of cars per household
            
    for i in range (0, len(Vehicle_List), 1): #Goes through the list of cars per household
        Riemann_Sum += (Vehicle_List[i] - Avg_Auto_Ownership)**2 #Calculates the riemann sum part of the standard deviation
        
    Standard_Deviation = math.sqrt(Riemann_Sum / Total_Households) #Calculates standard deviation
    return  Standard_Deviation

print(Read_Files('households.csv'))

def Drivers_License(filename):
    IsFirstRow = True #Flag to check if the row in the file is the first row. Initialized as true
    Num_With_License = 0
    Num_No_License = 0
    
    with open(filename, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file                     
            
            if (IsFirstRow == True): #Checks if the row is the first row
                IsFirstRow = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row   
                if (row[4] == 'TRUE'):
                    Num_With_License += 1
                    
                else:
                    Num_No_License += 1
                    
    return Num_With_License
                    
print(Drivers_License('persons.csv'))