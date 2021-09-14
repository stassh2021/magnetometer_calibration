# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 17:34:02 2021

@author: 6degt
"""
import numpy as np
import pandas as pd

from scipy import linalg

magn_triple = ['mx', 'my', 'mz']
A_scaling = np.array([[1.053, -0.082, -0.016], [-0.082, 1.072, -0.09], [-0.016, 0.009, 0.891]])
magn_offset = np.array([[-21.31, 27.13, -11.84]]).T
magn_strength = 22.01

def calc_meas_row(magn_row):
    mx, my, mz = magn_row[0]*0.15, magn_row[1]*0.15,  magn_row[2]*0.15
    basic_magn_vector = np.array([mx**2, 2*mx*my, 2*mx*mz, my**2, 2*my*mz, mz**2, mx, my, mz , 1.0])
    return basic_magn_vector


def quad_form(V, A):
    B = np.dot(A,V)
    return np.dot(V.T, B)

def compose_beta(A, V, B):
    beta = np.zeros(10)
    beta[0] = A[0,0]
    beta[1] = A[0,1]
    beta[2] = A[0,2]
    
    beta[3] = A[1,0]
    beta[4] = A[1,1]
    beta[5] = A[1,2]

    beta6_9 = -2*np.dot(A,V)

    beta[6] = beta6_9[0]
    beta[7] = beta6_9[1]
    beta[8] = beta6_9[2]
    
    beta[9] = quad_form(V,A) - magn_strength*magn_strength
    
    return beta
#DATA:


path = r"data/user_desk/Raw_Uncal_data.csv"
df = pd.read_csv(path)
magn_data = df[magn_triple].to_numpy()


X_li = []

for magn_row in magn_data[:2960]:
    basic_magn_vector = calc_meas_row(magn_row) 
    X_li.append(basic_magn_vector)
    
X = np.vstack(X_li)

data_matrix = np.dot(X.T, X)
eigvals, eigvecs = linalg.eig(data_matrix)

print(np.shape(data_matrix))


for val, vec in zip(eigvals, eigvecs):
    print(val)
    print(linalg.norm(val))
    print(vec)
    print(linalg.norm(vec))
    
print("Beta: ")    
beta = eigvecs[-1] 
A = np.diag([beta[0], beta[3], beta[5]])
A[0,1], A[0,2] = beta[1], beta[2]
A[1,2] = beta[4]

A[1,0] = A[0,1]
A[2,0] = A[0,2]
A[2,1] = A[1,2]

print(A)
s = pow(linalg.det(A), 1/3)
print(1/s)
print(linalg.det((1/s)*A))

print(1/s*A)

print("BETA SCALED:")
print(1/s*beta)

print(np.dot(data_matrix, beta))

print("EIGENE?: ")
for comp1, comp2 in zip(beta,np.dot(beta, data_matrix)):
    print(comp1/comp2)
    
beta_mag_cal = compose_beta(A_scaling,magn_offset, magn_strength)

print(beta_mag_cal)
X_beta = np.dot(data_matrix,beta_mag_cal)

for el1, el2 in zip(beta, X_beta):
    print(el1/el2)