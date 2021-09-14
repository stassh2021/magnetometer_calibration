# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 10:11:51 2021

@author: 6degt
# MagnDataViewer
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import pi as PI

ICM20948_UT_PER_LSB = 1.0  # DS MAGNETOMETER SPECIFICATIONS, header file

# magn_offset = np.array([-21.31, 27.13, -11.84])
# magn_offset = [-27.599, 39.675, -18.825]
# magn_offset = np.array([21.31, - 27.13, 11.84])

A_scaling = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
# A_scaling = np.array([[1.053, -0.082, -0.016], [-0.082, 1.072, -0.09], [-0.016, 0.009, 0.891]])
print(np.linalg.det(A_scaling))

# A(magn_data - m_offset)

coord_triple = ["x", "y", "z"]
accel_triple = ["a" + i for i in coord_triple]
gyro_triple = ["g" + i for i in coord_triple]
magn_triple = ["m" + i for i in coord_triple]
quat_quad = ['q0', 'q1', 'q2', 'q3']
def close_figs_run_rcparams():
    plt.close(fig='all')
    plt.rcParams['figure.figsize'] = (15, 15)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['font.size'] = 10
    
def add_magn_normed(df):
    mx = df["mx"].to_numpy()
    my = df["my"].to_numpy()
    mz = df["mz"].to_numpy()
    df["magn norm"] = np.sqrt(mx*mx+my*my+mz*mz)
    df['mx normed'] = df['mx']/df["magn norm"]
    df['my normed'] = df['my']/df["magn norm"]
    df['mz normed'] = df['mz']/df["magn norm"]
    
def add_accel_normed(df):
    ax = df["ax"].to_numpy()
    ay = df["ay"].to_numpy()
    az = df["az"].to_numpy()
    df['accel norm'] = np.sqrt(ax**2+ay**2+az**2)
    df['ax normed'] = df['ax']/df['accel norm']
    df['ay normed'] = df['ay']/df['accel norm']
    df['az normed'] = df['az']/df['accel norm']
    
def add_cos_ma(df):
    df['cos ma'] = ((df['mx normed'].to_numpy())*(df['ax normed'].to_numpy()) +
                           (df['my normed'].to_numpy())*(df['ay normed'].to_numpy()) +
                           (df['mz normed'].to_numpy())*(df['az normed'].to_numpy()))
#DATA:

path = r"data/user_desk/001_raw_data.csv"
path = r"data/user_desk/002_raw_data.csv"
path = r"data/user_desk/003_raw_data.csv"
path = r"data/user_desk/005_raw_data_rot90.csv"
# path = r'data/user_desk/debug_quat.csv'
# path = r'data/user_desk/debug_quat_mag_cal.csv'
path = r"data/user_desk/004_raw_data.csv"
path = r"data/user_desk/005_raw_data.csv"
path = r'data/user_desk/ater_mycal_test.csv'
path = r'data/user_desk/after_my_cal_90deg_rot.csv'
print(path)

df_uncalib = pd.read_csv(path)

# df_calib = pd.read_csv(path_calib)


""" Plan:
    [1] Radius
    [2] Fluctuations
    [3] Elipsoid
    [4] Projections """


# RADIUS:    
close_figs_run_rcparams()
add_magn_normed(df_uncalib)
# add_magn_norm(df_calib)
# channels =  ["magn norm"]  # + magn_triple 
# magn_norm_uncalib_arr = df_uncalib[channels].to_numpy()

# min_len = min(len(df_uncalib), len(df_calib))
# plt.plot(magn_norm_uncalib_arr[:min_len], color="blue", label = "uncalib")

# plt.legend()
# plt.title("MAGN NORM, " + path)
                      
# magn_norm_mean = np.mean(df["magn norm"].to_numpy())

# magn_norm_rel= df["magn norm"].to_numpy()/magn_norm_mean

# plt.figure()
# axes = plt.gca()
# axes.set_ylim([0.0,1.5])
# plt.plot(magn_norm_rel, label = 'magn norm fluctuations')
# plt.title(path)
# plt.legend()

xlim = 150
ylim = 150
zlim = 150    

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
mx = df_uncalib["mx"].to_numpy()*ICM20948_UT_PER_LSB 
my = df_uncalib["my"].to_numpy()*ICM20948_UT_PER_LSB 
mz = df_uncalib["mz"].to_numpy()*ICM20948_UT_PER_LSB
print("mx offset: ")
print((max(mx)+min(mx))/2.0)
print("my offset: ")
print((max(my)+min(my))/2.0) 
print("mz offset: ")
print((max(mz)+min(mz))/2.0)

