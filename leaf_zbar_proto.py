
import os
import time
time1 = time.time()
os.system('cls')
print("Z-Bar Prototype Program Results:\n")


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

np.set_printoptions(precision=2, sign='+', suppress=True)

from Point3S import *
from Point2SHP import *

#
# Input Options
#

testoption = 1 # Roll, Pitch, Heave
accX_g = 1.5 #G Lateral 
accY_g = 1 #G Longitudinal
heave_g = 1 #G Bump


np.set_printoptions(precision=2, sign='+')

#
# Car Dimensions
#

frontperc = 46/100 #percent
track = 1194 #mm (t)
wheelbase = 1536 #mm (l)
CGlocA = (1-frontperc)*wheelbase #mm (a)
CGlocB = frontperc*wheelbase #mm (b)
CGheight = 300 #mm (h)
# Assumption - Assumes constants for each of these figures

CG = np.array([0, CGlocA, CGheight])
#print('CG:', CG)

bump = +25
droop = -25
iterations = 20
bumpi = np.array((bump-droop)/iterations)
heaverange = np.arange(droop, bump, bumpi)
#print(heaverange)


carw_total = 500 #lbs
carw_faxle = carw_total*frontperc
carw_raxle = carw_total*(1-frontperc)
# Assumption - Car weight L/R is 50/50

carw_fl = carw_faxle/2
carw_fr = carw_faxle/2
carw_rl = carw_raxle/2
carw_rr = carw_raxle/2

W_mat = np.array([carw_fl, carw_fr, carw_rl, carw_rr, carw_total])

#print('W_mat:', W_mat)

if testoption == 1: # Roll, assumes given RC
    #accX_g = float(input('Input lateral Gs (pos = left turn): '))
    deltaW_F = CGheight*carw_faxle*accX_g/track
    deltaW_R = CGheight*carw_raxle*accX_g/track
    deltaW_mat = np.array([-deltaW_F, deltaW_F, -deltaW_R, deltaW_R, 0])
    W_mat = W_mat + deltaW_mat
#    print('W_mat(roll):', W_mat)
    isrolling = True
    ispitching = False
    plt.title("Force vs. Displacement for Roll")
    
if testoption == 2:
    #accY_g = float(input('Input longitudinal Gs (pos = accel): '))
    deltaW = CGheight*carw_total*accY_g/(wheelbase*2)
    deltaW_mat = np.array([-deltaW, -deltaW, deltaW, deltaW, 0])
    W_mat = W_mat + deltaW_mat
#    print('W_mat(pitch):', W_mat)
    isrolling = False
    ispitching = True
    plt.title("Force vs. Displacement for Pitch")
    
if testoption == 3:
    #heave_g = float(input('Input bump Gs: '))
    W_mat = W_mat*(heave_g+1)
#    print('W_mat(heave):', W_mat)
    isrolling = True
    ispitching = True
    plt.title("Force vs. Displacement for Heave")
    
#
# Suspension Dimensions (mm)
#

pt_F_LF_static = np.array([148,120,128])
pt_F_LA_static = np.array([148,-120,135])
pt_F_LO_static = np.array([515,22,110])

pt_F_UF_static = np.array([148,120,247])
pt_F_UA_static = np.array([148,-120,244])
pt_F_UO_static = np.array([489,10,290])

pt_F_TO_static = np.array([474,-80,200])
pt_F_TI_static = np.array([135,-80,188])

pt_F_PO_static = np.array([370,0,260])
pt_F_PI_static = np.array([147,0,96])
pt_F_PI_OG = pt_F_PI_static

pt_R_LF_static = np.array([148,-1380,128])
pt_R_LA_static = np.array([148,-1620,135])
pt_R_LO_static = np.array([515,-1478,110])

pt_R_UF_static = np.array([148,-1380,247])
pt_R_UA_static = np.array([148,-1620,244])
pt_R_UO_static = np.array([489,-1490,290])

pt_R_TO_static = np.array([474,-1580,200])
pt_R_TI_static = np.array([135,-1580,188])

pt_R_PO_static = np.array([340,-1500,260])
pt_R_PI_static = np.array([135,-1500,95])
pt_R_PI_OG = pt_R_PI_static

