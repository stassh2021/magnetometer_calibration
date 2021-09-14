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

data_columns = ['ax', 'ay', 'az', 'gx', 'gy', 'gz',
                'mx', 'my', 'mz', 'q0', 'q1', 'q2', 'q3' ]
data_columns = ['gx', 'gy', 'gz', 'ax', 'ay', 'az',
                'mx', 'my', 'mz', 'q0', 'q1', 'q2', 'q3' ]

# data_columns1 = ['gx', 'gy', 'gz', 'ax', 'ay', 'az',
                # 'mx', 'my', 'mz']


def fill_row_from(line, ind_start, ind_end, row_arr):
    ''' DATA structure assumption:
         Accel: [-0.298,0.083,1.002]
        Mag: [-20.550,-9.750,-45.600]
        Gyro: [-0.788,-0.290,-0.578]
        '''
    after_bracket = line.split('[')[1]
    before_bracket = after_bracket.split(']')[0]
    triple = before_bracket
    val_x, val_y, val_z = triple.split(',')
    val_x, val_y, val_z = float(val_x), float(val_y), float(val_z)
    print(val_x, val_y, val_z)
    row_arr[:, ind_start: ind_end] = val_x, val_y, val_z
    return row_arr


def fill_row_from_line(txt_file_line):
    ''' DATA structure assumption:
        lines of nums:
            Start Setup...

        988.00 520.00 -8352.00 0.31 -0.08 0.22 -295.00 32.00 -9.00
        996.00 524.00 -8496.00 -0.35 0.48 -0.30 -295.00 24.00 -2.00
        964.00 476.00 -8296.00 -0.02 0.54 0.39 -309.00 23.00 -1.00'''

    for line in txt_file_lines:
        row = []
        list_by_space = line.split(' ')
        for el in list_by_space:
            try:
                row.append(float(el))
            except ValueError:
                print('tried to convert float to string')


# def fill_row_from_line2(txt_file_line):
#     ''' DATA structure assumption:
#         lines of nums:
#             Start Setup...

#         t, ax, ay, az, gx, gy, gz, mx, my, mz, w, nx, ny, nz'''
#     row = []
#     list_by_space = txt_file_line.split(',')
#     for el in list_by_space:
#         try:
#             row.append(float(el))
#         except ValueError:
#             print(f'tried to convert string to float: {repr(el)}')
#     return row


def fill_row_from_list(list_by_comma): 
    row = []
    
    for el in list_by_comma: 
        el = el.strip()
        try:
            row.append(float(el))
        except ValueError:
            print(f'tried to convert string to float: {repr(el)}')
   
    return row

def create_list_of_arrays(lines):
    ''' DATA (txt_line) structure assumption:
        G:0.014,0.615,0.064|A:8.407,-2.376,3.593|M:-18.750,-1.050,58.350|Q:-0.815,0.073,0.555,-0.137; '''

    data_li = []
    num_lines = 0
    for line in lines:
        try:
            line = line.split("->")[1]
        except IndexError:
            pass
        line = line.strip().replace("G:","")
        line = line.replace("|A:", ",")
        line = line.replace("|M:", ",")
        line = line.replace("|Q:", ",")
        line = line.replace(";", "")
        list_by_comma = line.split(',')
        if len(list_by_comma)==len(data_columns):
            num_lines += 1
            row = fill_row_from_list(list_by_comma)
            data_li.append(row)
    print(f'number of lines proceeded: {num_lines}')
    return data_li



# DEFINE DATA:
# txt_file_name = 'raw_data_100Hz_IdleHand.txt'
# txt_file_name = 'raw_data_100Hz_table.txt'
# txt_file_name = 'raw_data_100Hz_UpDown10reps.txt'
# txt_file_name = 'output_desk.txt'
# txt_file_name = 'mouse_output_90y.txt'
# txt_file_name = 'mouse_output_test2.txt'
# txt_file_name = 'mouse_test2d90.txt'
txt_file_name = 'mouse_output_9degpersec10sec.txt'
txt_file_name = 'mouse_noise.txt'
txt_file_name = 'mouse_noise1.txt'
txt_file_name = '21SECNoise.txt'
txt_file_name = '30SEC_noise.txt'
txt_file_name = 'mouse_90degrees.txt'
txt_file_name = 'mouse_saturation.txt'
txt_file_name ='10_twists_80_hz_raw_data_almog.txt'
txt_file_name = "z_down_x_up_y_up.txt.txt"
txt_file_name = "magneto_check.txt"
txt_file_name = 'ater_mycal_test.txt'
# txt_file_name ="magn_red_test_15_06_2021.txt"
txt_file_name = 'after_my_cal_90deg_rot.txt'
# txt_file_path = r'data' + '/' + txt_file_name
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

print(f'CSV file saved to {csv_file_path}')