# magn_offset = [(max(mx)+min(mx))/2.0, (max(my)+min(my))/2.0, (max(mz)+min(mz))/2.0 ]
# magn_offset = [-9.9, -9.75, -30.225 ]
# magn_offset = [0.0, 0.0, 0.0 ]

# mx_ = df_calib["mx"].to_numpy()
# my_ = df_calib["my"].to_numpy()
# mz_ = df_calib["mz"].to_numpy()

magn_data = df_uncalib[magn_triple].to_numpy()

# Axes manipulation:
# magn_data[:, 1]*=-1  
# magn_data[:, 2]*=-1  

# magn_data_tramsformed = np.dot((magn_data - magn_offset*10), A_scaling)*ICM20948_UT_PER_LSB 

# magn_data_tramsformed = np.dot((magn_data*ICM20948_UT_PER_LSB - magn_offset), A_scaling)

# mx_t = magn_data_tramsformed[:, 0]
# my_t = magn_data_tramsformed[:, 1]
# mz_t = magn_data_tramsformed[:, 2]

# df_uncalib['mx'] = mx_t
# df_uncalib['my'] = my_t
# df_uncalib['mz'] = mz_t

# ax.plot_trisurf (mx, my, mz)
ax.set_xlim([-xlim,+xlim])
ax.set_ylim([-ylim,+ylim])
ax.set_zlim([-zlim,+zlim])

ax.scatter(mx, my, mz, color = "blue", label="raw")
# ax.scatter(mx_, my_, mz_, color = "red", label = "calib")
# ax.scatter(mx_t, my_t, mz_t, color ='green', label="transformed")
plt.title(f"MAGN {path}")

plt.figure()
plt.scatter(mx, my, label = "Z plane projection, uncalib", color="blue")


# plt.scatter(mx_t, my_t, label = "Z plane projection, transformed",  color="green")
# plt.scatter(mx_, my_, label = "Z plane projection, calib", color="red")
plt.title(path)
plt.xlabel("mx")
plt.ylabel("my")
plt.xlim([-xlim,+xlim])
plt.ylim([-ylim,+ylim])
axes = plt.gca()
axes.set_aspect("equal")
plt.legend()

plt.figure()
plt.scatter(mx, mz, label = "Y plane projection, unclaib", color="blue")
# plt.scatter(mx_t, mz_t, label = "Y plane projection, transformed", color="green")
# plt.scatter(mx_, mz_, label = "Y plane projection, calib", color="red")
plt.title(path)
plt.xlabel("mx")
plt.ylabel("mz")
plt.xlim([-xlim,+xlim])
plt.ylim([-ylim,+ylim])
axes = plt.gca()
axes.set_aspect("equal")
plt.legend()

plt.figure()
plt.scatter(my, mz, label = "X plane projection, uncalib", color="blue")
# plt.scatter(my_t, mz_t, label = "X plane projection, transformed", color="green")
# plt.scatter(my_, mz_, label = "X plane projection, calib", color="red")
plt.title(path)
plt.xlabel("my")
plt.ylabel("mz")
plt.xlim([-xlim,+xlim])
plt.ylim([-ylim,+ylim])
axes = plt.gca()
axes.set_aspect("equal")
plt.legend()


fig = plt.figure()
axes = fig.add_subplot(projection='3d')
ax = df_uncalib["ax"].to_numpy()
ay = df_uncalib["ay"].to_numpy()
az = df_uncalib["az"].to_numpy()
axes.scatter(ax, ay, az, color="red", label="Uncalibrated")
plt.title("ACCEL")

# COS CHESK:
add_magn_normed(df_uncalib)
add_accel_normed(df_uncalib)
add_cos_ma(df_uncalib)

plt.figure()
df_uncalib['cos ma'].plot()
plt.legend()


cos_ma = df_uncalib['cos ma'].to_numpy()
plt.figure()
plt.plot(np.arccos(cos_ma)*(180/PI), label ='angle ma')
plt.legend()



df_uncalib[accel_triple].plot()
plt.legend()

df_uncalib[magn_triple].plot()
df_uncalib['magn norm'].plot()
plt.legend()


plt.figure()
df_uncalib[quat_quad].plot()
plt.legend()