# Assumption - Longitudinal Z-Bar
coord_zbar_x = 120 #mm
coord_zbar_z = 140 #mm
pt_F_ZF_static = [coord_zbar_x, 100, coord_zbar_z]
pt_F_ZA_static = [coord_zbar_x, -100, coord_zbar_z]

pt_R_ZF_static = [coord_zbar_x, 1400, coord_zbar_z]
pt_R_ZA_static = [coord_zbar_x, -1600, coord_zbar_z]

arr_F_zbar_MR = np.array([])
arr_F_deflection_full = np.array([])
arr_R_zbar_MR = np.array([])
arr_R_deflection_full = np.array([])

#
# Heave Position Calculations
#

if droop != 0:

    pt_F_LO_bump = Point2SHP(1, pt_F_LF_static, pt_F_LA_static, pt_F_LO_static, pt_F_LO_static[2]+droop)
    pt_F_UO_bump = Point3S(1, pt_F_UF_static, pt_F_UF_static, pt_F_UA_static, pt_F_UA_static, pt_F_LO_static, pt_F_LO_bump, pt_F_UO_static)
    pt_F_TO_bump = Point3S(1, pt_F_TI_static, pt_F_TI_static, pt_F_UO_static, pt_F_UO_bump, pt_F_LO_static, pt_F_LO_bump, pt_F_TO_static)
    pt_F_PO_bump = Point3S(1, pt_F_UF_static, pt_F_UF_static, pt_F_UA_static, pt_F_UA_static, pt_F_UO_static, pt_F_UO_bump, pt_F_PO_static)
    pt_F_PI_bump = Point3S(1, pt_F_PO_static, pt_F_PO_bump, pt_F_ZA_static, pt_F_ZA_static, pt_F_ZF_static, pt_F_ZF_static, pt_F_PI_static)
    
    pt_R_LO_bump = Point2SHP(1, pt_R_LF_static, pt_R_LA_static, pt_R_LO_static, pt_R_LO_static[2]+droop)
    pt_R_UO_bump = Point3S(1, pt_R_UF_static, pt_R_UF_static, pt_R_UA_static, pt_R_UA_static, pt_R_LO_static, pt_R_LO_bump, pt_R_UO_static)
    pt_R_TO_bump = Point3S(1, pt_R_TI_static, pt_R_TI_static, pt_R_UO_static, pt_R_UO_bump, pt_R_LO_static, pt_R_LO_bump, pt_R_TO_static)
    pt_R_PO_bump = Point3S(1, pt_R_UF_static, pt_R_UF_static, pt_R_UA_static, pt_R_UA_static, pt_R_UO_static, pt_R_UO_bump, pt_R_PO_static)
    pt_R_PI_bump = Point3S(1, pt_R_PO_static, pt_R_PO_bump, pt_R_ZA_static, pt_R_ZA_static, pt_R_ZF_static, pt_R_ZF_static, pt_R_PI_static)
    #zbar_MR = [zbar_MR, deflection/bumpi]
    
    pt_F_LO_static = pt_F_LO_bump
    pt_F_UO_static = pt_F_UO_bump
    pt_F_TO_static = pt_F_TO_bump
    pt_F_PO_static = pt_F_PO_bump
    pt_F_PI_static = pt_F_PI_bump
    
    pt_R_LO_static = pt_R_LO_bump
    pt_R_UO_static = pt_R_UO_bump
    pt_R_TO_static = pt_R_TO_bump
    pt_R_PO_static = pt_R_PO_bump
    pt_R_PI_static = pt_R_PI_bump
    
    print(pt_F_LO_bump)
    #print(pt_F_UO_bump)
    #print(pt_F_TO_bump)
    #print(pt_F_PO_bump)
    #print(pt_F_PI_bump)
    
print("-----------------------------------------")

