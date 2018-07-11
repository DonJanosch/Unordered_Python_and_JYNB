import pandas as pd
import numpy as np
import glob, os, math, warnings,sys, datetime, itertools

os.chdir(os.getcwd().replace('scripts','MTO_Tool'))

logging = True

if logging:
    #Start log-File
    print('Start script and log-file...')
    old_stdout = sys.stdout
    log_file = open('{:%Y%m%d%H%M%S}_script_log_file.log'.format(datetime.datetime.now()),'w')
    sys.stdout = log_file
    print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
else:
    print('Not creating a log-file\n')

#Fixed parameters
print('Starting Script for generating material order table from Grasmann-table.\nNow: setting up parameters...')
result_file = 'results.xlsx'
result_table = 'Mengenliste'
exclude_KKS_items = ['0ND','P1','0GC','0LF'] #Search for part-string in column 'Part Name'

#General functions
warnings.simplefilter(action='ignore')
def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]

def laufmeter_ermitteln(x,standard_pipe_length=6,excess_material_factor=1.1):
    return int(math.ceil(x*excess_material_factor/standard_pipe_length)*standard_pipe_length)

def read_excel_data(sheet):
    #Reading Data
    print('Now: reading {} into momory...'.format(source_table)) #Report next step
    df = xl.parse(sheet)
    print('Finished: reading the file')
    return df

def save_excel_data(dataframe_to_save):
    target_file = insert_str(source_table,'_'+result_table+'_'+sheet,len(source_table)-4).replace('.xls','.xlsx')
    print('Now: Saving the calculated results to \'{}\'...'.format(source_file_path+'\\'+target_file))
    with pd.ExcelWriter(result_file) as writer:
        dataframe_to_save.dropna(axis=1, how='all').reset_index(drop=True).to_excel(writer,result_table,index=True)
        try:
            writer.save()
        except:
            print('ERROR: The file \'{}\' cant be written, maybe it is opened with another Software. Please close and try again.'.format(source_file_path+'\\'+result_file))
    try:
        os.rename(result_file,target_file)
        print('Finished: Entire job for file {} finished successfully!\n'.format(source_table))
    except:
        print('ERROR: A file with name \'{}\' already existed in the directory \'{}\'. The newly generated results file now is named \'{}\'.\n'.format(target_file,source_file_path,result_file))

def clean_excel_data(df):
    print('Now: cleaning raw data...')
    all_data = df.rename(columns=lambda x:x.strip()) #Stripping empty ' ' in columnnames
    all_data = all_data[all_data.index.notnull()] #Droping empty rows wich might be remarks or malformed entries
    for item in exclude_KKS_items:
        all_data = all_data[all_data['Part Name'].str.contains(item)==False]
    print('Finished: cleaning raw data')
    return all_data

def find_unique_set(list_of_unique_parameters,dataset,accumulating_item,safety_margin = 1):
    #Get depth of search-space
    depth = len(list_of_unique_parameters)
    #Get list of lists with unique-sets
    list_of_lists = [dataset[item].unique() for item in list_of_unique_parameters]
    #Search combinations of unique sets
    combinations = list(itertools.product(*list_of_lists))
    searches = [dict(zip(list_of_unique_parameters,combination)) for combination in combinations]
    df_results = pd.DataFrame(columns=df.columns)
    for search in searches: #<=== Als verschachtelte Schleife zwar nicht das effizienteste aber geht
        df_filtered = dataset
        for column,value in search.items():
            df_filtered = df_filtered[df_filtered[column]==value]
        if len(df_filtered)>0:
            b = df_filtered.iloc[0]
            if accumulating_item in df_filtered.columns:
                b[accumulating_item + '_summed'] = math.ceil(df_filtered[accumulating_item].sum()*safety_margin)
            else:
                    b['item_count'] = int(math.ceil(len(df_filtered)*safety_margin))
            df_results = df_results.append(b)
    return df_results

#OS operations
if not 'source_file_path' in locals():
    source_file_path = ''
print('Now: changing path to {}...'.format(source_file_path)) #Report next step
try:
    os.chdir(source_file_path) #Go to specified directory
except:
    print('ERROR: could not get to path \'{}\'. Can still work if the file is in the same directory as this script.'.format(source_file_path))

#Get list of all files by name
source_extension = '*.xls'
print('Now: Indexing all \'{}\' files to process...'.format(source_extension))
source_tables = [file for file in glob.glob(source_extension)]
print('Found these files to process:\n',source_tables,'\nNow: Start iterating over file-list...\n')

