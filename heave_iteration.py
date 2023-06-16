
import numpy as np
from Point3S import *
from Point2SHP import *
from unit_vector import *

def heave_iterate(droop, bump, iterations, FSUS, RSUS, ZBAR, ZBARDIM):
    bumpi = np.array((bump-droop)/iterations)
    heaverange = np.arange(droop, bump+bumpi, bumpi)
    
    F_PI_vec_S = FSUS[8, 0::2] - ZBAR[0, 0::2]
    R_PI_vec_S = RSUS[8, 0::2] - ZBAR[1, 0::2]
    ZBAR_angle_S = angle_between(F_PI_vec_S, R_PI_vec_S)
    
    THETA = np.array([])
    
    FSUB = np.array(FSUS)
    RSUB = np.array(RSUS)
    
    FSUB[2, :] = Point2SHP(1, FSUS[0, :], FSUS[1, :], FSUS[2, :], FSUS[2, 2]+droop-0*bumpi)    
    FSUB[5, :] = Point3S(1, FSUS[3, :], FSUS[3, :], FSUS[4, :], FSUS[4, :], FSUS[2, :], FSUB[2, :], FSUS[5, :])    
    FSUB[7, :] = Point3S(1, FSUS[6, :], FSUS[6, :], FSUS[5, :], FSUB[5, :], FSUS[2, :], FSUB[2, :], FSUS[7, :])
    FSUB[9, :] = Point3S(1, FSUS[3, :], FSUS[3, :], FSUS[4, :], FSUB[4, :], FSUS[5, :], FSUB[5, :], FSUS[9, :])
    FSUB[8, :] = Point3S(1, FSUS[9, :], FSUB[9, :], ZBAR[0, :], ZBAR[0, :], ZBAR[1, :], ZBAR[1, :], FSUS[8, :])
    
    #print(FSUB)
    
    RSUB[2, :] = Point2SHP(1, RSUS[0, :], RSUS[1, :], RSUS[2, :], RSUS[2, 2]+droop-0*bumpi)    
    RSUB[5, :] = Point3S(1, RSUS[3, :], RSUS[3, :], RSUS[4, :], RSUS[4, :], RSUS[2, :], RSUB[2, :], RSUS[5, :])    
    RSUB[7, :] = Point3S(1, RSUS[6, :], RSUS[6, :], RSUS[5, :], RSUB[5, :], RSUS[2, :], RSUB[2, :], RSUS[7, :])
    RSUB[9, :] = Point3S(1, RSUS[3, :], RSUS[3, :], RSUS[4, :], RSUB[4, :], RSUS[5, :], RSUB[5, :], RSUS[9, :])
    RSUB[8, :] = Point3S(1, RSUS[9, :], RSUB[9, :], ZBAR[0, :], ZBAR[0, :], ZBAR[1, :], ZBAR[1, :], RSUS[8, :])
    
    #print(RSUB)
    
    FSUS = FSUB
    RSUS = RSUB
    #print(FSUS)
    
    G = ZBARDIM[0]
    J = ZBARDIM[1]**4-ZBARDIM[2]**4
    L = ZBARDIM[3]
    
    
    # LCA Fore(0) Aft(1) Outer(2)
    # UCA Fore(3) Aft(4) Outer(5)
    # Tie Rod Inner(6) Outer(7) 
    # Pullrod Inner(8) Outer(9)
    
    arr_Fphi = []
    arr_Rphi = []
    
    for index in heaverange:
        FSUB[2, :] = Point2SHP(1, FSUS[0, :], FSUS[1, :], FSUS[2, :], FSUS[2, 2]+bumpi)    
        FSUB[5, :] = Point3S(1, FSUS[3, :], FSUS[3, :], FSUS[4, :], FSUS[4, :], FSUS[2, :], FSUB[2, :], FSUS[5, :])    
        FSUB[7, :] = Point3S(1, FSUS[6, :], FSUS[6, :], FSUS[5, :], FSUB[5, :], FSUS[2, :], FSUB[2, :], FSUS[7, :])
        FSUB[9, :] = Point3S(1, FSUS[3, :], FSUS[3, :], FSUS[4, :], FSUB[4, :], FSUS[5, :], FSUB[5, :], FSUS[9, :])
        FSUB[8, :] = Point3S(1, FSUS[9, :], FSUB[9, :], ZBAR[0, :], ZBAR[0, :], ZBAR[1, :], ZBAR[1, :], FSUS[8, :])
        
        RSUB[2, :] = Point2SHP(1, RSUS[0, :], RSUS[1, :], RSUS[2, :], RSUS[2, 2]+bumpi)    
        RSUB[5, :] = Point3S(1, RSUS[3, :], RSUS[3, :], RSUS[4, :], RSUS[4, :], RSUS[2, :], RSUB[2, :], RSUS[5, :])    
        RSUB[7, :] = Point3S(1, RSUS[6, :], RSUS[6, :], RSUS[5, :], RSUB[5, :], RSUS[2, :], RSUB[2, :], RSUS[7, :])
        RSUB[9, :] = Point3S(1, RSUS[3, :], RSUS[3, :], RSUS[4, :], RSUB[4, :], RSUS[5, :], RSUB[5, :], RSUS[9, :])
        RSUB[8, :] = Point3S(2, RSUS[9, :], RSUB[9, :], ZBAR[2, :], ZBAR[2, :], ZBAR[3, :], ZBAR[3, :], RSUS[8, :])

        F_PI_vec_B = FSUB[8, 0::2] - ZBAR[0, 0::2]
        R_PI_vec_B = RSUB[8, 0::2] - ZBAR[1, 0::2]
        ZBAR_angle_B = angle_between(F_PI_vec_B, R_PI_vec_B)
        
        THETA = np.append(THETA, ZBAR_angle_S-ZBAR_angle_B) 
        
        radF = np.array([F_PI_vec_B[0], 0, F_PI_vec_B[1]])
        radR = np.array([R_PI_vec_B[0], 0, R_PI_vec_B[1]])
        F_PULL_vec_B = FSUB[9,:] - FSUB[8, :]
        R_PULL_vec_B = RSUB[9,:] - RSUB[8, :]
        
        Fphi = angle_between(radF, -F_PULL_vec_B)
        Rphi = angle_between(radR, -R_PULL_vec_B)
        arr_Fphi = np.append(arr_Fphi, Fphi)
        arr_Rphi = np.append(arr_Rphi, Rphi)
        
        #print(index, FSUB[8, :], RSUB[8, :])
        #print(index, ZBAR_angle_B)
        
        FSUS = np.array(FSUB)
        RSUS = np.array(RSUB)

        # Calculate wheel forces and add for axle force
        
    return np.stack((heaverange, arr_Fphi*57.3, arr_Rphi*57.3), axis=1)
    #return True