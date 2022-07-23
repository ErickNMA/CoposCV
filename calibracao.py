# IMPORTAR BIBLIOTECAS

import matplotlib.pyplot as plt
import numpy as np
plt.close('all')

plotC = True
plotV = True

# FUNCAO PARA GERAR FIGURA

def new_fig(tabela):
    
    plt.figure(figsize=(5,8))
    
    
    plt.subplots_adjust(top=0.981,
        bottom=0.073,
        left=0.159,
        right=0.932,
        hspace=0.192,
        wspace=0.2
    )
    
    ax1 = plt.subplot(2,1,1)
    ax1.set_ylim(np.max(tabela[:,1])+50,np.min(tabela[:,1])-50)
    ax1.set_xlim(np.min(tabela[:,0])-50,np.max(tabela[:,0])+50)
    ax1.set_xlabel('u')
    ax1.set_ylabel('v')
    
    ax2 = plt.subplot(2,1,2)
    ax2.set_xlabel('y')
    ax2.set_ylabel('x')
    ax2.set_xlim(np.max(tabela[:,3])+50,np.min(tabela[:,3])-50)
    ax2.set_ylim(np.min(tabela[:,2])-50,np.max(tabela[:,2])+50)

    return ax1,ax2


# IMPORTAR DADOS DA CALIBRACAO

tabela = np.array([
	[+375.8, +711.6, 1000, 350],
	[+586.2, +715.6, 1000, 175],
	[+792.7, +720.9, 1000, 0],
	[+998.4, +728.1, 1000, -175],
	[+1207.2, +735.2, 1000, -350],
	[+359.4, +543.9, 1150, 350],
	[+580.5, +551.1, 1150, 175],
	[+800.1, +557.2, 1150, 0],
	[+1014.9, +562.5, 1150, -175],
	[+1240.3, +570.7, 1150, -350],
	[+337.3, +357.7, 1300, 350],
	[+575.3, +363.3, 1300, 175],
	[+807.0, +370.3, 1300, 0],
	[+1039.3, +377.3, 1300, -175],
	[+1273.5, +385.1, 1300, -350]
])

n = len(tabela)

matrizCalibracao = []

for i in range(n):
	u = tabela[i][0]
	v = tabela[i][1]
	matrizCalibracao.append([1,u, v, u**2, v**2, u*v])

# PLOTAR DADOS

if plotC:
	ax1,ax2 = new_fig(tabela)

	for i in range(n):
		u = tabela[i][0]
		v = tabela[i][1]
		x = tabela[i][2]
		y = tabela[i][3]
		ax1.plot(u, v, 'C0.')
		ax1.text(u, v-10, "%d" % (i+1))
		ax2.plot(y, x, 'C1.')
		ax2.text(y, x+10, "%d" % (i+1))

	if not plotV:
		plt.show()

# CALIBRACAO

tabelaC = np.copy(matrizCalibracao)

nC = len(tabelaC)

X1 = np.copy(tabelaC)
Y1 = np.copy(tabela)[:,2].reshape(nC,1)
b1 = np.linalg.pinv(X1) @ Y1

X2 = np.copy(tabelaC)
Y2 = np.copy(tabela)[:,3].reshape(nC,1)
b2 = np.linalg.pinv(X2) @ Y2

# VALIDACAO

tabelaV = np.array([
    [+1188.2, +645.2, +1081.4, -320.6],
    [+583.6, +604.9, +1101.6, +176.9],
    [+845.3, +527.1, +1174.9, -33.8],
    [+645.2, +433.6, +1246.7, +125.6],
    [+1228.0, +428.0, +1265.1, -320.6],
    [+1252.3, +645.9, +1083.7, -370.8],
    [+340.3, +620.2, +1083.7, +373.9],
    [+799.9, +630.5, +1084.4, +0.1],
    [+812.9, +321.7, +1336.9, +0.1],
])

nV = len(tabelaV)
u = tabelaV[:,0].reshape(nV,1)
v = tabelaV[:,1].reshape(nV,1)
xr = tabelaV[:,2].reshape(nV,1)
yr = tabelaV[:,3].reshape(nV,1)

nV = len(tabelaV)
X1 = np.hstack([u**0,u,v,u**2,v**2,u*v])
X2 = np.hstack([u**0,u,v,u**2,v**2,u*v])

xe = np.round(X1@b1,1)
ye = np.round(X2@b2,1)

# ANALISE DO ERRO

erro_x = abs(xr - xe)
erro_y = abs(yr - ye)


# PLOTAR DADOS DA VALIDACAO

if plotV:
	ax1,ax2 = new_fig(tabelaV)

	for i in range(nV):
		u = tabelaV[i][0]
		v = tabelaV[i][1]
		x = tabelaV[i][2]
		y = tabelaV[i][3]
		ax1.plot(u, v, 'C0.')
		ax2.plot(y, x, 'C1.')
		ax2.plot(ye[i], xe[i], 'C2.')
        
	plt.show(),plt.legend(['Pontos reais', 'Pontos estimados'])