for index in heaverange:
    #print('a')
    pt_F_LO_bump = Point2SHP(1, 
                             pt_F_LF_static, 
                             pt_F_LA_static, 
                             pt_F_LO_static, 
                             pt_F_LO_static[2]+bumpi) # +bumpi
    pt_F_UO_bump = Point3S(1, 
                           pt_F_UF_static, 
                           pt_F_UF_static, 
                           pt_F_UA_static, 
                           pt_F_UA_static, 
                           pt_F_LO_static, 
                           pt_F_LO_bump, 
                           pt_F_UO_static)
    pt_F_TO_bump = Point3S(1, 
                           pt_F_TI_static, 
                           pt_F_TI_static, 
                           pt_F_UO_static, 
                           pt_F_UO_bump, 
                           pt_F_LO_static, 
                           pt_F_LO_bump, 
                           pt_F_TO_static)
    pt_F_PO_bump = Point3S(1, 
                           pt_F_UF_static, 
                           pt_F_UF_static, 
                           pt_F_UA_static, 
                           pt_F_UA_static, 
                           pt_F_UO_static, 
                           pt_F_UO_bump, 
                           pt_F_PO_static)
    pt_F_PI_bump = Point3S(1, 
                           pt_F_PO_static, 
                           pt_F_PO_bump, 
                           pt_F_ZA_static, 
                           pt_F_ZA_static, 
                           pt_F_ZF_static, 
                           pt_F_ZF_static, 
                           pt_F_PI_static)
    
    pt_R_LO_bump = Point2SHP(1, 
                             pt_R_LF_static, 
                             pt_R_LA_static, 
                             pt_R_LO_static, 
                             pt_R_LO_static[2]+bumpi) # +bumpi
    pt_R_UO_bump = Point3S(1, 
                           pt_R_UF_static, 
                           pt_R_UF_static, 
                           pt_R_UA_static, 
                           pt_R_UA_static, 
                           pt_R_LO_static, 
                           pt_R_LO_bump, 
                           pt_R_UO_static)
    pt_R_TO_bump = Point3S(1, 
                           pt_R_TI_static, 
                           pt_R_TI_static, 
                           pt_R_UO_static, 
                           pt_R_UO_bump, 
                           pt_R_LO_static, 
                           pt_R_LO_bump, 
                           pt_R_TO_static)
    pt_R_PO_bump = Point3S(1, 
                           pt_R_UF_static, 
                           pt_R_UF_static, 
                           pt_R_UA_static, 
                           pt_R_UA_static, 
                           pt_R_UO_static, 
                           pt_R_UO_bump, 
                           pt_R_PO_static)
    pt_R_PI_bump = Point3S(1, 
                           pt_R_PO_static, 
                           pt_R_PO_bump, 
                           pt_R_ZA_static, 
                           pt_R_ZA_static, 
                           pt_R_ZF_static, 
                           pt_R_ZF_static, 
                           pt_R_PI_static)
    
    
    arr_F_deflection_full = np.append(arr_F_deflection_full, np.linalg.norm(pt_F_PI_bump - pt_F_PI_OG))
    F_deflection = np.linalg.norm(pt_F_PI_bump - pt_F_PI_static)
    arr_F_zbar_MR = np.append(arr_F_zbar_MR, F_deflection/bumpi)
    #print(index, '==', deflection/bumpi)
    
    arr_R_deflection_full = np.append(arr_R_deflection_full, np.linalg.norm(pt_R_PI_bump - pt_R_PI_OG))
    R_deflection = np.linalg.norm(pt_R_PI_bump - pt_R_PI_static)
    arr_R_zbar_MR = np.append(arr_R_zbar_MR, R_deflection/bumpi)
    #print(index, '==', deflection/bumpi)
    
    pt_F_LO_static = pt_F_LO_bump
    pt_F_UO_static = pt_F_UO_bump
    pt_F_TO_static = pt_F_TO_bump
    pt_F_PO_static = pt_F_PO_bump
    pt_F_PI_static = pt_F_PI_bump
    
    pt_R_LO_static = pt_R_LO_bump
    pt_R_UO_static = pt_R_UO_bump
    pt_R_TO_static = pt_R_TO_bump
    pt_R_PO_static = pt_R_PO_bump
    pt_R_PI_static = pt_R_PI_bump
    
    print(index, pt_F_LO_bump)

