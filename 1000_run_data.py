import csv
import math
import collections, functools, operator
import pandas as pd
import zipfile
import io

#Note: Each csv file made from data frames must be put into different format to make it easy for plotly to operate

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
    int, int --> dictionary

    This function calculates the average amount of households who have a certain amount of cars
    (0, 1, 2, 3, or 4) in each spatial category. It returns a dictionary with the keys being
    the spatial category and the values being a dictionary where the keys are the number of cars 
    and the values are the amount of households who own that amount of cars.

    fo_num = tells which folders to look at.
    fi_num = tells which file to look at.

    '''   
    is_first_row = True
    spatial_category_list = []
    cars_list = []
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    ownerships_dict = {}
    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
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
            
                    if (is_first_row == True): 
                        is_first_row = False  
            
                    else: 
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
            
                    if (is_first_row == True): 
                        is_first_row = False    
            
                    else: 
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
    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
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

    # Change return variable based on desired output (final_means_dict = means, sd = standard deviation, cv = coefficient of variation)        
    return sd

#Have means as output from Auto_Ownership_Mean_SD_CV()
#data_frame_auto1 = pd.DataFrame.from_dict(Auto_Ownership_Mean_SD_CV(), orient = 'index')
#data_frame_auto1.to_csv('auto_ownership_means_50_runs.csv',sep=',')

#Have sd as output from Auto_Ownership_Mean_SD_CV()
#data_frame_auto2 = pd.DataFrame.from_dict(Auto_Ownership_Mean_SD_CV(), orient = 'index')
#data_frame_auto2.to_csv('auto_ownership_sd_50_runs.csv',sep=',')

#Have means cv output from Auto_Ownership_Mean_SD_CV()
#data_frame_auto3 = pd.DataFrame.from_dict(Auto_Ownership_Mean_SD_CV(), orient = 'index')
#data_frame_auto3.to_csv('auto_ownership_cv_50_runs.csv',sep=',')

#print(Auto_Ownership_Mean_SD_CV())

def Drivers_License(fo_num, fi_num):
    '''
    int, int --> dictionary

    This function calculates the fraction of people (16+ years old) who have a license in each spatial 
    category. It returns a dictionary where the keys are the spatial categories and the values are the 
    fraction of those people who have licenses in that spatial category.

    fo_num = tells which folders to look at.
    fi_num = tells which file to look at.
    '''
    is_first_row = True 
    household_zones_dict = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    sp_license = {}
    total_people = {}

    #Folders for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders for 50 runs
    folders = ['0-49']

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
        
                file_reader = csv.reader(myfile2, delimiter = ',') 
        
                for row in file_reader:                    
            
                    if (is_first_row == True): 
                        is_first_row = False 
            
                    else:               
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
        
                file_reader = csv.reader(myfile2, delimiter = ',') 
        
                for row in file_reader:                  
            
                    if (is_first_row == True): 
                        is_first_row = False 
            
                    else: 
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
                    
def Mean_SD_CV_Drivers_License():
    '''
    none --> dict

    This function calculates the mean, standard deviation, and coefficient of variation for driver's
    license ownership. It returns a dictionary of means or standard deviations or coefficients of
    variation. 
    '''
    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    sd_dict = {}
    means_dict = {}
    totals_sum = {}
    sc_cd = {}

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders used for 50 runs
    folders = ['0-49']

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

    #Change return variable based on desired output (means_dict = means, sd_dict = standard deviation, sc_cd = coefficient of variation)
    return means_dict

#Have means as output from Mean_SD_CV_Drivers_License()
#data_frame_drivers1 = pd.DataFrame.from_dict(Mean_SD_CV_Drivers_License(), orient = 'index')
#data_frame_drivers1.to_csv('drivers_means_50_runs.csv',sep=',')

#Have sd as output from Mean_SD_CV_Drivers_License()
#data_frame_drivers2 = pd.DataFrame.from_dict(Mean_SD_CV_Drivers_License(), orient = 'index')
#data_frame_drivers2.to_csv('drivers_sd_50_runs.csv',sep=',')

#Have means cv output from Mean_SD_CV_Drivers_License()
#data_frame_drivers3 = pd.DataFrame.from_dict(Mean_SD_CV_Drivers_License(), orient = 'index')
#data_frame_drivers3.to_csv('drivers_cv_50_runs.csv',sep=',')

#print(Mean_SD_CV_Drivers_License())

def Trip_Amounts(fo_num, fi_num):
    '''
    int, int --> dict

    This function calculates the amount of trips that occured every hour during the period of 12am
    to 12am the next day (24 hours) for each spatial category. The function returns a dictionary
    where the keys are the spatial categories and the values are a list where each element represents 
    the hour and how many trips occured in that hour, starting at 12 am.

    '''
    is_first_row = True
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

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders for 50 runs
    folders = ['0-49']
    first_file = list(range(50))
    other_files = list(range(10))
    
    if (fo_num == 0):
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'households.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')
    
                for row in file_reader1:
                    if (is_first_row1 == True):
                       is_first_row1 = False  
                
                    else:        
                        household_zones_dict[row[0]] = row[1]    

    
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'trip_modes.csv')), encoding="utf-8") as myfile2:
        
                file_reader = csv.reader(myfile2, delimiter = ',') 
        
                for row in file_reader: 
            
                    if (is_first_row == True): 
                        is_first_row = False    
            
                    else: 
                        start_list.append(row[4])
                        weight_list.append(row[6])
                
                        if(row[0] in household_zones_dict):
                            zone = household_zones_dict[row[0]]
                            planning_district = variables[0][zone]
                            spatial_category = variables[1][planning_district]
                            spatial_category_list.append(spatial_category) 

    else:
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'households.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')
    
                for row in file_reader1:
                    if (is_first_row1 == True):
                       is_first_row1 = False    
                
                    else:      
                        household_zones_dict[row[0]] = row[1]    

    
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'trip_modes.csv')), encoding="utf-8") as myfile2:
        
                file_reader = csv.reader(myfile2, delimiter = ',') 
        
                for row in file_reader: 
            
                    if (is_first_row == True): 
                        is_first_row = False 
            
                    else: 
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
       
def Mean_SD_CV_Trip_Amounts(): 
    '''
    None --> dict

    This function calculates the mean, standard deviation, and coefficient of variation for the trip
    amounts across 1000 runs. It returns a dictionary of means or standard deviations or coefficients 
    of variation. 
    '''

    data = []
    totals_dict = {}
    sum_dict = {}
    final_means_dict = {}
    riemann_dict = {}
    sd = {}
    cv = {}

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders used for 50 runs
    folders = ['0-49']
    first_file = list(range(50))
    other_files = list(range(10))

    for i in range (0, len(folders), 1):
        if (i == 0):
            for j in range (0, len(first_file), 1):
                data.append(Trip_Amounts(i, j))

        else:
            for k in range (0, len(other_files), 1):
                data.append(Trip_Amounts(i, k))

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

    #Change return variable based on desired output (final_means_dict = means, sd_dict = standard deviation, cv = coefficient of variation)        
    return final_means_dict

#Have means as output from Mean_SD_CV_Trip_Amounts()
#data_frame_amounts1 = pd.DataFrame.from_dict(Mean_SD_CV_Trip_Amounts(), orient = 'index')
#data_frame_amounts1.to_csv('trip_amounts_means_50_runs.csv',sep=',')

#Have sd as output from Mean_SD_CV_Trip_Amounts()
#data_frame_amounts2 = pd.DataFrame.from_dict(Mean_SD_CV_Trip_Amounts(), orient = 'index')
#data_frame_amounts2.to_csv('trip_amounts_sd_50_runs.csv',sep=',')

#Have cv as output from Mean_SD_CV_Trip_Amounts()
#data_frame_amounts3 = pd.DataFrame.from_dict(Mean_SD_CV_Trip_Amounts(), orient = 'index')
#data_frame_amounts3.to_csv('trip_amounts_cv_50_runs.csv',sep=',')

#print(Mean_SD_CV_Trip_Amounts())

def Trip_Durations(fo_num, fi_num):
    '''
    int, int --> dict

    This function determines the average trip time for each spatial category by trip modes. It returns a nested
    dictionary where the keys are the spatial categories, and the values are dictionaries with keys being modes
    of transportation and values being the average trip time for that specific mode.

    '''
    is_first_row2 = True 
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

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
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
                    if (is_first_row1 == True): 
                        is_first_row1 = False   
            
                    else:       
                        household_zones_dict[row[0]] = row[1]
    
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'trip_modes.csv')), encoding="utf-8") as myfile2:
        
                file_reader = csv.reader(myfile2, delimiter = ',') 
        
                for row in file_reader: 
            
                    if (is_first_row2 == True): 
                        is_first_row2 = False  
            
                    else:
                        trip_type.append(row[3])
                        duration = (float(row[5]) - float(row[4]))
                        durations_list.append(duration)
                        weight_list.append(float(row[6]))
                
                        if(row[0] in household_zones_dict):
                            zone = household_zones_dict[row[0]]
                            planning_district = variables[0][zone]
                            spatial_category = variables[1][planning_district]
                            spatial_category_list.append(spatial_category)

    else:
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'households.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')

                for row in file_reader1:
                    if (is_first_row1 == True): 
                        is_first_row1 = False  
            
                    else:             
                        household_zones_dict[row[0]] = row[1]
    
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'trip_modes.csv')), encoding="utf-8") as myfile2:
        
                file_reader = csv.reader(myfile2, delimiter = ',') 
        
                for row in file_reader: 
            
                    if (is_first_row2 == True): 
                        is_first_row2 = False 
            
                    else: 
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

def Trip_Durations_Mean_SD_CV():  
    '''
    None --> dict

    This function calculates the mean, standard deviation, and coefficient of variation for the trip
    durations across 1000 runs. It returns a dictionary of means or standard deviations or coefficients of
    variation. 
    '''
    data = []
    totals_dict = {}
    sum_dict = {}
    final_means_dict = {}
    riemann_dict = {}
    sd = {}
    cv = {}

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']  
    
    #Folders used for 50 runs
    folders = ['0-49']
    first_file = list(range(50))
    other_files = list(range(10))

    for i in range (0, len(folders), 1):
        if (i == 0):
            for j in range (0, len(first_file), 1):
                data.append(Trip_Durations(i, j))

        else:
            for k in range (0, len(other_files), 1):
                data.append(Trip_Durations(i, k))  

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

    #Change return variable based on desired output (final_means_dict = means, sd = standard deviation, cv = coefficient of variation)        
    return final_means_dict

#Have means as output from Trip_Durations_Mean_SD_CV()
#df_durations1 = pd.DataFrame.from_dict(Trip_Durations_Mean_SD_CV(), orient = 'index')
#df_durations1.to_csv('trip_durations_means_50_runs.csv',sep=',')

#Have sd as output from Trip_Durations_Mean_SD_CV()
#df_durations2 = pd.DataFrame.from_dict(Trip_Durations_Mean_SD_CV(), orient = 'index')
#df_durations2.to_csv('trip_durations_sd_50_runs.csv',sep=',')

#Have cv as output from Trip_Durations_Mean_SD_CV()
#df_durations3 = pd.DataFrame.from_dict(Trip_Durations_Mean_SD_CV(), orient = 'index')
#df_durations3.to_csv('trip_durations_cv_50_runs.csv',sep=',')

#print(Trip_Durations_Mean_SD_CV())

def Shopping_Activities(fo_num, fi_num):
    '''
    int, int --> dict

    This function calculates the amount of shopping trips that occured in each spatial category. It
    returns a dictionary where the keys are the spatial categories and the values are the amounts 
    of shopping trips that occured in that specific spatial category.

    fo_num = tells which folders to look at.
    fi_num = tells which file to look at.
    '''
    is_first_row = True 
    spatial_category_list = []
    d_act_list = []
    activities = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    shopping_amounts = {}

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders used for 50 runs
    folders = ['0-49']

    first_file = list(range(50))
    other_files = list(range(10))
    
    if (fo_num == 0):
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:
        
                file_reader = csv.reader(myfile, delimiter = ',') 
        
                for row in file_reader:                 
            
                    if (is_first_row == True): 
                        is_first_row = False 
            
                    else: 
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
                file_reader = csv.reader(myfile, delimiter = ',') 
        
                for row in file_reader:             
            
                    if (is_first_row == True): 
                        is_first_row = False   
            
                    else: 
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

def Mean_SD_CV_Shopping_Activities():
    '''
    none --> dict

    This function calculates the mean, standard deviation, and coefficient of variation for the amount
    of shopping activities. It returns a dictionary of means or standard deviations or coefficients of
    variation.  
    '''

    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    totals_sum = {}
    means_dict = {}
    sd_dict = {}
    sc_cd = {}

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders for 50 runs
    folders = ['0-49']
    
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

    #Change return variable based on desired output (means_dict = means, sd_dict = standard deviation, sc_cd = coefficient of variation)
    return means_dict

#Have means as output from Mean_SD_CV_Shopping_Activities()
#df_shopping1 = pd.DataFrame.from_dict(Mean_SD_CV_Shopping_Activities(), orient = 'index')
#df_shopping1.to_csv('shopping_means_50_runs.csv',sep=',')

#Have sd as output from Mean_SD_CV_Shopping_Activities()
#df_shopping2 = pd.DataFrame.from_dict(Mean_SD_CV_Shopping_Activities(), orient = 'index')
#df_shopping2.to_csv('shopping_sd_50_runs.csv',sep=',')

#Have cv as output from Mean_SD_CV_Shopping_Activities()
#df_shopping3 = pd.DataFrame.from_dict(Mean_SD_CV_Shopping_Activities(), orient = 'index')
#df_shopping3.to_csv('shopping_cv_50_runs.csv',sep=',')

#print(Mean_SD_CV_Shopping_Activities())

def Other_Activities(fo_num, fi_num):
    '''
    int, int --> dict

    This function calculates the amount of other trips that occured in each spatial category. It
    returns a dictionary where the keys are the spatial categories and the values are the amounts 
    of other trips that occured in that specific spatial category.
    '''
    is_first_row = True 
    spatial_category_list = []
    d_act_list = []
    activities = {}
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    other_amounts = {}

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders used for 50 runs
    folders = ['0-49']
    
    first_file = list(range(50))
    other_files = list(range(10))
    
    if (fo_num == 0):
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:
        
                file_reader = csv.reader(myfile, delimiter = ',')  
        
                for row in file_reader:                     
            
                    if (is_first_row == True): 
                        is_first_row = False   
            
                    else: 
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
                file_reader = csv.reader(myfile, delimiter = ',') 
        
                for row in file_reader:                    
            
                    if (is_first_row == True): 
                        is_first_row = False  
            
                    else: 
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

def Mean_SD_CV_Other_Activities():
    '''
    none --> dict

    This function calculates the mean, standard deviation, and coefficient of variation for the amount
    of other activities. It returns a dictionary of means or standard deviations or coefficients of
    variation.  
    '''

    data = []
    keys_list = []
    values_list = []
    group_dict = {}
    totals_sum = {}
    means_dict = {}
    sd_dict = {}
    sc_cd = {}

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders for 50 runs
    folders = ['0-49']
    
    first_file = list(range(50))
    other_files = list(range(10))
    
    for i in range (0, len(folders), 1):
        if (i == 0):
            for j in range (0, len(first_file), 1):
                data.append(Other_Activities(i, j))

        else:
            for k in range (0, len(other_files), 1):
                data.append(Other_Activities(i, k))

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

    #Change return variable based on desired output (means_dict = means, sd_dict = standard deviation, sc_cd = coefficient of variation)
    return means_dict

#Have means as output from Mean_SD_CV_Other_Activities()
#df_other1 = pd.DataFrame.from_dict(Mean_SD_CV_Other_Activities(), orient = 'index')
#df_other1.to_csv('other_means_50_runs.csv',sep=',')

#Have sd as output from Mean_SD_CV_Other_Activities()
#df_other2 = pd.DataFrame.from_dict(Mean_SD_CV_Other_Activities(), orient = 'index')
#df_other2.to_csv('other_sd_50_runs.csv',sep=',')

#Have cv as output from Mean_SD_CV_Other_Activities()
#df_other3 = pd.DataFrame.from_dict(Mean_SD_CV_Other_Activities(), orient = 'index')
#df_other3.to_csv('other_cv_50_runs.csv',sep=',')

#print(Mean_SD_CV_Other_Activities())

def School_Activities(fo_num, fi_num):
    '''
    int, int --> dict

    This function calculates the amount of school trips that occured in each spatial category. It
    returns a dictionary where the keys are the spatial categories and the values are nested
    dictionaries where the keys are student statuses and the values are the amounts of school trips.
    '''
    is_first_row2 = True 
    is_first_row1 = True
    spatial_category_list = []
    d_act_list = []
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    households_list = []
    house_person_status = {}
    person_list = []
    house_person_act = {}
    sp_list = []
    status_list = []
    final_dict = {}
    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders used for 50 runs
    folders = ['0-49']

    first_file = list(range(50))
    other_files = list(range(10))
    
    if (fo_num == 0):
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')

                for row in file_reader1:
                    if (is_first_row2 == True): 
                        is_first_row2 = False 
            
                    else: 
                        d_act_list.append(row[5])
                        households_list.append(row[0])
                        person_list.append(row[1])
                        zone = row[6] 
                        pd = variables[0][zone]
                        if (pd != '0'):
                            sc = variables[1][pd]
                            spatial_category_list.append(sc)   
                    
                        else:
                            spatial_category_list.append('0')
    
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'persons.csv')), encoding="utf-8") as myfile2:
        
                file_reader = csv.reader(myfile2, delimiter = ',') 
        
                for row in file_reader:
            
                    if (is_first_row1 == True): 
                        is_first_row1 = False 
            
                    else: 
                        if (row[0] in house_person_status):
                            house_person_status[row[0]][row[1]] = row[9]
                            new_dict = house_person_status[row[0]]
                            house_person_status[row[0]] = new_dict
                    
                        else:
                            house_person_status[row[0]] = {row[1] : row[9]}

    else:
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')

                for row in file_reader1:
                    if (is_first_row2 == True): 
                        is_first_row2 = False 
            
                    else: 
                        d_act_list.append(row[5])
                        households_list.append(row[0])
                        person_list.append(row[1])
                        zone = row[6] 
                        pd = variables[0][zone]
                        if (pd != '0'):
                            sc = variables[1][pd]
                            spatial_category_list.append(sc)   
                    
                        else:
                            spatial_category_list.append('0')
    
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'persons.csv')), encoding="utf-8") as myfile2:
        
                file_reader = csv.reader(myfile2, delimiter = ',') 
        
                for row in file_reader:
            
                    if (is_first_row1 == True): 
                        is_first_row1 = False    
            
                    else: 
                        if (row[0] in house_person_status):
                            house_person_status[row[0]][row[1]] = row[9]
                            new_dict = house_person_status[row[0]]
                            house_person_status[row[0]] = new_dict
                    
                        else:
                            house_person_status[row[0]] = {row[1] : row[9]}

    for i in range (0, len(households_list), 1):
        if (d_act_list[i] == 'School'):
            if (households_list[i] in house_person_act):
                house_person_act[households_list[i]][person_list[i]] = spatial_category_list[i]
                new_dict = house_person_act[households_list[i]]
                house_person_act[households_list[i]] = new_dict
                
            else:
                house_person_act[households_list[i]] = {person_list[i] : spatial_category_list[i]}

    for key in house_person_act:
        for key1 in house_person_act[key]:
            sp_list.append(house_person_act[key][key1])
            
            if (key in house_person_status and key1 in house_person_status[key]):
                status_list.append(house_person_status[key][key1])
    
    for j in range (0, len(sp_list), 1):
        if sp_list[j] in final_dict:
            if status_list[j] in final_dict[sp_list[j]]:
                final_dict[sp_list[j]][status_list[j]] += 1
                
            else:
                final_dict[sp_list[j]][status_list[j]] = 1
                
        else:
            final_dict[sp_list[j]] = {status_list[j] : 1}

    return final_dict

def School_Activities_Mean_SD_CV():
    '''
    none --> dict

    This function calculates the mean, standard deviation, and coefficient of variation for the amount
    of school activities. It returns a dictionary of means or standard deviations or coefficients of
    variation.
    '''
    data = []
    totals_dict = {}
    sum_dict = {}
    final_means_dict = {}
    riemann_dict = {}
    sd = {}
    cv = {}

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs)
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']  
    
    #Folders for 50 runs
    folders = ['0-49']
    first_file = list(range(50))
    other_files = list(range(10))

    for i in range (0, len(folders), 1):
        if (i == 0):
            for j in range (0, len(first_file), 1):
                data.append(School_Activities(i, j))

        else:
            for k in range (0, len(other_files), 1):
                data.append(School_Activities(i, k))  

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

    #Change return variable based on desired output (final_means_dict = means, sd = standard deviation, cv = coefficient of variation)        
    return final_means_dict

#Have means as output from School_Activities_Mean_SD_CV()
#df_school1 = pd.DataFrame.from_dict(School_Activities_Mean_SD_CV(), orient = 'index')
#df_school1.to_csv('school_means_50_runs.csv',sep=',')

#Have sd as output from School_Activities_Mean_SD_CV()
#df_school2 = pd.DataFrame.from_dict(School_Activities_Mean_SD_CV(), orient = 'index')
#df_school2.to_csv('school_sd_50_runs.csv',sep=',')

#Have cv as output from School_Activities_Mean_SD_CV()
#df_school3 = pd.DataFrame.from_dict(School_Activities_Mean_SD_CV(), orient = 'index')
#df_school3.to_csv('school_cv_50_runs.csv',sep=',')

#print(School_Activities_Mean_SD_CV())

def Work_Activities(fo_num, fi_num):
    '''
    int, int --> dict

    This function calculates the amount of work trips that occured in each spatial category. It
    returns a dictionary where the keys are the spatial categories and the values are nested
    dictionaries where the keys are employment statuses and the values are another dictionary.
    The keys are the occupation sectors and the values are the amounts of work trips for that 
    occupation sector.
    '''
    is_first_row2 = True 
    is_first_row1 = True
    spatial_category_list = []
    d_act_list = []
    variables = Conversions('C:\\Users\\gusevael\\Downloads\\GTAModelV4ToPD.csv', 'C:\\Users\\gusevael\\Downloads\\PD_Spatial_Category_Conversion.csv')
    households_list = []
    house_person_status = {}
    person_list = []
    house_person_act = {}
    occupation_list = []
    house_person_occupation = {}
    sp_list = []
    status_list = []
    final_dict = {}
    #Folders used for 1000 runs
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']
    
    #Folders used for 50 runs
    folders = ['0-49']

    first_file = list(range(50))
    other_files = list(range(10))
    
    if (fo_num == 0):
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')  
        
                for row1 in file_reader1: # Goes through every row in file                     
            
                    if (is_first_row1 == True): #Checks if the row is the first row
                        is_first_row1 = False #Changes flag to false since there is only 1 first row    
            
                    else: #If the row is not the first row
                        d_act_list.append(row1[5])
                        households_list.append(row1[0])
                        person_list.append(row1[1])
                        zone = row1[6] 
                        pd = variables[0][zone]
                        if (pd != '0'):
                            sc = variables[1][pd]
                            spatial_category_list.append(sc)   
                    
                        else:
                            spatial_category_list.append('0')
        
                  
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(first_file[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'persons.csv')), encoding="utf-8") as myfile2:
        
                file_reader2 = csv.reader(myfile2, delimiter = ',')  
        
                for row2 in file_reader2: 
                    if (is_first_row2 == True): 
                        is_first_row2 = False 
            
                    else: 

                        if (row2[0] in house_person_status):
                            house_person_status[row2[0]][row2[1]] = row2[6]
                            new_dict = house_person_status[row2[0]]
                            house_person_status[row2[0]] = new_dict
                    
                        elif (row2[0] not in house_person_status):
                            house_person_status[row2[0]] = {row2[1] : row2[6]}

                        if (row2[0] in house_person_occupation):
                            house_person_occupation[row2[0]][row2[1]] = row2[7]
                            new_dict = house_person_occupation[row2[0]]
                            house_person_occupation[row2[0]] = new_dict

                        elif (row2[0] not in house_person_occupation):
                            house_person_occupation[row2[0]] = {row2[1] : row2[7]}


    else:
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip:
         
            with io.TextIOWrapper(myzip.open(Get_Archive(myzip, 'trips.csv')), encoding="utf-8") as myfile:

                file_reader1 = csv.reader(myfile, delimiter = ',')  
        
        for row1 in file_reader1:                    
            
            if (is_first_row1 == True): 
                is_first_row1 = False 
            
            else: 
                d_act_list.append(row1[5])
                households_list.append(row1[0])
                person_list.append(row1[1])
                zone = row1[6] 
                pd = variables[0][zone]
                if (pd != '0'):
                    sc = variables[1][pd]
                    spatial_category_list.append(sc)   
                    
                else:
                    spatial_category_list.append('0')
        
                  
        with zipfile.ZipFile(r'\\fs-01\Shared$\Groups\TMG\Research\2021\UMC\1000 Runs\Runs\\' + folders[fo_num] +'\\' + str(other_files[fi_num]) + '.zip') as myzip2:
         
            with io.TextIOWrapper(myzip2.open(Get_Archive(myzip2, 'persons.csv')), encoding="utf-8") as myfile2:
        
                file_reader2 = csv.reader(myfile2, delimiter = ',') 
        
                for row2 in file_reader2:
                    if (is_first_row2 == True):
                        is_first_row2 = False   
            
                    else: 

                        if (row2[0] in house_person_status):
                            house_person_status[row2[0]][row2[1]] = row2[6]
                            new_dict = house_person_status[row2[0]]
                            house_person_status[row2[0]] = new_dict
                    
                        elif (row2[0] not in house_person_status):
                            house_person_status[row2[0]] = {row2[1] : row2[6]}

                        if (row2[0] in house_person_occupation):
                            house_person_occupation[row2[0]][row2[1]] = row2[7]
                            new_dict = house_person_occupation[row2[0]]
                            house_person_occupation[row2[0]] = new_dict

                        elif (row2[0] not in house_person_occupation):
                            house_person_occupation[row2[0]] = {row2[1] : row2[7]}

    for i in range (0, len(households_list), 1):
        if (d_act_list[i] == 'PrimaryWork'):
            if (households_list[i] in house_person_act):
                house_person_act[households_list[i]][person_list[i]] = spatial_category_list[i]
                new_dict = house_person_act[households_list[i]]
                house_person_act[households_list[i]] = new_dict
                
            else:
                house_person_act[households_list[i]] = {person_list[i] : spatial_category_list[i]} 
    
    for key in house_person_act:
        for key1 in house_person_act[key]:
            sp_list.append(house_person_act[key][key1])
            
            if (key in house_person_status and key1 in house_person_status[key]):
                status_list.append(house_person_status[key][key1])

            if (key in house_person_occupation and key1 in house_person_occupation[key]):
                occupation_list.append(house_person_occupation[key][key1])
    
    for j in range (0, len(sp_list), 1):
        if sp_list[j] in final_dict:
            if status_list[j] in final_dict[sp_list[j]]:
                if (occupation_list[j] in final_dict[sp_list[j]][status_list[j]]):
                    final_dict[sp_list[j]][status_list[j]][occupation_list[j]] += 1
                
                else:
                    final_dict[sp_list[j]][status_list[j]][occupation_list[j]] = 1

            else:
                final_dict[sp_list[j]][status_list[j]] = {occupation_list[j] : 1}
                
        else:
            inner_dict = {occupation_list[j] : 1}
            final_dict[sp_list[j]] = {status_list[j] : inner_dict}

    return final_dict

def Work_Activities_Mean():
    '''
    none --> dict

    This function calculates the mean, standard deviation, and coefficient of variation for the amount
    of work activities. It returns a dictionary of means or standard deviations or coefficients of
    variation.
    '''
    data = []
    totals_dict = {}
    sd = {}
    cv = {}

    #Folders used for 1000 runs (uncomment this line when you wish to collect data from 1000 runs) 
    #folders = ['0-49', '50-59', '60-69', '70-79', '80-89', '90-99', '100-109', '110-119', '120-129', '130-139', '140-149', '150-159', '160-169', '170-179', '180-189', '190-199', '200-209', '210-219', '220-229', '230-239', '240-249', '250-259', '260-269', '270-279', '280-289', '290-299', '300-309', '310-319', '320-329', '330-339', '340-349', '350-359', '360-369', '370-379', '380-389', '390-399', '400-409', '410-419', '420-429', '430-439', '440-449', '450-459', '460-469', '470-479', '480-489', '490-499', '500-509', '510-519', '520-529', '530-539', '540-549', '550-559', '560-569', '570-579', '580-589', '590-599', '600-609', '610-619', '620-629', '630-639', '640-649', '650-659', '660-669', '670-679', '680-689', '690-699', '700-709', '710-719', '720-729', '730-739', '740-749', '750-759', '760-769', '770-779', '780-789', '790-799', '800-809', '810-819', '820-829', '830-839', '840-849', '850-859', '860-869', '870-879', '880-889', '890-899', '900-909', '910-919', '920-929', '930-939', '940-949', '950-959', '960-969', '970-979', '980-989', '990-999']  
    
    #Folders used for 50 runs
    folders = ['0-49']
    
    first_file = list(range(50))
    other_files = list(range(10))
    means_dict = {}
    riemann_sums = {}

    for i in range (0, len(folders), 1):
        if (i == 0):
            for j in range (0, len(first_file), 1):
                data.append(Work_Activities(i, j))

        else:
            for k in range (0, len(other_files), 1):
                data.append(Work_Activities(i, k)) 

    for i in range (0, len(data), 1):
            for key1 in data[i]:
                for key2 in data[i][key1]:
                    for key3 in data[i][key1][key2]:
                        if (key1 in totals_dict and key2 in totals_dict[key1] and key3 in totals_dict[key1][key2]):
                            totals_dict[key1][key2][key3].append(data[i][key1][key2][key3])
                    
                        else:
                            if (key1 not in totals_dict):
                                totals_dict[key1] = {key2: {key3 : [data[i][key1][key2][key3]]}}    
                            
                            elif (key2 not in totals_dict[key1]):
                                totals_dict[key1][key2] = {key3 : [data[i][key1][key2][key3]]}
                                
                            elif (key3 not in totals_dict[key1][key2]):
                                totals_dict[key1][key2][key3] = [data[i][key1][key2][key3]]
                                
    length = len(totals_dict[key1][key2][key3])
    
    for key1 in totals_dict:
        inner = {}
        for key2 in totals_dict[key1]:
            inner_inner = {}
            for key3 in totals_dict[key1][key2]:
                value = sum(totals_dict[key1][key2][key3])/length
                
                inner_inner[key3] = value
            inner[key2] = inner_inner
        means_dict[key1] = inner

    for i in range (0, len(data), 1):
        for key1 in data[i]:
            for key2 in data[i][key1]:
                for key3 in data[i][key1][key2]:
                    if (key1 in riemann_sums and key2 in riemann_sums[key1] and key3 in riemann_sums[key1][key2]):
                        riemann_sums[key1][key2][key3] += (data[i][key1][key2][key3] - means_dict[key1][key2][key3])**2
                        
                    else:
                        if (key1 not in riemann_sums):
                            riemann_sums[key1] = {key2: {key3 : (data[i][key1][key2][key3] - means_dict[key1][key2][key3])**2}}    
                                
                        elif (key2 not in riemann_sums[key1]):
                            riemann_sums[key1][key2] = {key3 : (data[i][key1][key2][key3] - means_dict[key1][key2][key3])**2}
                                    
                        elif (key3 not in riemann_sums[key1][key2]):
                            riemann_sums[key1][key2][key3] = (data[i][key1][key2][key3] - means_dict[key1][key2][key3])**2   

    for key1 in riemann_sums:
        final_inner = {}
        for key2 in riemann_sums[key1]:
            final_inner_inner = {}
            for key3 in riemann_sums[key1][key2]:
                final_value = math.sqrt(riemann_sums[key1][key2][key3]/len(data))
                
                final_inner_inner[key3] = final_value
            final_inner[key2] = final_inner_inner
        sd[key1] = final_inner                
    print(sd)    
    for key1 in sd:
        cv_inner = {}
        for key2 in riemann_sums[key1]:
            cv_inner_inner = {}
            for key3 in riemann_sums[key1][key2]:
                cv_value = sd[key1][key2][key3]/means_dict[key1][key2][key3]
                    
                cv_inner_inner[key3] = cv_value
            cv_inner[key2] = cv_inner_inner
        cv[key1] = cv_inner                    
                            
    return means_dict

#print(Work_Activities_Mean())