import numpy as np

class point:
    def __init__(self, a, b, c, d):
        self.u = a
        self.v = b
        self.y = c
        self.x = d

class reg:
    def __init__(self, p1, p2, p3, p4):
        dv = float(p1.v-p2.v)
        du = float(p1.u-p2.u)
        if(du != 0):
            self.a1 = (dv/du)
            self.b1 = (p1.v - ((dv/du)*p1.u))
        else:
            self.a1 = 0
            self.b1 = 0

        dv = float(p2.v-p3.v)
        du = float(p2.u-p3.u)
        if(du != 0):
            self.a2 = (dv/du)
            self.b2 = (p2.v - ((dv/du)*p2.u))
        else:
            self.a2 = 0
            self.b2 = 0
        
        dv = float(p3.v-p4.v)
        du = float(p3.u-p4.u)
        if(du != 0):
            self.a3 = (dv/du)
            self.b3 = (p3.v - ((dv/du)*p3.u))
        else:
            self.a3 = 0
            self.b3 = 0
        
        dv = float(p4.v-p1.v)
        du = float(p4.u-p1.u)
        if(du != 0):
            self.a4 = (dv/du)
            self.b4 = (p4.v - ((dv/du)*p4.u))
        else:
            self.a4 = 0
            self.b4 = 0

class function:
    c = 0
    d = 0
    e = 0
    f = 0

p00 = point(129.5, 224.5, 426, 1216.8)
p01 = point(236.5, 225.5, 261.5, 1216.8)
p02 = point(377.5, 232.5, 41.3, 1216.8)
p03 = point(506.5, -157.5, 426, 1216.8)
p04 = point(658.5, 241.5, -394.6, 1210.6)

p10 = point(136.5, 309.5, 430, 1066.7)
p11 = point(247.5, 313.5, 250.5, 1066.8)
p12 = point(504.5, 227.5, 21.8, 1066.8)
p13 = point(505.5, 324.5, -165.2, 1066.8)
p14 = point(646.5, 323.5, -404.72, 1066.8)

p20 = point(149.5, 372.5, 421.8, 943.4)
p21 = point(250.5, 377.5, 250.5, 943.4)
p22 = point(383.5, 383.5, 23.6, 943.4)
p23 = point(504.5, 386.5, -183.5, 943.4)
p24 = point(634.5, 386.5, -408.6, 943.4)


table = [[p00, p01, p02, p03, p04], [p10, p11, p12, p13, p14], [p20, p21, p22, p23, p24]]

fields = [[table[0][0], table[1][0], table[1][1], table[0][1]], [table[1][0], table[2][0], table[2][1], table[1][1]], [table[0][1], table[1][1], table[1][2], table[0][2]], [table[1][1], table[2][1], table[2][2], table[1][2]], [table[0][2], table[1][2], table[1][3], table[0][3]], [table[1][2], table[2][2], table[2][3], table[1][3]], [table[0][3], table[1][3], table[1][4], table[0][4]], [table[1][3], table[2][3], table[2][4], table[1][4]]]

consts = [reg(fields[0][0], fields[0][1], fields[0][2], fields[0][3]), reg(fields[1][0], fields[1][1], fields[1][2], fields[1][3]), reg(fields[2][0], fields[2][1], fields[2][2], fields[2][3]), reg(fields[3][0], fields[3][1], fields[3][2], fields[3][3]), reg(fields[4][0], fields[4][1], fields[4][2], fields[4][3]), reg(fields[5][0], fields[5][1], fields[5][2], fields[5][3]), reg(fields[6][0], fields[6][1], fields[6][2], fields[6][3]), reg(fields[7][0], fields[7][1], fields[7][2], fields[7][3])]

def getField(u, v):
    for i in range(len(consts)):
        u_min = ((v - consts[i].b1)/consts[i].a1)
        u_max = ((v - consts[i].b3)/consts[i].a3)
        v_max = ((consts[i].a2*u)+consts[i].b2)
        v_min = ((consts[i].a4*u)+consts[i].b4)
        if((u >= u_min) and (u <= u_max) and (v >= v_min) and (v <= v_max)):
            return (i+1)

def uv_to_yx(u, v):
    field = getField(u, v)
    D = []
    for i in range(len(fields[field])):
        D.append([fields[field][i].u, fields[field][i].v, (fields[field][i].u * fields[field][i].v), 1])
    #Encontrando as constantes para x, por Cramer:
    Dc = D
    Dd = D
    De = D
    Df = D
    for i in range(len(fields[field])):
        Dc[0][i] = fields[field][i].x
        Dd[1][i] = fields[field][i].x
        De[2][i] = fields[field][i].x
        Df[3][i] = fields[field][i].x
    cx = (np.linalg.det(Dc)/np.linalg.det(D))
    dx = (np.linalg.det(Dd)/np.linalg.det(D))
    ex = (np.linalg.det(De)/np.linalg.det(D))
    fx = (np.linalg.det(Df)/np.linalg.det(D))
    #Encontrando as constantes para y, por Cramer:
    Dc = D
    Dd = D
    De = D
    Df = D
    for i in range(len(fields[field])):
        Dc[0][i] = fields[field][i].y
        Dd[1][i] = fields[field][i].y
        De[2][i] = fields[field][i].y
        Df[3][i] = fields[field][i].y
    cy = (np.linalg.det(Dc)/np.linalg.det(D))
    dy = (np.linalg.det(Dd)/np.linalg.det(D))
    ey = (np.linalg.det(De)/np.linalg.det(D))
    fy = (np.linalg.det(Df)/np.linalg.det(D))

    x = ((cx*u) + (dx*v) + (ex*u*v) + fx)
    y = ((cy*u) + (dy*v) + (ey*u*v) + fy)

    return (x, y)


print(uv_to_yx(129.5, 224.5))