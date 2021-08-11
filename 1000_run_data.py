import csv
import math
import collections, functools, operator
import pandas as pd
import zipfile
import io

def Conversions(file1, file2):
    '''
    file, file --> dict, dict

    This function reads a file in order to convert a zone to the appropriate planning 
    district. It then reads the second file to convert the planning districts to spatial
    categories. The function returns two dictionaries, the first one having the keys as
    zones and the values as the appropriate planning districts. The second dictionary has
    the planning districts as keys and spatial categories as values.

    '''
    zone_to_pd = {}
    pd_to_sp = {}    
    
    with open(file1, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for conversion_row1 in csv_reader:   
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1 
                zone_to_pd[conversion_row1[0]] = conversion_row1[1]
                
            
    with open(file2, 'r') as csv_file1:
        csv_reader1 = csv.reader(csv_file1, delimiter=',')
        line_count1 = 0
        for conversion_row2 in csv_reader1:
            if line_count1 == 0:
                line_count1 += 1
            else:
                line_count1 += 1
                pd_to_sp[conversion_row2[0]] = conversion_row2[1]
                   
    return (zone_to_pd, pd_to_sp)

def Get_Archive(my_zipfile, suffix_string): 
        for file in my_zipfile.namelist():
            if (file.endswith(suffix_string)):
                return file

        raise Exception('Unable to find archive name with the given suffix')

def Auto_Ownership(fo_num, fi_num): 
    '''
    file --> dictionary

    This function calculates the average amount of households who have a certain amount of cars
    (0, 1, 2, 3, or 4) in each spatial category. It returns a dictionary with the keys being
    the spatial category and the values being a dictionary where the keys are the number of cars 
    and the values are the amount of households who own that amount of cars.

    fo_num = tells which folders to look at.
    fi_num = tells which file to look at.

    '''   
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    spatial_category_list = []
    cars_list = []
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    ownerships_dict = {}
    #Folders used for 1000 runs
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders used for 50 runs
    folders = ['0-49']

    first_file = list(range(50))
    other_files = list(range(10))
    if (fo_num == 0):
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip:

            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'households.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')  

                for row in file_reader1:                  
            
                    if (is_first_row == True): #Checks if the row is the first row
                        is_first_row = False #Changes flag to false since there is only 1 first row    
            
                    else: #If the row is not the first row
                        cars_list.append(int(row[5]))
                        home_zone = row[1] 
                        home_pd = variables[0][home_zone]
                        home_sc = variables[1][home_pd]
                        spatial_category_list.append(home_sc)
                
                for i in range (0, len(spatial_category_list), 1): 
        
                    if spatial_category_list[i] in ownerships_dict:
                        if cars_list[i] in ownerships_dict[spatial_category_list[i]]:
                            value = ownerships_dict[spatial_category_list[i]][cars_list[i]] + 1
                            ownerships_dict[spatial_category_list[i]][cars_list[i]] = value          
                
                        else:
                            ownerships_dict[spatial_category_list[i]][cars_list[i]] = 1
                
                    else:
                        ownerships_dict[spatial_category_list[i]] = {cars_list[i] : 1}

    else:
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip:

            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'households.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')  

                for row in file_reader1:                  
            
                    if (is_first_row == True): #Checks if the row is the first row
                        is_first_row = False #Changes flag to false since there is only 1 first row    
            
                    else: #If the row is not the first row
                        cars_list.append(int(row[5]))
                        home_zone = row[1] 
                        home_pd = variables[0][home_zone]
                        home_sc = variables[1][home_pd]
                        spatial_category_list.append(home_sc)
                
                for i in range (0, len(spatial_category_list), 1): 
        
                    if spatial_category_list[i] in ownerships_dict:
                        if cars_list[i] in ownerships_dict[spatial_category_list[i]]:
                            value = ownerships_dict[spatial_category_list[i]][cars_list[i]] + 1
                            ownerships_dict[spatial_category_list[i]][cars_list[i]] = value          
                
                        else:
                            ownerships_dict[spatial_category_list[i]][cars_list[i]] = 1
                
                    else:
                        ownerships_dict[spatial_category_list[i]] = {cars_list[i] : 1}
        
    return ownerships_dict 

