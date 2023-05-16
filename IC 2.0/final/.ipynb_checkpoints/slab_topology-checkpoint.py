import numpy as np
import healpy as hp
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import multiprocessing as mp
from joblib import Parallel, delayed

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

def phi_of_k_cart(norms_and_vecs):

    phi_rand = []
    phi_k_dict = {}
    for norm in norms_and_vecs.keys():
        phi_rand = np.random.randn(8,len(norms_and_vecs[norm]))#we need 8 independent random vectors. See pdf for details
        phi_k_dict.update({norm:phi_rand})
    return phi_k_dict

def phi_of_x_cart(Lsize,x,y,z,norms_and_vecs,Phi_k_dict,alpha):
    Phi_x = 0.0 #Initial value of \Phi(\vec{x})
    prefactor = 0.0
    R = 1.0 #Radius of the CMB surface
    A = 1.0 #Amplitude of the Power Spectrum
    
    for norm in norms_and_vecs.keys():
        
        k = 2.0*math.pi*norm/Lsize/alpha#norm of Fourier vector
        sqrt_Pspec = math.sqrt(A*(k**(-3.0)))#Square-root of Harrison-Zeldovich Power-spectrum
        khat = np.transpose(norms_and_vecs[norm])# unit Fourier vectors
        
        cos_gamma1 = np.dot(np.array([x,y,z]),khat) 
        # dot of \hat{x} and \hat{k} in exp(ix.k) in the first octant        
        cos_gamma2 = np.dot(np.array([x,-y,z]),khat) 
        # dot of \hat{x} and \hat{k} in exp(ix.k) in the 2nd octant: y -> - y        
        cos_gamma3 = np.dot(np.array([-x,-y,z]),khat) 
        # dot of \hat{x} and \hat{k} in exp(ix.k) in the 3rd octant: x, y -> -x, -y        
        cos_gamma4 = np.dot(np.array([-x,y,z]),khat) 
        # dot of \hat{x} and \hat{k} in exp(ix.k) in the 4th octant: x -> -x 
        
        prefactor = 2*(np.cos(k*R*cos_gamma1)*Phi_k_dict[norm][0]-np.sin(k*R*cos_gamma1)*Phi_k_dict[norm][1] + \
                    np.cos(k*R*cos_gamma2)*Phi_k_dict[norm][2]-np.sin(k*R*cos_gamma2)*Phi_k_dict[norm][3] + \
                    np.cos(k*R*cos_gamma3)*Phi_k_dict[norm][4]-np.sin(k*R*cos_gamma3)*Phi_k_dict[norm][5] + \
                    np.cos(k*R*cos_gamma4)*Phi_k_dict[norm][6]-np.sin(k*R*cos_gamma4)*Phi_k_dict[norm][7])
        prefactor = np.sum(prefactor) #sum over all angles with fixed nnorm
        
        Phi_x += sqrt_Pspec*prefactor #sum over norms
    return Phi_x

def phi_map_cart_parallel(Nside,nmax,Lsize,alpha,seed):
    np.random.seed(seed) # fixes random seed, for debugging
    normvecs_dict = vector_n(nmax,alpha) #initialize norms and vectors
    randphi_dict = phi_of_k_cart(normvecs_dict) #initialize random values of \phi(\vec{k>)
    
    def phi_of_x_cart_wrapper(xyz):
        x, y, z = xyz
        return phi_of_x_cart(Lsize, x, y, z, normvecs_dict, randphi_dict, alpha)

    n_jobs = mp.cpu_count()
    phi_in_pixel = Parallel(n_jobs=n_jobs)(delayed(phi_of_x_cart_wrapper)(xyz) for xyz in np.transpose(hp.pix2vec(Nside,np.arange(hp.nside2npix(Nside)))))
    return np.array(phi_in_pixel)

def generate_map(Nside, nmax, Lsize, alpha, seed):
    return phi_map_cart_parallel(Nside,nmax,Lsize,alpha,seed)