import interpolation as itp
import matplotlib.pyplot as plt

with open('moving.txt', 'r') as file:
        texto = file.readlines()

u = []
v = []
xreal = []
yreal = []

for i in range(len(texto)):
    line = texto[i].split('\t')
    u.append(round(float(line[0].replace(',', '')), 1))
    v.append(round(float(line[1].replace(',', '')), 1))
    xreal.append(round(float(line[2].replace(',', '')), 1))
    yreal.append(round(float(line[3].replace(';\n', '')), 1))

xcalc = []
ycalc = []

for i in range(len(texto)):
    (x, y) = itp.uv_to_xy(u[i], v[i])
    if((x != None) and (y != None)):
        xcalc.append(x)
        ycalc.append(y)

plt.scatter(ycalc, xcalc)
plt.show()