def Auto_Ownership_Mean_SD_CV():
    '''
    none --> dict

    This function calculates the mean, standard deviation, and coefficient of variation for auto ownership.
    It returns a dictionary of means or standard deviations or coefficients of variation.

    '''
    data = []
    means_dict = {}
    totals_dict = {}
    sum_dict = {}
    final_means_dict = {}
    riemann_dict = {}
    sd = {}
    cv = {}
    #Folders used for 1000 runs
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders used for 50 runs
    folders = ['0-49']
    first_file = list(range(50))
    other_files = list(range(10))
    
    for i in range (0, len(folders), 1):
        if (i == 0):
            for j in range (0, len(first_file), 1):
                data.append(Auto_Ownership(i, j))

        else:
            for k in range (0, len(other_files), 1):
                data.append(Auto_Ownership(i, k))
        
    for i in range (0, len(data), 1):
        for key1 in data[i]:
            if (key1 in totals_dict):
                totals_dict[key1].append(data[i][key1])
                
            else:
                totals_dict[key1] = [data[i][key1]]

    for i in range (0, len(data), 1):
        for key1 in data[i]:
            if (key1 in totals_dict):
                totals_dict[key1].append(data[i][key1])
                
            else:
                totals_dict[key1] = [data[i][key1]]
                
    for key in totals_dict:
        result = dict(functools.reduce(operator.add,
                 map(collections.Counter, totals_dict[key])))  
        
        sum_dict[key] = result
        
    for key in sum_dict:
        means_dict = {}
        for key1 in sum_dict[key]:
            means_dict[key1] = sum_dict[key][key1] / len(data)   
            final_means_dict[key] = means_dict

    for key in final_means_dict:
        riemann_sums_inner = {}
        for j in range (0, len(data), 1):
            for key1 in data[j]:
                counter = 0
                if (key1 == key):
                    for key2 in final_means_dict[key]:
                        if key2 in riemann_sums_inner:
                            riemann_sums_inner[key2].append((data[j][key1][key2] - final_means_dict[key1][key2])**2)
                            counter += 1
                            
                        else:
                            riemann_sums_inner[key2] = [(data[j][key1][key2] - final_means_dict[key1][key2])**2]
                            
                    riemann_dict[key] = riemann_sums_inner
    
    for sp_key in riemann_dict:
        inner_dict = {}
        for inner_key in riemann_dict[sp_key]:
            value = math.sqrt(sum(riemann_dict[sp_key][inner_key])/len(riemann_dict[sp_key][inner_key]))
            inner_dict[inner_key] = value
        sd[sp_key] = inner_dict           
   
    for key in sd:
        cv_inner_dict = {}
        for key1 in sd[key]:
            cv_value = sd[key][key1] / final_means_dict[key][key1]
            cv_inner_dict[key1] = cv_value
        cv[key] = cv_inner_dict

    # Change return variable based on desired output (mean, sd = standard deviation, cv = coefficient of variation)        
    return sd

#data_frame_auto = pd.DataFrame.from_dict(Auto_Ownership_Mean_SD(), orient = 'index')
#data_frame_auto.to_csv('auto_ownership_50_runs.csv',sep=',')

