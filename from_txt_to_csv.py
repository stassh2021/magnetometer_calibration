# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:37:17 2020

@author: 6degt

(1) convert txt to standard df, save as csv
(2) plot the df
"""
import numpy as np
import pandas as pd


imu_titles_9dof = ['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz']
data_columns = ['t', 'ax', 'ay', 'az', 'gx', 'gy', 'gz',
                'mx', 'my', 'mz', 'w', 'nx', 'ny', 'nz']

data_columns = ['ax', 'ay', 'az', 'gx', 'gy', 'gz',
                'mx', 'my', 'mz']

# data_columns1 = ['gx', 'gy', 'gz', 'ax', 'ay', 'az',
                # 'mx', 'my', 'mz']



def fill_row_from_line(txt_file_line):
    ''' DATA structure assumption:
        lines of nums:
            Start Setup...

        ax, ay, az, gx, gy, gz, mx, my, mz'''
    row = []
    list_by_space = txt_file_line.split(',')
    
    for el in list_by_space: 
        el = el.strip()
        try:
            row.append(float(el))
        except ValueError:
            print(f'tried to convert string to float: {repr(el)}')
   
    return row


def fill_row_from_line(txt_file_line):
    ''' DATA structure assumption:
     
      (1) ax, ay, az, gx, gy, gz, mx, my, mz
      (2) Raw: ax, ay, az, gx, gy, gz, mx, my, mz'''
    
    txt_file_line = txt_file_line.replace("Raw:", "").strip()
    # print(txt_file_line)
    row = []
    try: 
        txt_file_line = txt_file_line.split("->")[1]
    except IndexError:
        pass
    list_by_space = txt_file_line.split(',')
    
    for el in list_by_space: 
        el = el.strip()
        try:
            row.append(float(el))
        except ValueError:
            print(f'tried to convert string to float: {repr(el)}')
   
    return row

def create_list_of_arrays(lines):

    data_li = []
    num_lines = 0
    for line in lines:
        list_by_space =line.split(',')
        if len(list_by_space)==9:
            num_lines += 1
            row = fill_row_from_line(line)
            data_li.append(row)
    print(f'number of lines proceeded: {num_lines}')
    return data_li



# DEFINE DATA:

txt_file_name = "Calib_mG_RadsPerS_uT.txt"
# txt_file_name = "Raw_Uncal_data.txt"
txt_file_path = r'data' + '/' + txt_file_name

txt_file_name = "Calib_mG_RadsPerS_uT.txt"
# txt_file_name = "Raw_Uncal_data.txt"
txt_file_name = "001_raw_data.txt"
txt_file_name = "002_raw_data.txt"
txt_file_name = "003_raw_data.txt"
txt_file_name = "004_raw_data.txt"
txt_file_name = "005_raw_data_rot90.txt"
txt_file_name = "005_raw_data.txt"
txt_file_name = 'ater_mycal_test.txt'
# txt_file_path = r'data/user_desk_almog/' + txt_file_name
txt_file_path = r'data/user_desk/' + txt_file_name


with open(txt_file_path, 'r') as f:
    lines = f.readlines()
    f.close()
data_li = create_list_of_arrays(lines)

data_arr = np.vstack(data_li)

df = pd.DataFrame(data_arr, columns = data_columns)

file_b_name = txt_file_name.split('.')[0]
csv_file_path = r'data/user_desk' + '/' + file_b_name + '.csv'
df.to_csv(csv_file_path, index=False)


print(f"Data columns: {data_columns}")
print(f'CSV file saved to {csv_file_path}')