#Iterate over all documents which need computing
for source_table in source_tables:
    print('Now: Processing file \'{}\''.format(source_table))
    #Get list of all avaliable sheets in the excel file
    xl = pd.ExcelFile(source_table)
    list_of_sheets = xl.sheet_names

    #Iterate over all sheets and determine what todo with it
    for sheet in list_of_sheets:
        #Rohre - How shal the sheet 'Rohre' be treated?
        if sheet == 'Rohre' or sheet =='Rohre-Fittinge-Armaturen':
            print('Now: Processing sheet \'{}\''.format(sheet))
            #Specific parameters
            filter_by = 'Part Name'
            accumulating_objects = ['Pipe'] #Accumulating all objects over attribute 'Part Name' and summing them up. More items can be added.
            unique_identifier = 'NPD1'
            summing_parameter_pipe = 'Pipe Length [m]'
            suming_identifier_pipe = 'Summed Pipe Length [m]'
            ordering_identifier_pipe = 'Total Pipe Length [m]'
            summing_parameter_shaped_parts = 'Description'
            summing_identifier_shaped_parts = 'Total number [pcs]'
            parameters_for_output_list = ['Description','Part Name','NPD1','OD1 [mm]','WT1 [mm]','NPD2','OD2 [mm]','WT2 [mm]','Material','DIN',summing_identifier_shaped_parts,suming_identifier_pipe,ordering_identifier_pipe]
            replacement_column_names = {'NPD1':'DN1','NPD2':'DN2','OD1 [mm]':'Da1 [mm]','OD2 [mm]':'Da2 [mm]','WT1 [mm]':'s1 [mm]','WT2 [mm]':'s2 [mm]'}
            safety_margin_pipe = 1.1 #10% mehr Rohr berücksichtigen
            safety_margin_parts = 1.1 #10% mehr Einbaustücke berücksichtigen
            
            #Read and clean Data
            df = read_excel_data(sheet)
            all_data = clean_excel_data(df)

            #Processing Data
            print('Now: calculating new table...')
            order_data = pd.DataFrame(columns=all_data.columns)
            ###Calculating Pipes
            for obj in accumulating_objects:
                a = all_data[all_data[filter_by]==obj]
                for idx in a[unique_identifier].unique():
                    b = a[a[unique_identifier]==idx]
                    b_sum = b[summing_parameter_pipe].sum()
                    b[suming_identifier_pipe] = b_sum
                    b[ordering_identifier_pipe] = laufmeter_ermitteln(b_sum,excess_material_factor=safety_margin_pipe)
                    order_data = order_data.append(b.iloc[0])
            ###Calculating spahed parts
            item_list = all_data[summing_parameter_shaped_parts].unique()
            a = all_data[all_data[summing_parameter_pipe].isnull()]
            for obj in item_list:
                b = a[a[summing_parameter_shaped_parts]==obj]
                b_sum = len(b.index)
                if b_sum >0:
                    b[summing_identifier_shaped_parts] = int(math.ceil(b_sum*safety_margin_parts))
                    order_data = order_data.append(b.iloc[0])
            print('Finished: calculating new table')

            #Save results
            save_excel_data(order_data[parameters_for_output_list].sort_values(by=[summing_parameter_shaped_parts,unique_identifier]).rename(index=str,columns=replacement_column_names))

        #Schrauben - How shal the sheet 'Schrauben' be treated?
        elif sheet == 'Schrauben':
            print('Now: Processing sheet \'{}\''.format(sheet))
            #Specific parameters
            unique_filters = ['Description','Bolt Diameter [mm]','Bolt Length [mm]']
            summing_parameter = 'Bolt Quantity'
            safety_margin = 1.2 #20% mehr
            parameters_for_output_list = ['Description','Material','DIN','Bolt Diameter [mm]','Bolt Length [mm]','Bolt Quantity_summed']

            #Read and clean Data
            df = read_excel_data(sheet)
            all_data = clean_excel_data(df).dropna(axis=1, how='all')
            
            #Processing Data
            print('Now: start accumulating...')
            order_data = find_unique_set(unique_filters,all_data,summing_parameter,safety_margin)
            print('Now: done accumulating...')

            #Save results
            save_excel_data(order_data[parameters_for_output_list])

        #Muttern - How shal the sheet 'Muttern' be treated?
        elif sheet == 'Muttern':
            print('Now: Processing sheet \'{}\''.format(sheet))
            #Specific parameters
            unique_filters = ['Description','Nuts Diameter [mm]']
            summing_parameter = 'Nuts Quantity'
            safety_margin = 1.2 #20% mehr
            parameters_for_output_list = ['Description','Nuts Diameter [mm]','Nuts Quantity_summed']

            #Read and clean Data
            df = read_excel_data(sheet)
            all_data = clean_excel_data(df).dropna(axis=1, how='all')
            
            #Processing Data
            print('Now: start accumulating...')
            order_data = find_unique_set(unique_filters,all_data,summing_parameter,safety_margin)
            print('Now: done accumulating...')

            #Save results
            save_excel_data(order_data[parameters_for_output_list])

        #Dichtungen - How shal the sheet 'Dichtungen' be treated?
        elif sheet == 'Dichtungen':
            print('Now: Processing sheet \'{}\''.format(sheet))
            #Specific parameters
            unique_filters = ['Description','NPD [in]']
            summing_parameter = ''
            safety_margin = 1.2 #20% mehr
            parameters_for_output_list = ['Description','NPD [in]','Material','item_count']

            #Read and clean Data
            df = read_excel_data(sheet)
            all_data = clean_excel_data(df).dropna(axis=1, how='all')
            
            #Processing Data
            print('Now: start accumulating...')
            order_data = find_unique_set(unique_filters,all_data,summing_parameter,safety_margin)
            print('Now: done accumulating...')

            #Save results
            save_excel_data(order_data[parameters_for_output_list])
        else:
            print('ERROR: no routine for processing sheet \'{}\' defined. Sheet was not processed...\n'.format(sheet))
            
print('Done!')
print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

if logging:
    #Close logfile
    sys.stdout = old_stdout
    log_file.close()
    print('Done!')

