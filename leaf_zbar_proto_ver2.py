
import os
os.system('cls')
print("---------------------------------------\nZ-Bar Prototype Program (ver 2) Results:\n----------------------------------------")

import numpy as np
np.set_printoptions(precision=2, sign='+', suppress=True, floatmode='fixed')

from Point3S import *
from Point2SHP import *
from unit_vector import *
from heave_iteration import *

FSUS = np.array([
                [148,120,128], [148,-120,135], [515,22,110], # LCA Fore(0) Aft(1) Outer(2)
                [148,120,247], [148,-120,244], [489,10,290], # UCA Fore(3) Aft(4) Outer(5)
                [135,-80,188], [474,-80,200],                # Tie Rod Inner(6) Outer(7) 
                [147,0,96], [370,0,260]                      # Pullrod Inner(8) Outer(9)
                ], dtype='float')



RSUS = np.array([
                [148,-1380,128], [148,-1620,135], [515,-1478,110], 
                [148,-1380,247], [148,-1620,244], [489,-1490,290], 
                [135,-1580,188], [474,-1580,200],                  
                [110,-1500,180], [340,-1500,260]                    
                ], dtype='float')

coord_zbar_x = 120 #mm
coord_zbar_z = 140 #mm

ZBAR = np.array([
                [coord_zbar_x, 100, coord_zbar_z],
                [coord_zbar_x, -100, coord_zbar_z],
                [coord_zbar_x, -1400, coord_zbar_z],
                [coord_zbar_x, -1600, coord_zbar_z],
                ], dtype='float')

ZBARDIM = np.array([
                   202240/(2*(1+.28)), #G - MPa
                   25, #D - mm
                   24, #d - mm
                   -RSUS[8,1] - FSUS[8,1], #L - mm
                   np.linalg.norm(ZBAR[0, 0::2] - FSUS[8, 0::2]), #RF - mm
                   np.linalg.norm(ZBAR[1, 0::2] - RSUS[8, 0::2]), #RR - mm
                   ], dtype='float')

# Calculate static zbar theta 


#print(F_PI_vec_S)
#print(R_PI_vec_S)
#print(ZBAR_angle_S*57.3)

#print(ZBARDIM)

print(heave_iterate(-25, 25, 20, FSUS, RSUS, ZBAR, ZBARDIM))

#print(FSUS[0, 0::2]) #2D-ification
#print(RSUS)