#print('bumpi size: ', bumpi.size)
#print(arr_zbar_MR)
#print('MR size: ', arr_zbar_MR.size)


zbarG = 77000 #MPa(Nmm-2), mild steel
zbarL = 1500/2 #mm
# Assumption - Longitudinal Z-Bar
# Assumption - Perfect 50/50 bar split F/R
F_zbarR = np.linalg.norm(np.array([pt_F_ZF_static[0], 0, pt_F_ZF_static[2]]) 
                       - np.array([pt_F_PI_static[0], 0, pt_F_PI_static[2]])) 
R_zbarR = np.linalg.norm(np.array([pt_R_ZF_static[0], 0, pt_R_ZF_static[2]]) 
                       - np.array([pt_R_PI_static[0], 0, pt_R_PI_static[2]])) 
zbarD = 25 #mm
zbard = 23.5 #mm

leafE = 200000 #MPa(Nmm-2), mild steel
F_leafB = 50 #mm width
F_leafH = 2.5 #mm thickness
F_leafIx = F_leafB*F_leafH**3 #mm4
F_leafL = 120 #mm (half-car width)

R_leafB = 50 #mm width
R_leafH = 2 #mm thickness
R_leafIx = R_leafB*R_leafH**3 #mm4
R_leafL = 120 #mm (half-car width)


F_force_per_disp_pitch = np.sign(heaverange) * arr_F_deflection_full*leafE*F_leafIx / (F_leafL**3)
R_force_per_disp_pitch = np.sign(heaverange) * arr_R_deflection_full*leafE*R_leafIx / (R_leafL**3)

# Needs to be altered for side-specific pitch?
F_force_per_disp_roll = np.sign(heaverange) * arr_F_deflection_full*np.pi*zbarG*(zbarD**4 - zbard**4) / (32*F_zbarR**2*zbarL)
R_force_per_disp_roll = np.sign(heaverange) * arr_F_deflection_full*np.pi*zbarG*(zbarD**4 - zbard**4) / (32*R_zbarR**2*zbarL)

F_lb_per_disp = (F_force_per_disp_pitch*ispitching + F_force_per_disp_roll*isrolling)*arr_F_zbar_MR/4.44822 + carw_fl
R_lb_per_disp = (R_force_per_disp_pitch*ispitching + R_force_per_disp_roll*isrolling)*arr_R_zbar_MR/4.44822 + carw_rl

F_interpointlation = np.interp(W_mat, F_lb_per_disp, heaverange)
R_interpointlation = np.interp(W_mat, R_lb_per_disp, heaverange)

#plt.plot(heaverange, F_lb_per_disp, 'o')

plt.plot(F_lb_per_disp, heaverange, '-')
plt.plot(R_lb_per_disp, heaverange, '-')

plt.plot(W_mat[0], F_interpointlation[0], 'D-r')
plt.plot(W_mat[1], F_interpointlation[1], 'D-r')
plt.plot(W_mat[2], R_interpointlation[2], 'D-g')
plt.plot(W_mat[3], R_interpointlation[3], 'D-g')

#plt.plot(heaverange, arr_F_deflection_full)
#plt.plot(heaverange, arr_R_deflection_full)

print('Deg Roll Difference: ',
      -np.arctan( (F_interpointlation[1]-F_interpointlation[0]) / track )*57.3
      +
      np.arctan( (R_interpointlation[3]-R_interpointlation[2]) / track )*57.3)
print('MM Roll Difference: ',
      track*np.sin(
                -np.arctan( (F_interpointlation[1]-F_interpointlation[0]) / track )
                +
                np.arctan( (R_interpointlation[3]-R_interpointlation[2]) / track ))
      )

#800*12*25.4*(2/track)*(
#      -np.arctan( (F_interpointlation[1]-F_interpointlation[0]) / track )*57.3
#      +
#      np.arctan( (R_interpointlation[3]-R_interpointlation[2]) / track )*57.3
#      )



plt.axis('auto')
plt.xlabel("Vertical Force (lbs)")
plt.ylabel("Displacement (mm)")

time2 = time.time()

print('Code Runtime (sec): ', time2-time1)

plt.show()

