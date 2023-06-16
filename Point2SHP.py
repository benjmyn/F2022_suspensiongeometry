
import numpy as np

def Point2SHP(POINTOPTION, P1, P2, P3, zhp):
    
    S1 = P1-P3
    S2 = P2-P3
    
    x1 = P1[0]
    x2 = P2[0]
    
    y1 = P1[1]
    y2 = P2[1]
    
    z1 = P1[2]
    z2 = P2[2]
    z = zhp
    
    R1 = np.linalg.norm(P1-P3)
    R2 = np.linalg.norm(P2-P3)

    C = (x1**2 - x2**2) + (y1**2 - y2**2) + (z1**2 - z2**2) + (R2**2 - R1**2)
    
    
    Bx = (C/2 - (z1-z2)*z) / (y1-y2)
    Mx = (x1-x2) / (y1-y2)
    
    By = (C/2 - (z1-z2)*z) / (x1+0.00001-x2)
    My = (y1-y2) / (x1+0.00001-x2)
    
    
    if Bx == float('inf') or Mx == float('inf'):
        polyA = (1+My**2)
        polyB = 2*(-y1 + x1*My - By*My)
        polyC = y1**2 + By**2 + x1**2 - 2*By*x1 + z**2 - 2*z*z1 + z1**2 - R1**2

        y = np.roots([polyA, polyB, polyC])
        y = y[POINTOPTION]
        x = By - My*y

    else:    
        polyA = (1+Mx**2)
        polyB = 2*(-x1 + y1*Mx - Bx*Mx)
        polyC = x1**2 + Bx**2 + y1**2 - 2*Bx*y1 + z**2 - 2*z*z1 + z1**2 - R1**2

        x = np.roots([polyA, polyB, polyC])
        x = x[POINTOPTION-1]
        y = Bx - Mx*x
    
    return np.array([x, y, z])