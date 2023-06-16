
import numpy as np
option = 3
#np.set_printoptions(precision=2, sign='+')

frontperc = 46/100 #percent
track = 1194 #mm (t)
wheelbase = 1536 #mm (l)
CGlocA = (1-frontperc)*wheelbase #mm (a)
CGlocB = frontperc*wheelbase #mm (b)
CGheight = 300 #mm (h)
# Assumption - Assumes constants for each of these figures


CG = np.array([0, CGlocA, CGheight])
print('CG:', CG)


carw_total = 500 #lbs
carw_faxle = carw_total*frontperc
carw_raxle = carw_total*(1-frontperc)
# Assumption - Car weight L/R is 50/50

carw_fl = carw_faxle/2
carw_fr = carw_faxle/2
carw_rl = carw_raxle/2
carw_rr = carw_raxle/2

W_mat = np.array([carw_fl, carw_fr, carw_rl, carw_rr, carw_total])

print('W_mat:', W_mat)

if option == 1: # Roll, assumes given RC
    accX_g = float(input('Input lateral Gs (pos = left turn): '))
    deltaW_F = CGheight*carw_faxle*accX_g/track
    deltaW_R = CGheight*carw_raxle*accX_g/track
    deltaW_mat = np.array([-deltaW_F, deltaW_F, -deltaW_R, deltaW_R, 0])
    W_mat = W_mat + deltaW_mat
    print('W_mat(roll):', W_mat)
    
if option == 2:
    accY_g = float(input('Input longitudinal Gs (pos = accel): '))
    deltaW = CGheight*carw_total*accY_g/(wheelbase*2)
    deltaW_mat = np.array([-deltaW, -deltaW, deltaW, deltaW, 0])
    W_mat = W_mat + deltaW_mat
    print('W_mat(pitch):', W_mat)
    
if option == 3:
    heave_g = float(input('Input bump Gs: '))
    W_mat = W_mat*(heave_g+1)
    print('W_mat(heave):', W_mat)