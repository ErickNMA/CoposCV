import cv2 as cv
import libOpenClient as loc
from lookup_table import interpolation
import time as t
import numpy as np

def find_xy(uk, vk):
    list_u = []
    list_v = []
    n = 0
    for i in range(int(uk)-100,int(uk)+100):
        for j in range(int(vk)-100,int(vk)+100):
            try:
                if (bin[j][i] == 255):
                    list_u.append(i)
                    list_v.append(j)
                    n+=1
            except: 
                pass
    
    if len(list_u) !=0:
        uk = sum(list_u) / len(list_u)
        vk = sum(list_v) / len(list_v)

    cv.circle(frame, [int(uk),int(vk)], 5, (0, 255, 255), 2)

    u = round( (uk+ roi[0])/2 , 1)
    v = round( (vk+ roi[1])/2 , 1)
    x = np.sum(np.array([ 1.46597571e+03,  1.31243271e-01, -8.22592943e-01, -1.21769489e-04, -1.74839687e-03,  9.58774954e-05])*np.array([1,u,v,u**2,v**2,u*v]))
    y = np.sum(np.array([ 5.21405242e+02, -1.26623726e+00,  4.74633446e-01,  1.81918022e-05, -1.08157031e-04, -1.22588526e-03])*np.array([1,u,v,u**2,v**2,u*v]))
    return x,y,n

#oc = loc.libOpenClient('200.128.140.12')

""" def calib_save():
    coordenadas_Cartesianas = oc.listen_cart()

    print("U: "+str(circles[0][0][0])+"\t\tV: "+str(circles[0][0][1]) + "\t\tX: " + str(coordenadas_Cartesianas.x) + "\tY: " +  str(coordenadas_Cartesianas.y))

    with open('moving.txt', 'a') as file:
        file.write(str(circles[0][0][0])+",\t"+str(circles[0][0][1]) + ",\t" + str(coordenadas_Cartesianas.x) + ",\t" +  str(coordenadas_Cartesianas.y)+";\n")
 """

#Resolucao de captura:
webcam = cv.VideoCapture(1, cv.CAP_V4L2)
webcam.set(cv.CAP_PROP_FRAME_WIDTH, 1150)
webcam.set(cv.CAP_PROP_FRAME_HEIGHT, 1150)
webcam.set(cv.CAP_PROP_FPS, 10)

#Identificando a mesa:
ret, frame = webcam.read()
#roi = cv.selectROI("imgName", frame, False, False)
#print(roi)
roi = (108, 351, 1348, 510)

while (True):
    m = 0

    if True:

        #Obter imagem:
        ret, frame = webcam.read()

        # Crop image
        frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

        #Conversao para tons de cinza:
        gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        #Aplicando brilho e contraste:
        alpha = 1
        beta = 200
        image = np.uint8(np.clip((alpha*gray_image+beta), 0, 255))

        #Aplicando Blur a imagem:
        image = cv.blur(image, (15, 15), 0)

        #Binarização com limiar:
        T = 200
        bin = image.copy()
        bin[bin > T] = 255
        bin[bin < 255] = 0

        #Aplicacao da transformada de Rough:
        circles = cv.HoughCircles(bin,cv.HOUGH_GRADIENT,2,80,param1=1200,param2=3,minRadius=35,maxRadius=55)

        #Desenhando os circulos identificados:
        if(len(circles[0]) >= 2):
            circulo1 = [int(circles[0][0][0]), int(circles[0][0][1])]
            circulo2 = [int(circles[0][1][0]), int(circles[0][1][1])]
            
            x1,y1,n1 = find_xy(circulo1[0], circulo1[1])
            x2,y2,n2 = find_xy(circulo2[0], circulo2[1])

            if n1 < n2:
                pequen = (x1, y1)
                grande = (x2, y2)
            else:
                grande = (x1, y1)
                pequen = (x2, y2)
            
            print("%+.1f - %+.1f \t\t %+.1f - %+.1f" % (pequen[0], pequen[1], grande[0], grande[1]))
            
        cv.imshow("Output", frame)
        cv.waitKey(30)