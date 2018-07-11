import pandas as pd
import numpy as np
import glob
import os

#Fixed Settings
default_path = 'E:\Python\Workspace\Sort_EXCEL' #Where are the files stored?
search_file_extension = '*.xlsx' #What identifies the files to be considered?
results_file = 'results.xlsx' #What shall be the output-files name?

print('Lets merge some EXCEL-Files, shall we?')
print('Now: Changing path to ',default_path) #Report next step
os.chdir(default_path) #Go to specified directory

#If the results file exists already, delete it, else just continue
try:
    os.remove(results_file)
    print('Now: Removing prior results file {}'.format(results_file)) #Report next step
except:
    pass

print('Now: Listing all the files in the directory...') #Report next step
file_list = [file for file in glob.glob(search_file_extension)] #Make a list of all the files that need to be considered

all_data = pd.DataFrame() #Create an empty pandas data frame to hold the merged data

progress = 0 #Iterator to report the progress

print('Now: Processing the follwing files: \n',file_list) #Report next step
for f in file_list: #Iterate over each file in the list
    progress+=1 #Increment progress-iterator
    print('... reading: {} ({}/{})'.format(f,progress,len(file_list))) #Report progress
    df = pd.read_excel(f)#,header=None) #Load the file, there is no header-line
    df['Source_File'] = f #Make a new column which holds the file name
    #Make a new column that holds the Revision-Nr and other required items for sorting
    all_data = all_data.append(df, ignore_index=True) #Append the new data set to the existing data-frame

'''
print('Now: Filtering the {} found entries'.format(len(all_data))) #Report next step
#Post-processing
all_data.dropna(axis=[0,1], how='all') #Drop rows and columns that are entirely empty
all_data = all_data.sort_values(by=[list(all_data)[0],'Source_File'])
all_data = all_data.drop_duplicates(subset=[list(all_data)[0]],keep='last')
'''
#Get some rules for sorting

print('Now: Saving the {} filtered results to {}'.format(len(all_data),default_path+'\\'+results_file)) #Report next step
with pd.ExcelWriter(results_file) as wb: #Open a socket-object for writing the results to a excel-file
    all_data.to_excel(wb,'results') #Dump the data-frame to the new sheet 'results'
    wb.save() #Save the new file

print('Done!') #Report execution
