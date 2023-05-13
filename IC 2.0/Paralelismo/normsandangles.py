# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 18:25:01 2016

@author: Thiago Pereira 
         tspereira@uel.br
         
"""

import math

def nandang(nmax,alpha):
    
    a = vector_n(nmax,alpha)
    b = vectors_to_angles(a)
    
    return b

def nandvecs(nmax,alpha):
    a = vector_n(nmax,alpha)
    
    return a

def norm_square(nmax,alpha):

    norms2 = {}
    for i in range(nmax+1):
        for j in range(nmax+1):
            for k in range(1,nmax+1):#nz always greater than zero
                n2 = (i**2+j**2+(alpha*k)**2)
                if not(n2 in norms2.keys()):
                    norms2.update({n2:[]})
    return norms2

def vector_n(nmax,alpha):
    vec_n = {}
    for norm in norm_square(nmax,alpha).keys(): 
        vec_n[math.sqrt(norm)] = []
        nz_count = int(math.floor(math.sqrt(norm)))
        for nz in range(1,nz_count+1): #we do not include components at and bellow the nz=0 plane
            nx2_plus_ny2 = norm - nz**2 #the case nz=0 should be handled separetely
            nx2_ny2_count = int(math.floor(math.sqrt(nx2_plus_ny2)))
            for ny in range(nx2_ny2_count+1):
                nx = int(math.sqrt(norm - nz**2 - ny**2))
                if nz%alpha==0 and nx**2 + ny**2 + nz**2 == norm:
                    vec_n[math.sqrt(norm)].append([nx/math.sqrt(norm),ny/math.sqrt(norm),nz/math.sqrt(norm)])
    return vec_n

def vectors_to_angles(n_dict):
    new_n = dict()
    for k in n_dict.keys():
        angles = []
        for vector in n_dict[k]:
            if vector[0] != 0:
                phi = math.atan(float(vector[1])/float(vector[0]))
            else:
                phi = math.pi/2.0  
                if vector[1] == 0:  
                    phi = 0.0
            if vector[2] != 0:
                theta = math.atan((math.sqrt(vector[0]**2 + vector[1]**2))/vector[2])
            else:
                theta = math.pi/2.0  # tan^-1(inf) = pi/2
            angles.append([theta, phi])
        new_n.update({k: angles})
    return new_n
