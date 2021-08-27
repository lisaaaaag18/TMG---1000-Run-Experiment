import pandas as pd
import plotly.express as px

#Note: All csv files used here are the edited versions of those from 1000_runs_data

# Graph for Mean Trip Durations
#df_durations = pd.read_csv('C:\\Users\\gusevael\\Downloads\\durations_means_50_runs.csv')
#df_durations.Mode = df_durations.Mode.astype('category')
#df_durations.dtypes
#fig = px.bar(df_durations, x='Spatial_Category', y = 'Mean', color = 'Mode', barmode = 'group', title = 'Mean Trip Durations Per Spatial Category')
#fig.show()

# Graph for SD Trip Durations
#df_durations = pd.read_csv('C:\\Users\\gusevael\\Downloads\\durations_sd_50_runs.csv')
#df_durations.Mode = df_durations.Mode.astype('category')
#df_durations.dtypes
#fig = px.bar(df_durations, x='Spatial_Category', y = 'Standard_Deviation', color = 'Mode', barmode = 'group', title = 'Trip Durations Standard Deviations Per Spatial Category')
#fig.show()

# Graph for CV Trip Durations
#df_durations = pd.read_csv('C:\\Users\\gusevael\\Downloads\\durations_cv_50_runs.csv')
#df_durations.Mode = df_durations.Mode.astype('category')
#df_durations.dtypes
#fig = px.bar(df_durations, x='Spatial_Category', y = 'Coefficient_of_Variation', color = 'Mode', barmode = 'group', title = 'Trip Durations Coefficient of Variation Per Spatial Category')
#fig.show()

####################################################################################################################

# Graph for Mean Trip Amounts
#df_trip_amounts = pd.read_csv('C:\\Users\\gusevael\\Downloads\\amounts_means_50_runs.csv')
#df_trip_amounts.Hour = df_trip_amounts.Hour.astype('category')
#df_trip_amounts.dtypes
#fig2 = px.bar(df_trip_amounts, x='Spatial_Category', y = 'Mean', color = 'Hour', barmode = 'group', title = 'Mean Trip Amounts Per Hour Per Spatial Category')
#fig2.show()

# Graph for SD Trip Amounts
#df_trip_amounts = pd.read_csv('C:\\Users\\gusevael\\Downloads\\amounts_sd_50_runs.csv')
#df_trip_amounts.Time = df_trip_amounts.Time.astype('category')
#df_trip_amounts.dtypes
#fig2 = px.bar(df_trip_amounts, x='Spatial_Category', y = 'Standard_Deviation', color = 'Time', barmode = 'group', title = 'Trip Amounts Standard Deviation Per Hour Per Spatial Category')
#fig2.show()

# Graph for CV Trip Amounts
#df_trip_amounts = pd.read_csv('C:\\Users\\gusevael\\Downloads\\amounts_cv_50_runs.csv')
#df_trip_amounts.Time = df_trip_amounts.Time.astype('category')
#df_trip_amounts.dtypes
#fig2 = px.bar(df_trip_amounts, x='Spatial_Category', y = 'Coefficient_of_Variation', color = 'Time', barmode = 'group', title = 'Trip Amounts Coefficient of Variation Per Hour Per Spatial Category')
#fig2.show()

####################################################################################################################

#Graph for Mean Auto Ownership
#data_frame_auto = pd.read_csv('C:\\Users\\gusevael\\Downloads\\auto_means_50_runs.csv')
#data_frame_auto.Amount_of_Cars = data_frame_auto.Amount_of_Cars.astype('category')
#data_frame_auto.dtypes
#fig3 = px.bar(data_frame_auto, x='Spatial_Category', y = 'Mean', color = 'Amount_of_Cars', barmode = 'group', title = 'Mean Number of Cars Per Spatial Category')
#fig3.show()

#Graph for SD Auto Ownership
#data_frame_auto = pd.read_csv('C:\\Users\\gusevael\\Downloads\\auto_sd_50_runs.csv')
#data_frame_auto.Amount_of_Cars = data_frame_auto.Amount_of_Cars.astype('category')
#data_frame_auto.dtypes
#fig3 = px.bar(data_frame_auto, x='Spatial_Category', y = 'Standard_Deviation', color = 'Amount_of_Cars', barmode = 'group', title = 'Auto Ownership Standard Deviation Per Spatial Category')
#fig3.show()

#Graph for CV Auto Ownership
#data_frame_auto = pd.read_csv('C:\\Users\\gusevael\\Downloads\\auto_cv_50_runs.csv')
#data_frame_auto.Amount_of_Cars = data_frame_auto.Amount_of_Cars.astype('category')
#data_frame_auto.dtypes
#fig3 = px.bar(data_frame_auto, x='Spatial_Category', y = 'Coefficient_of_Variation', color = 'Amount_of_Cars', barmode = 'group', title = 'Auto Ownership Coefficient of Variation Per Spatial Category')
#fig3.show()

####################################################################################################################

#Graph for Mean School Activities
#data_frame_school = pd.read_csv('C:\\Users\\gusevael\\Downloads\\school_means_50_runs.csv')
#data_frame_school.Student_Status = data_frame_school.Student_Status.astype('category')
#data_frame_school.dtypes
#fig3 = px.bar(data_frame_school, x='Spatial_Category', y = 'Mean', color = 'Student_Status', barmode = 'group', title = 'Mean Number of School Activities Per Spatial Category')
#fig3.show()

#Graph for SD School Activities
#data_frame_school = pd.read_csv('C:\\Users\\gusevael\\Downloads\\school_sd_50_runs.csv')
#data_frame_school.Student_Status = data_frame_school.Student_Status.astype('category')
#data_frame_school.dtypes
#fig3 = px.bar(data_frame_school, x='Spatial_Category', y = 'Standard_Deviation', color = 'Student_Status', barmode = 'group', title = 'School Activities Standard Deviation Per Spatial Category')
#fig3.show()

#Graph for CV School Activities
#data_frame_school = pd.read_csv('C:\\Users\\gusevael\\Downloads\\school_cv_50_runs.csv')
#data_frame_school.Student_Status = data_frame_school.Student_Status.astype('category')
#data_frame_school.dtypes
#fig3 = px.bar(data_frame_school, x='Spatial_Category', y = 'Coefficient_of_Variation', color = 'Student_Status', barmode = 'group', title = 'School Activities Coefficient of Variation Per Spatial Category')
#fig3.show()
