# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 18:25:01 2016

@author: Thiago Pereira 
         tspereira@uel.br
         
"""

import math

#%%
def nandang(nmax,alpha):
    """
    This codes returns the set {k} and {\hat{k}}_k for the quasi-slab topology. The input
    parameters are:
    
    nmax: maximum of the sum over {k}
    alpha: ration between the Lx (or Ly) and the Lz directions
    
    The output is a dictionary containing k as keys and (\theta_k,\varphi_k) as values.

    Our code works for boxes of the form (Lx,Ly,Lz)=(alpha,alpha,1)Lz, where alpha is an integer
    and Lz is the width of the slab. A typical example would be (4,4,1)L. A perfect slab corresponds
    to (infinity,infinity,1)Lz.
    """
    
    
    a = vector_n(nmax,alpha)
    b = vectors_to_angles(a)
    
    return b

#%%
def norm_square(nmax,alpha):
    """
    This function returns all the norms n possible for a given cutoff nmax, where n is defined as follows.
    The Fourier vector \vec{k} for a 3-torus is
    $$
    \vec{k} = 2\pi(nx/Lx,ny/Ly,nz/Lz) = (2\pi/alpha/Lz)(nx,nx,alpha*nz)
    $$
    where we have used Lx=Ly=alpha*Lz. Thus we define 
    $$
    \vec{n} = (nx,ny,alpha*nz)
    $$
    The code bellow computes the norm of \vec{n}. From this list of norms one can directly obtain
    the list {k} by simply multiplying {n} by (2\pi/alpha/Lz)
    """

    norms2 = {}
    for i in range(nmax+1):
        for j in range(nmax+1):
            for k in range(1,nmax+1):#nz always greater than zero
                n2 = (i**2+j**2+(alpha*k)**2)
                if not(n2 in norms2.keys()):
                    norms2.update({n2:[]})
    return norms2

#%%
def vector_n(nmax,alpha):
    """
    This function returns a dictionary containing n (as compute above) as keys and (nx,ny,alpha*nz)
    as values.
    """
    vec_n = {}
    for norm in norm_square(nmax,alpha).keys(): 
        vec_n[math.sqrt(norm)] = []
        nz_count = int(math.floor(math.sqrt(norm)))
        for nz in range(1,nz_count+1): #we do not include components at and bellow the nz=0 plane
            nx2_plus_ny2 = norm - nz**2
            nx2_ny2_count = int(math.floor(math.sqrt(nx2_plus_ny2)))
            for ny in range(nx2_ny2_count+1):
                nx = int(math.sqrt(norm - nz**2 - ny**2))
                if nz%alpha==0 and nx**2 + ny**2 + nz**2 == norm:
                    vec_n[math.sqrt(norm)].append([nx,ny,nz])
    return vec_n

#%%
def vectors_to_angles(n_dict):
    """
    This functions receives a dictionary containing n as keys and (nx,ny,alpha*nz) as values and
    returns another dictionary with n as keys and (\theta_k,\varphi_k) as values. The keys will
    be latter multiplied by (2\pi/alpha/Lz) to be transformed in the Fourier norms k.
    """     
    #   partial_time = time.time()
    new_n = dict()
    for k in n_dict.keys():
        angles = []
        for vector in n_dict[k]:
            # calculate the azimuthal angle
            if vector[0] != 0:
                phi = math.atan(float(vector[1])/float(vector[0]))
            else:
                phi = math.pi/2.0  # tan^-1(inf) = pi/2
                if vector[1] == 0:  # tan^-1(0/0) = 0.0
                    phi = 0.0
            # calculate the polar angle
            if vector[2] != 0:
                # sqrt returns float, float/int = float
                theta = math.atan((math.sqrt(vector[0]**2 + vector[1]**2))/vector[2])
            else:
                theta = math.pi/2.0  # tan^-1(inf) = pi/2
            angles.append([theta, phi])
        new_n.update({k: angles})
#    print('vectors_to_angles: OK in {time} s'.format(time = time.time() - partial_time))
    return new_n