def Drivers_License(fo_num, fi_num):
    '''
    file --> dictionary

    This function calculates the fraction of people (16+ years old) who have a license in each spatial 
    category. It returns a dictionary where the keys are the spatial categories and the values are the 
    fraction of those people who have licenses in that spatial category.

    fo_num = tells which folders to look at.
    fi_num = tells which file to look at.
    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    household_zones_dict = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    sp_license = {}
    total_people = {}
    folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    first_file = list(range(50))
    other_files = list(range(10))

    if (fo_num == 0):
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'households.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')

                for row in file_reader1:
                    household_zones_dict[row[0]] = row[1]

        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'persons.csv')), encoding="utf-8") as myfile2:
        
                file_reader = csv.reader(myfile2, delimiter = ',') #Reads csv file  
        
                for row in file_reader: # Goes through every row in file                     
            
                    if (is_first_row == True): #Checks if the row is the first row
                        is_first_row = False #Changes flag to false since there is only 1 first row    
            
                    else: #If the row is not the first row 

                
                        if(row[0] in household_zones_dict):
                            if (int(row[2]) >= 16):
                                zone = household_zones_dict[row[0]]
                                planning_district = variables[0][zone]
                                spatial_category = variables[1][planning_district]
                                total_people[spatial_category] = total_people.get(spatial_category, 0) + 1
                                if(row[4] == 'true'):
                                    sp_license[spatial_category] = sp_license.get(spatial_category, 0) + 1  

    else:
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'households.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')

                for row in file_reader1:
                    household_zones_dict[row[0]] = row[1]

        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'persons.csv')), encoding="utf-8") as myfile2:
        
                file_reader = csv.reader(myfile2, delimiter = ',') #Reads csv file  
        
                for row in file_reader: # Goes through every row in file                     
            
                    if (is_first_row == True): #Checks if the row is the first row
                        is_first_row = False #Changes flag to false since there is only 1 first row    
            
                    else: #If the row is not the first row 

                
                        if(row[0] in household_zones_dict):
                            if (int(row[2]) >= 16):
                                zone = household_zones_dict[row[0]]
                                planning_district = variables[0][zone]
                                spatial_category = variables[1][planning_district]
                                total_people[spatial_category] = total_people.get(spatial_category, 0) + 1
                                if(row[4] == 'true'):
                                    sp_license[spatial_category] = sp_license.get(spatial_category, 0) + 1  

                    

    sc_fraction = {k: sp_license.get(k, 0) / float(total_people[k]) for k in total_people}  
                  
    return sc_fraction
                    
#print(Drivers_License('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\persons.csv'))

def Mean_Drivers_License():
    '''
    none --> tuple

    This function calculates the mean, standard deviation, and coefficient of variation for driver's
    license ownership. It returns a 3-element tuple where the first element is a dictionary of means. 
    The keys are spatial categories and the values are the mean fraction of people with a license 
    for that spatial category. The second element is a dictionary for standard deviation where the keys 
    are the spatial categories and the values are standard deviations. The last element is a dictionary 
    for the coefficient of variation where the keys are the spatial categories and the values are the 
    coefficients of variation.
    '''
    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    sd_dict = {}
    means_dict = {}
    totals_sum = {}
    sc_cd = {}
    folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    first_file = list(range(50))
    other_files = list(range(10))
    
    for i in range (0, len(folders), 1):
        if (i == 0):
            for j in range (0, len(first_file), 1):
                data.append(Drivers_License(i, j))

        else:
            for k in range (0, len(other_files), 1):
                data.append(Drivers_License(i, k))

    for i in range (0, len(data), 1):
        for key in data[i]:
             keys_list.append(key)
             values_list.append(data[i][key])
        
    for j in range (0, len(keys_list), 1):
        if (keys_list[j] in group_dict):
            group_dict[keys_list[j]].append(values_list[j])
        
        else:
            group_dict[keys_list[j]] = [values_list[j]]
        
    for key in group_dict:
        totals_sum[key] = sum(group_dict[key])

    for key in totals_sum:
        means_dict[key] = totals_sum[key] / len(data)

    for key in group_dict:
        riemann_sum = 0
        for k in range (0, len(group_dict[key]), 1):
            riemann_sum += (group_dict[key][k] - means_dict[key])**2
        standard_deviation = math.sqrt(riemann_sum / len(group_dict[key]))
        sd_dict[key] = standard_deviation

    for key in means_dict:
        value = sd_dict[key]/means_dict[key]
        sc_cd[key] = value

    return means_dict

#print(Mean_SD_Drivers_License())

def Trip_Amounts(filename1, filename2):
    '''
    file --> dict

    This function calculates the amount of trips that occured every hour during the period of 12am
    to 12am the next day (24 hours) for each spatial category. The function returns a dictionary
    where the keys are the spatial categories and the values are a list where each element represents 
    the hour and how many trips occured in that hour, starting at 12 am.

    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    is_first_row1 = True
    bins = [0 for x in range (0,24)]
    start_list = []
    weight_list = []
    spatial_category_list = []
    household_zones_dict = {}
    sp_trip_quantity = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    sp_weights = {}
    output = {}
    
    with open (filename1, 'r') as csvfile1:
            file_reader1 = csv.reader(csvfile1, delimiter = ',')
    
            for row in file_reader1:
                if (is_first_row1 == True): #Checks if the row is the first row
                    is_first_row1 = False #Changes flag to false since there is only 1 first row    
                
                else: #If the row is not the first row             
                    household_zones_dict[row[0]] = row[1]    

    
    with open(filename2, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file  
            
            if (is_first_row == True): #Checks if the row is the first row
                is_first_row = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                start_list.append(row[4])
                weight_list.append(row[6])
                
                if(row[0] in household_zones_dict):
                    zone = household_zones_dict[row[0]]
                    planning_district = variables[0][zone]
                    spatial_category = variables[1][planning_district]
                    spatial_category_list.append(spatial_category)                
                
    for j in range (0, len(spatial_category_list), 1):
        if spatial_category_list[j] in sp_trip_quantity:
            sp_trip_quantity[spatial_category_list[j]].append(start_list[j])
            sp_weights[spatial_category_list[j]].append(weight_list[j])
        else:
            sp_trip_quantity[spatial_category_list[j]] = [start_list[j]] 
            sp_weights[spatial_category_list[j]] = [weight_list[j]] 
            
    for key in sp_trip_quantity:
        bins = [0 for x in range (0,24)]
        for i in range (0, len(sp_trip_quantity[key]), 1):
            index = float(sp_trip_quantity[key][i])//60 % 24
            bins[int(index)] += float(sp_weights[key][i])  
            output[key] = bins

    final_output = {}
    for key in output:
        hour = 1
        inner_dict = {}
        for k in range (0, len(output[key]), 1):
            inner_dict[hour] = output[key][k] 
            hour += 1
        final_output[key] = inner_dict          
    
    return final_output

#print(Trip_Amounts('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\1\\Microsim Results\\trip_modes.csv'))
       
def Mean_SD_Trip_Amounts(): 
    '''
    None --> tuple

    This function calculates the mean, standard deviation, and coefficient of variation for the trip
    amounts across 1000 runs. It returns a tuple where the first element is a dictionary of means. The 
    key is the spatial category and the values are dictionaries where the key is the hour (1-24) starting
    from 12 am to 12 am the next day. The value is the mean amount of trips that occured in that hour for
    that specific spatial category. The same principle applies to the standard deviation and coefficient
    of variation which are the second and third elements in the tuple.
    '''

    data = []
    totals_dict = {}
    sum_dict = {}
    final_means_dict = {}
    riemann_dict = {}
    sd = {}
    cv = {}

    for i in range(0, 1000):
        data.append(Trip_Amounts("C:\\Users\\gusevael\\Downloads\\1000 Run Data\\" + str(i) + "\\Microsim Results\\households.csv", "C:\\Users\\gusevael\\Downloads\\1000 Run Data\\" + str(i) + "\\Microsim Results\\trip_modes.csv"))

    for i in range (0, len(data), 1):
        for key1 in data[i]:
            if (key1 in totals_dict):
                totals_dict[key1].append(data[i][key1])
                
            else:
                totals_dict[key1] = [data[i][key1]]
                
    for key in totals_dict:
        result = dict(functools.reduce(operator.add,
                 map(collections.Counter, totals_dict[key])))  
        
        sum_dict[key] = result
        
    for key in sum_dict:
        means_dict = {}
        for key1 in sum_dict[key]:
            means_dict[key1] = sum_dict[key][key1] / len(data)   
            final_means_dict[key] = means_dict

    for key in final_means_dict:
        riemann_sums = [0 for x in range (0, 24)]
        for j in range (0, len(data), 1):
            for key1 in data[j]:
                counter = 0
                if (key1 == key):
                    for key2 in final_means_dict[key]:
                        riemann_sums[counter] += (data[j][key1][key2] - final_means_dict[key1][key2])**2
                        counter += 1
                        
                        if (0 not in riemann_sums):    
                            riemann_dict[key] = riemann_sums
                                                   
    for sum_key in riemann_dict:
        counter1 = 1
        inner_sd = {}
        for k in range (0, len(riemann_dict[sum_key]), 1):
            new_value = math.sqrt(riemann_dict[sum_key][k] / len(data))
            inner_sd[counter1] = new_value
            counter1 += 1
        sd[sum_key] = inner_sd

    for key in sd:
        cv_inner_dict = {}
        for key1 in sd[key]:
            cv_value = sd[key][key1] / final_means_dict[key][key1]
            cv_inner_dict[key1] = cv_value
        cv[key] = cv_inner_dict
            
    return final_means_dict, sd, cv

#print(Mean_SD_Trip_Amounts())
#data_frame_amounts = pd.DataFrame.from_dict(Mean_SD_Trip_Amounts(), orient = 'index')
#data_frame_amounts.to_csv('trip_amounts_1000_runs.csv',sep=',')
#print(Mean_SD_Trip_Amounts())

def Trip_Durations(filename1, filename2):
    '''
    file --> dict

    This function determines the average trip time for each spatial category by trip modes. It returns a nested
    dictionary where the keys are the spatial categories, and the values are dictionaries with keys being modes
    of transportation and values being the average trip time for that specific mode.

    '''
    is_first_row2 = True #Flag to check if the row in the file is the first row. Initialized as true
    is_first_row1 = True
    duration = 0
    durations_list = []
    household_zones_dict = {}
    weight_list = []
    spatial_category_list = []
    durations_dict = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    trip_type = []
    output_means = {}
    sc_weights = {}

    with open (filename1, 'r') as csvfile1:
        file_reader1 = csv.reader(csvfile1, delimiter = ',')

        for row in file_reader1:
            if (is_first_row1 == True): #Checks if the row is the first row
                is_first_row1 = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row             
                household_zones_dict[row[0]] = row[1]
    
    with open(filename2, 'r') as csvfile: #Opens csv file
        
        file_reader = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row in file_reader: # Goes through every row in file  
            
            if (is_first_row2 == True): #Checks if the row is the first row
                is_first_row2 = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row 
                trip_type.append(row[3])
                duration = (float(row[5]) - float(row[4]))
                durations_list.append(duration)
                weight_list.append(float(row[6]))
                
                if(row[0] in household_zones_dict):
                    zone = household_zones_dict[row[0]]
                    planning_district = variables[0][zone]
                    spatial_category = variables[1][planning_district]
                    spatial_category_list.append(spatial_category)

    for i in range (0, len(spatial_category_list), 1): 
        
        if spatial_category_list[i] in durations_dict:
            if trip_type[i] in durations_dict[spatial_category_list[i]]:
                value = durations_dict[spatial_category_list[i]][trip_type[i]] + (durations_list[i] * weight_list[i])
                durations_dict[spatial_category_list[i]][trip_type[i]] = value
                weight_value = sc_weights[spatial_category_list[i]][trip_type[i]] + weight_list[i]
                sc_weights[spatial_category_list[i]][trip_type[i]] = weight_value
                
            else:
                durations_dict[spatial_category_list[i]][trip_type[i]] = (durations_list[i] * weight_list[i])
                sc_weights[spatial_category_list[i]][trip_type[i]] = weight_list[i]
                
        else:
            durations_dict[spatial_category_list[i]] = {trip_type[i] : (durations_list[i] * weight_list[i])}
            sc_weights[spatial_category_list[i]] = {trip_type[i] : weight_list[i]}

            
                        
    for key in durations_dict:
        sc_means = {k: durations_dict[key][k] / float(sc_weights[key][k]) for k in durations_dict[key] if k in sc_weights[key]} 
        output_means[key] = sc_means
    
    return output_means

#print(Trip_Durations('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\households.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\0\\Microsim Results\\trip_modes.csv'))

def Trip_Durations_Mean_Sd():  
    '''
    None --> tuple

    This function calculates the mean, standard deviation, and coefficient of variation for the trip
    durations across 1000 runs. It returns a tuple where the first element is a dictionary of means. The 
    key is the spatial category and the values are dictionaries where the key is the mode of transportation.
    The value is the mean durtion of trips that occured for that mode of transportation for that specific 
    spatial category. The same principle applies to the standard deviation and coefficient of variation 
    which are the second and third elements in the tuple.
    '''
    data = []
    totals_dict = {}
    sum_dict = {}
    final_means_dict = {}
    riemann_dict = {}
    sd = {}
    cv = {}

    for i in range(0, 1000):
        data.append(Trip_Durations("C:\\Users\\gusevael\\Downloads\\1000 Run Data\\" + str(i) + "\\Microsim Results\\households.csv", "C:\\Users\\gusevael\\Downloads\\1000 Run Data\\" + str(i) + "\\Microsim Results\\trip_modes.csv"))

    for i in range (0, len(data), 1):
        for key1 in data[i]:
            if (key1 in totals_dict):
                totals_dict[key1].append(data[i][key1])
                
            else:
                totals_dict[key1] = [data[i][key1]]
                
    for key in totals_dict:
        result = dict(functools.reduce(operator.add,
                 map(collections.Counter, totals_dict[key])))  
        
        sum_dict[key] = result
        
    for key in sum_dict:
        means_dict = {}
        for key1 in sum_dict[key]:
            means_dict[key1] = sum_dict[key][key1] / len(data)   
            final_means_dict[key] = means_dict

    for key in final_means_dict:
        riemann_sums_inner = {}
        for j in range (0, len(data), 1):
            for key1 in data[j]:
                counter = 0
                if (key1 == key):
                    for key2 in final_means_dict[key]:
                        if key2 in riemann_sums_inner:
                            riemann_sums_inner[key2].append((data[j][key1][key2] - final_means_dict[key1][key2])**2)
                            counter += 1
                            
                        else:
                            riemann_sums_inner[key2] = [(data[j][key1][key2] - final_means_dict[key1][key2])**2]
                            
                    riemann_dict[key] = riemann_sums_inner
    
    for sp_key in riemann_dict:
        inner_dict = {}
        for inner_key in riemann_dict[sp_key]:
            value = math.sqrt(sum(riemann_dict[sp_key][inner_key])/len(riemann_dict[sp_key][inner_key]))
            inner_dict[inner_key] = value
        sd[sp_key] = inner_dict
            
   
    for key in sd:
        cv_inner_dict = {}
        for key1 in sd[key]:
            cv_value = sd[key][key1] / final_means_dict[key][key1]
            cv_inner_dict[key1] = cv_value
        cv[key] = cv_inner_dict
            
    return final_means_dict, sd, cv

#df_durations = pd.DataFrame.from_dict(Trip_Durations_Mean_Sd(), orient = 'index')
#df_durations.to_csv('trip_durations_1000_runs.csv',sep=',')
#print(df.loc['9','VFH'])
#print(Trip_Durations_Mean_Sd())

def Shopping_Activities(fo_num, fi_num):
    '''
    file --> dict

    This function calculates the amount of shopping trips that occured in each spatial category. It
    returns a dictionary where the keys are the spatial categories and the values are the amounts 
    of shopping trips that occured in that specific spatial category.

    fo_num = tells which folders to look at.
    fi_num = tells which file to look at.
    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    spatial_category_list = []
    d_act_list = []
    activities = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    shopping_amounts = {}
    folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    first_file = list(range(50))
    other_files = list(range(10))
    
    if (fo_num == 0):
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:
        
                file_reader = csv.reader(myfile, delimiter = ',') #Reads csv file  
        
                for row in file_reader: # Goes through every row in file                     
            
                    if (is_first_row == True): #Checks if the row is the first row
                        is_first_row = False #Changes flag to false since there is only 1 first row    
            
                    else: #If the row is not the first row
                        d_act_list.append(row[5])
                        zone = row[6] 
                        pd = variables[0][zone]
                        if (pd != '0'):
                            sc = variables[1][pd]
                            spatial_category_list.append(sc)   
                    
                        else:
                            spatial_category_list.append('0')

    else:
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip:
     
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:
                file_reader = csv.reader(myfile, delimiter = ',') #Reads csv file  
        
                for row in file_reader: # Goes through every row in file                     
            
                    if (is_first_row == True): #Checks if the row is the first row
                        is_first_row = False #Changes flag to false since there is only 1 first row    
            
                    else: #If the row is not the first row
                        d_act_list.append(row[5])
                        zone = row[6] 
                        pd = variables[0][zone]
                        if (pd != '0'):
                            sc = variables[1][pd]
                            spatial_category_list.append(sc)   
                    
                        else:
                            spatial_category_list.append('0')
                
    for i in range (0, len(spatial_category_list), 1):
        if (spatial_category_list[i] in activities):
            activities[spatial_category_list[i]].append(d_act_list[i])
                                
        else:
            activities[spatial_category_list[i]] = [d_act_list[i]]
            
    for key in activities:
        counter  = 0
        for j in range (0, len(activities[key]), 1):
            if (activities[key][j] == 'Market'):
                counter += 1
        shopping_amounts[key] = counter
    del(shopping_amounts['0'])         
    
    return shopping_amounts

#print(Shopping_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trips.csv'))

def Mean_Shopping_Activities():
    '''
    none --> tuple

    This function calculates the mean, standard deviation, and coefficient of variation for the amount
    of shopping activities. It returns a 3-element tuple where the first element is a dictionary of means. 
    The keys are spatial categories and the values are the mean amount of shopping trips for that spatial 
    category. The second element is a dictionary for standard deviation where the keys are the spatial 
    categories and the values are standard deviations. The last element is a dictionary for the coefficient 
    of variation where the keys are the spatial categories and the values are the coefficients of variation. 
    '''

    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    totals_sum = {}
    means_dict = {}
    sd_dict = {}
    sc_cd = {}
    folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    first_file = list(range(50))
    other_files = list(range(10))
    
    for i in range (0, len(folders), 1):
        if (i == 0):
            for j in range (0, len(first_file), 1):
                data.append(Shopping_Activities(i, j))

        else:
            for k in range (0, len(other_files), 1):
                data.append(Shopping_Activities(i, k))


    for i in range (0, len(data), 1):
        for key in data[i]:
             keys_list.append(key)
             values_list.append(data[i][key])
        
    for j in range (0, len(keys_list), 1):
        if (keys_list[j] in group_dict):
            group_dict[keys_list[j]].append(values_list[j])
        
        else:
            group_dict[keys_list[j]] = [values_list[j]]
        
    for key in group_dict:
        totals_sum[key] = sum(group_dict[key])

    for key in totals_sum:
        means_dict[key] = totals_sum[key] / len(data)

    for key in group_dict:
        riemann_sum = 0
        for k in range (0, len(group_dict[key]), 1):
            riemann_sum += (group_dict[key][k] - means_dict[key])**2
        standard_deviation = math.sqrt(riemann_sum / len(group_dict[key]))
        sd_dict[key] = standard_deviation

    for key in means_dict:
        value = sd_dict[key]/means_dict[key]
        sc_cd[key] = value

    return means_dict

#print(Mean_SD_Shopping_Activities())

def Other_Activities(fo_num, fi_num):
    '''
    file --> dict

    This function calculates the amount of other trips that occured in each spatial category. It
    returns a dictionary where the keys are the spatial categories and the values are the amounts 
    of other trips that occured in that specific spatial category.
    '''
    is_first_row = True #Flag to check if the row in the file is the first row. Initialized as true
    spatial_category_list = []
    d_act_list = []
    activities = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    other_amounts = {}
    folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    first_file = list(range(50))
    other_files = list(range(10))
    
    if (fo_num == 0):
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:
        
                file_reader = csv.reader(myfile, delimiter = ',') #Reads csv file  
        
                for row in file_reader: # Goes through every row in file                     
            
                    if (is_first_row == True): #Checks if the row is the first row
                        is_first_row = False #Changes flag to false since there is only 1 first row    
            
                    else: #If the row is not the first row
                        d_act_list.append(row[5])
                        zone = row[6] 
                        pd = variables[0][zone]
                        if (pd != '0'):
                            sc = variables[1][pd]
                            spatial_category_list.append(sc)   
                    
                        else:
                            spatial_category_list.append('0')

    else:
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip:
     
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:
                file_reader = csv.reader(myfile, delimiter = ',') #Reads csv file  
        
                for row in file_reader: # Goes through every row in file                     
            
                    if (is_first_row == True): #Checks if the row is the first row
                        is_first_row = False #Changes flag to false since there is only 1 first row    
            
                    else: #If the row is not the first row
                        d_act_list.append(row[5])
                        zone = row[6] 
                        pd = variables[0][zone]
                        if (pd != '0'):
                            sc = variables[1][pd]
                            spatial_category_list.append(sc)   
                    
                        else:
                            spatial_category_list.append('0')
                
    for i in range (0, len(spatial_category_list), 1):
        if (spatial_category_list[i] in activities):
            activities[spatial_category_list[i]].append(d_act_list[i])
                                
        else:
            activities[spatial_category_list[i]] = [d_act_list[i]]
            
    for key in activities:
        counter  = 0
        for j in range (0, len(activities[key]), 1):
            if (activities[key][j] == 'IndividualOther'):
                counter += 1
        other_amounts[key] = counter
    del(other_amounts['0'])         
    
    return other_amounts
#print(Other_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trips.csv'))

def Mean_Other_Activities():
    '''
    none --> tuple

    This function calculates the mean, standard deviation, and coefficient of variation for the amount
    of other activities. It returns a 3-element tuple where the first element is a dictionary of means. 
    The keys are spatial categories and the values are the mean amount of other trips for that spatial 
    category. The second element is a dictionary for standard deviation where the keys are the spatial 
    categories and the values are standard deviations. The last element is a dictionary for the coefficient 
    of variation where the keys are the spatial categories and the values are the coefficients of variation. 
    '''

    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    totals_sum = {}
    means_dict = {}
    sd_dict = {}
    sc_cd = {}
    folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    first_file = list(range(50))
    other_files = list(range(10))
    
    for i in range (0, len(folders), 1):
        if (i == 0):
            for j in range (0, len(first_file), 1):
                data.append(Other_Activities(i, j))

        else:
            for k in range (0, len(other_files), 1):
                data.append(Other_Activities(i, k))
    df = pd.DataFrame.from_dict(data)
    df.to_csv('other_totals_1000_runs.csv',sep=',')

    for i in range (0, len(data), 1):
        for key in data[i]:
             keys_list.append(key)
             values_list.append(data[i][key])
        
    for j in range (0, len(keys_list), 1):
        if (keys_list[j] in group_dict):
            group_dict[keys_list[j]].append(values_list[j])
        
        else:
            group_dict[keys_list[j]] = [values_list[j]]
        
    for key in group_dict:
        totals_sum[key] = sum(group_dict[key])

    for key in totals_sum:
        means_dict[key] = totals_sum[key] / len(data)

    for key in group_dict:
        riemann_sum = 0
        for k in range (0, len(group_dict[key]), 1):
            riemann_sum += (group_dict[key][k] - means_dict[key])**2
        standard_deviation = math.sqrt(riemann_sum / len(group_dict[key]))
        sd_dict[key] = standard_deviation

    for key in means_dict:
        value = sd_dict[key]/means_dict[key]
        sc_cd[key] = value

    return means_dict

#print(Mean_Sd_Other_Activities())

def School_Activities(filename2, filename1): #DOES NOT WORK YET
    is_first_row2 = True #Flag to check if the row in the file is the first row. Initialized as true
    is_first_row1 = True
    spatial_category_list = []
    d_act_list = []
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    households_list = []
    house_person_status = {}
    person_list = []
    house_person_act = {}
    total_dict = {}
    
    with open(filename2, 'r') as csvfile: #Opens csv file
        
        file_reader2 = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row2 in file_reader2: # Goes through every row in file                     
            
            if (is_first_row2 == True): #Checks if the row is the first row
                is_first_row2 = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row
                d_act_list.append(row2[5])
                households_list.append(row2[0])
                person_list.append(row2[1])
                zone = row2[6] 
                pd = variables[0][zone]
                if (pd != '0'):
                    sc = variables[1][pd]
                    spatial_category_list.append(sc)   
                    
                else:
                    spatial_category_list.append('0')
    
    for i in range (0, len(households_list), 1):
        if (d_act_list[i] == 'School'):
            house_person_act[households_list[i]] = {person_list[i] : spatial_category_list[i]}
        
                  
    with open(filename1, 'r') as csvfile: #Opens csv file
        
        file_reader1 = csv.reader(csvfile, delimiter = ',') #Reads csv file  
        
        for row1 in file_reader1: # Goes through every row in file
            if (is_first_row1 == True): #Checks if the row is the first row
                is_first_row1 = False #Changes flag to false since there is only 1 first row    
            
            else: #If the row is not the first row    
                house_person_status[row1[0]] = {row1[1] : row1[9]}
                
    print(house_person_act)
    print(house_person_status)    
    value = 1            
    for key in house_person_act:
        for key_inner in house_person_act[key]:
            if (key in house_person_status and key_inner in house_person_status[key]):
                if (house_person_act[key][key_inner] not in total_dict):
                    total_dict[house_person_act[key][key_inner]] = {house_person_status[key][key_inner] : 1}
                    
                else:
                    value += 1
                    total_dict[house_person_act[key][key_inner]] = {house_person_status[key][key_inner] : value}
                
    #del(school_dict['0'])         
    
    return total_dict  

#print(School_Activities('C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\trips.csv', 'C:\\Users\\gusevael\\Downloads\\1000 Run Data\\9\\Microsim Results\\persons.csv'))      