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

ICM20948_UT_PER_LSB = 0.15  # DS MAGNETOMETER SPECIFICATIONS, header file, microTeslas per LSB

magn_offset = np.array([-21.31, 27.13, -11.84])
magn_offset = [-27.599, 39.675, -18.825]
# magn_offset = np.array([21.31, - 27.13, 11.84])

A_scaling = np.array([[1.053, -0.082, -0.016], [-0.082, 1.072, -0.09], [-0.016, 0.009, 0.891]])
print(np.linalg.det(A_scaling))

# A(magn_data - m_offset)

coord_triple = ["x", "y", "z"]
accel_triple = ["a" + i for i in coord_triple]
gyro_triple = ["g" + i for i in coord_triple]
magn_triple = ["m" + i for i in coord_triple]

def close_figs_run_rcparams():
    plt.close(fig='all')
    plt.rcParams['figure.figsize'] = (15, 15)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['font.size'] = 10
    
def add_magn_norm(df):
    mx = df["mx"].to_numpy()
    my = df["my"].to_numpy()
    mz = df["mz"].to_numpy()
    df["magn norm"] = np.sqrt(mx*mx+my*my+mz*mz)
# DATA:
#Calibrated and not calibrated magnetometers:

path = r"data/user_desk/Raw_Uncal_data.csv"
path_calib = r"data/user_desk/Calib_mG_RadsPerS_uT.csv"

df_uncalib = pd.read_csv(path)
df_calib = pd.read_csv(path_calib)


""" Plan:
    [1] Radius
    [2] Fluctuations
    [3] Elipsoid
    [4] Projections """


# RADIUS:    
close_figs_run_rcparams()
add_magn_norm(df_uncalib)
add_magn_norm(df_calib)
channels =  ["magn norm"]  # + magn_triple 
magn_norm_uncalib_arr = df_uncalib[channels].to_numpy()
magn_norm_calib_arr = df_calib[channels].to_numpy()

# PLOT RADIUS CONSERVATION:
min_len = min(len(df_uncalib), len(df_calib))
plt.plot(magn_norm_uncalib_arr[:min_len], color="blue", label = "uncalib")
plt.plot(magn_norm_calib_arr[:min_len], color = "red", label = "calib")
plt.legend()
plt.title("MAGN NORM, " + path)
plt.show()
                      
# magn_norm_mean = np.mean(df["magn norm"].to_numpy())
#
# magn_norm_rel= df["magn norm"].to_numpy()/magn_norm_mean
#
# plt.figure()
# axes = plt.gca()
# axes.set_ylim([0.0,1.5])
# plt.plot(magn_norm_rel, label = 'magn norm fluctuations')
# plt.title(path)
# plt.legend()
# #
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

mx_ = df_calib["mx"].to_numpy()
my_ = df_calib["my"].to_numpy()
mz_ = df_calib["mz"].to_numpy()

magn_data = df_uncalib[magn_triple].to_numpy()

# Axes manipulation:
# magn_data[:, 1]*=-1
# magn_data[:, 2]*=-1

# magn_data_tramsformed = np.dot((magn_data - magn_offset*10), A_scaling)*ICM20948_UT_PER_LSB

magn_data_tramsformed = np.dot((magn_data*ICM20948_UT_PER_LSB - magn_offset), A_scaling)

mx_t = magn_data_tramsformed[:, 0]
my_t = magn_data_tramsformed[:, 1]
mz_t = magn_data_tramsformed[:, 2]

# ax.plot_trisurf (mx, my, mz)
ax.set_xlim([-xlim,+xlim])
ax.set_ylim([-ylim,+ylim])
ax.set_zlim([-zlim,+zlim])

ax.scatter(mx, my, mz, color = "blue", label="raw")
ax.scatter(mx_, my_, mz_, color = "red", label = "calib")
ax.scatter(mx_t, my_t, mz_t, color ='green', label="transformed")
plt.title(f"MAGN {path}")
plt.legend()
plt.show()

# PLANE X-Y PROJECTIONS:
plt.figure()
plt.scatter(mx, my, label = "Z plane projection, uncalib", color="blue")
plt.scatter(mx_t, my_t, label = "Z plane projection, transformed",  color="green")
plt.scatter(mx_, my_, label = "Z plane projection, calib", color="red")
plt.title(path)
plt.xlabel("mx")
plt.ylabel("my")
plt.xlim([-xlim,+xlim])
plt.ylim([-ylim,+ylim])
axes = plt.gca()
axes.set_aspect("equal")
plt.legend()
plt.show()

# PLANE X-Z PROJECTIONS:
plt.figure()
plt.scatter(mx, mz, label = "Y plane projection, unclaib", color="blue")
plt.scatter(mx_t, mz_t, label = "Y plane projection, transformed", color="green")
plt.scatter(mx_, mz_, label = "Y plane projection, calib", color="red")
plt.title(path)
plt.xlabel("mx")
plt.ylabel("mz")
plt.xlim([-xlim,+xlim])
plt.ylim([-ylim,+ylim])
axes = plt.gca()
axes.set_aspect("equal")
plt.legend()
plt.show()

# PLANE Y-Z PROJECTIONS:
plt.figure()
plt.scatter(my, mz, label = "X plane projection, uncalib", color="blue")
plt.scatter(my_t, mz_t, label = "X plane projection, transformed", color="green")
plt.scatter(my_, mz_, label = "X plane projection, calib", color="red")
plt.title(path)
plt.xlabel("my")
plt.ylabel("mz")
plt.xlim([-xlim,+xlim])
plt.ylim([-ylim,+ylim])
axes = plt.gca()
axes.set_aspect("equal")
plt.legend()
plt.show()

# # ACCEL 3D PLOT:
# fig = plt.figure()
# axes = fig.add_subplot(projection='3d')
# ax = df_calib["ax"].to_numpy()
# ay = df_calib["ay"].to_numpy()
# az = df_calib["az"].to_numpy()
# axes.scatter(ax, ay, az, color="red", label="Uncalibrated")
# plt.title("ACCEL 3D PLOT")
# plt.show()

