import cv2 as cv
import libOpenClient as loc
from lookup_table import interpolation
import time as t
import numpy as np

#oc = loc.libOpenClient('200.128.140.12')

""" def calib_save():
    coordenadas_Cartesianas = oc.listen_cart()

    print("U: "+str(circles[0][0][0])+"\t\tV: "+str(circles[0][0][1]) + "\t\tX: " + str(coordenadas_Cartesianas.x) + "\tY: " +  str(coordenadas_Cartesianas.y))

    with open('moving.txt', 'a') as file:
        file.write(str(circles[0][0][0])+",\t"+str(circles[0][0][1]) + ",\t" + str(coordenadas_Cartesianas.x) + ",\t" +  str(coordenadas_Cartesianas.y)+";\n")
 """

#Resolucao de captura:
webcam = cv.VideoCapture(0, cv.CAP_V4L2)
webcam.set(cv.CAP_PROP_FRAME_WIDTH, 1150)
webcam.set(cv.CAP_PROP_FRAME_HEIGHT, 1150)
webcam.set(cv.CAP_PROP_FPS, 10)

#Identificando a mesa:
#Obter imagem:
ret, frame = webcam.read()

med_alvo_x = []
med_alvo_y = []
med_dest_x = []
med_dest_y = []

# Select ROI
#roi = cv.selectROI("imgName", frame, False, False)
#print(roi)
roi = (108, 351, 1348, 510)

while (True):
    medax = 0
    meday = 0
    meddx = 0
    meddy = 0
    med_alvo_x.clear()
    med_alvo_y.clear()
    med_dest_x.clear()
    med_dest_y.clear()
    m = 0
    #for l in range(50):
    while(True):

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

        #cv.imshow("Output", image)
        #cv.waitKey(1)

        #Aplicando Blur a imagem:
        image = cv.blur(image, (15, 15), 0)

        #Binarização com limiar:
        T = 200
        bin = image.copy()
        bin[bin > T] = 255
        bin[bin < 255] = 0
        #bin = cv.bitwise_not(bin)

        #cv.imshow("Output", bin)
        #cv.imshow("hsadiof", frame)
        #cv.waitKey(1)

        #Aplicacao da transformada de Rough:
        circles = cv.HoughCircles(bin,cv.HOUGH_GRADIENT,2,80,param1=1200,param2=3,minRadius=35,maxRadius=55)

        #Desenhando os circulos identificados:
        if(len(circles[0]) >= 2):
            r1 = int(circles[0][0][2])
            r2 = int(circles[0][1][2])
            if(r1 > r2):
                alvo = [int(circles[0][0][0]), int(circles[0][0][1])]
                destino = [int(circles[0][1][0]), int(circles[0][1][1])]
                cv.circle(frame, alvo, int(circles[0][0][2]), (0, 0, 255), 2)
                cv.circle(frame, destino, int(circles[0][1][2]), (255, 0, 0), 2)
            else:
                alvo = [int(circles[0][1][0]), int(circles[0][1][1])]
                destino = [int(circles[0][0][0]), int(circles[0][0][1])]
                cv.circle(frame, destino, int(circles[0][0][2]), (255, 0, 0), 2)
                cv.circle(frame, alvo, int(circles[0][1][2]), (0, 0, 255), 2)

            print('\n=> ALVO: \t' + str(round(alvo[0], 1)) + '\t' + str(round(alvo[1], 1)))
        #print('\n=> DESTINO: ' + str(round(destino[0], 1)) + '\t' + str(round(destino[1], 1)))
        
        """ (x, y) = interpolation.uv_to_xy(alvo[0], alvo[1])
        if(m == 0):
            med_alvo_x.append(x)
            med_alvo_y.append(y)
            m = m+1
        elif((abs(x-med_alvo_x[m-1]) < 10) and (abs(y-med_alvo_y[m-1]) < 10)):
            med_alvo_x.append(x)
            med_alvo_y.append(y)
            m = m+1

        (x, y) = interpolation.uv_to_xy(destino[0], destino[1])
        if(m == 0):
            med_dest_x.append(x)
            med_dest_y.append(y)
            m = m+1
        elif((abs(x-med_dest_x[m-1]) < 10) and (abs(y-med_dest_y[m-1]) < 10)):
            med_dest_x.append(x)
            med_dest_y.append(y)
            m = m+1 """

        cv.imshow("Output", frame)
        cv.waitKey(30)
    
    """ for k in range(50):
        medax = medax + med_alvo_x[k]
        meday = meday + med_alvo_y[k]
        meddx = meddx + med_dest_x[k]
        meddy = meddy + med_dest_y[k]

    print('\n=> ALVO: \t' + str(round((medax/50), 1)) + '\t' + str(round((meday/50), 1)))
    print('\n=> DESTINO: ' + str(round((meddx/50), 1)) + '\t' + str(round((meddy/50), 1)))

    t.sleep(30) """