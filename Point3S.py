
import numpy as np

def Point3S(POINTOPTION, static1, dynamic1, static2, dynamic2, static3, dynamic3, static4):
    
    x1 = dynamic1[0]
    x2 = dynamic2[0]
    x3 = dynamic3[0]
    y1 = dynamic1[1]
    y2 = dynamic2[1]
    y3 = dynamic3[1]
    z1 = dynamic1[2]
    z2 = dynamic2[2]
    z3 = dynamic3[2]
    
    R1 = np.linalg.norm(static1 - static4)
    R2 = np.linalg.norm(static2 - static4)
    R3 = np.linalg.norm(static3 - static4)
    
    u2 = x2-x1
    v2 = y2-y1
    w2 = z2-z1
    u3 = x3-x1
    v3 = y3-y1
    w3 = z3-z1
    
    c1 = R1**2
    c2 = R2**2 - (u2**2 + v2**2 + w2**2)
    c3 = R3**2 - (u3**2 + v3**2 + w3**2)
    c4 = 0.5*(c1-c2)
    c5 = 0.5*(c1-c3)
    
    a1 = w3*u2 - w2*u3
    a2 = w3*v2 - w2*v3
    a3 = w3*c4 - w2*c5
    a4 = a3/a2
    a5 = -a1/a2
    
    b1 = (c4 - a4*v2) / (w2+0.0000000001) # NaN
    b2 = -(u2 + a5*v2) / (w2+0.0000000001) # NaN
    
    A = 1 + a5**2 + b2**2
    B = 2*(a4*a5 + b1*b2 - (1+a5**2+b2**2)*x1)
    C = -2*(a4*a5 + b1*b2)*x1 + a4**2 + b1**2 - R1**2 + (1+a5**2+b2**2)*(x1**2)
    
    roots = np.roots([A, B, C])
    xout = roots[POINTOPTION-1]
    yout = a4 + a5*xout - a5*x1 + y1
    zout = b1 + b2*xout - b2*x1 + z1
    
    return np.array([xout, yout, zout])
    