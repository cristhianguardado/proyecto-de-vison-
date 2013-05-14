import math
import sys
import os
import Image, ImageDraw, ImageFont
import random
import numpy as np
from math import *
from sys import argv
import numpy 

def boton(img):
    image = filtrar(img)
    image.save('filtro.png')
    image,gx,gy,minimo,maximo,conv = contorno(image)
    image.save('bordes.png')
    img=normalizar(image,minimo,maximo,conv)
    img.save('normalizada.png')
    im_bin,analis = binarizar(img)
    img.save('binarizada.png')
    return im_bin,gx,gy,minimo,maximo,conv,analis

def contorno(image):
    sobelx = ([-1,0,1],[-2,0,2],[-1,0,1]) 
    sobely = ([1,2,1],[0,0,0],[-1,-2,-1])     
    img,gx,gy,minimo,maximo,conv=convolucion(sobelx,sobely,image)
    return img,gx,gy,minimo,maximo,conv

def convolucion(sobelx,sobely,image):
    foto = image.load()
    ancho, alto = image.size 
    m=len(sobelx[0])
    conv = np.empty((ancho, alto))
    gx=numpy.empty((ancho, alto))
    gy=numpy.empty((ancho, alto))
    minimo = 255
    maximo = 0
    for x in range(ancho):
        for y in range(alto):
            sumax = 0.0
            sumay = 0.0
            for i in range(m): 
                for j in range(m): 
                    try:
                        sumax +=(foto[x+i,y+j][0]*sobelx[i][j])
                        sumay +=(foto[x+i,y+j][0]*sobely[i][j])

                    except:
                        pass
            gradiente = math.sqrt(pow(sumax,2)+pow(sumay,2))
            conv[x,y]=gradiente
            gx[x,y]=sumax
            gy[x,y]=sumay
            gradiente = int(gradiente)
            foto[x,y] = (gradiente,gradiente,gradiente)
            p = gradiente
            if p <minimo:
                minimo = p
            if  p > maximo:
                maximo = p
    image.save('convolucion.png')
    return image,gx,gy,minimo,maximo,conv

def normalizar(image,minimo,maximo,conv):
    foto = image.load()
    dif = maximo-minimo
    prom_pixel = 255.0/dif
    ancho,alto = image.size
    for i in range(ancho):
        for j in range(alto):
            pixel =int(floor((conv[i,j]-minimo)*prom_pixel))
            foto[i,j]=(pixel,pixel,pixel);
  return image

def binarizar(img):
    foto = img.load()
    ancho,alto = img.size
    analis = numpy.empty((ancho, alto))
    minimo = int(argv[2])
    for i in range(ancho):
        for j in range(alto):
            if foto[i,j][1] < minimo:
                p=0
            else:
                p= 255
            foto[i,j]=(p,p,p)
            analis[i,j]= p
    return img,analis

def filtrar(image):
    image,analis = escala(image)
    foto = image.load()
    ancho, alto =image.size
    listas = [-1,0,1]
    for i in range(ancho):
        for j in range(alto):
            prom = vecino(i,j,listas,analis)
            foto[i,j] = (prom,prom,prom)
    image.save('filtro.png')
    return image

def escala(image):
    image = Image.open(image) 
    foto = image.load()
    ancho,alto = image.size
    analis = numpy.empty((ancho, alto))
    for i in range(ancho):
        for j in range(alto):
            (r,g,b) = image.getpixel((i,j))
            tam = (r+g+b)/3
            foto[i,j] = (tam,tam,tam)
            analis[i,j] = int(tam)
    a = image.save('escala_gris.png')
    return image,analis

def vecino(i,j,listas,analis):
    promedio = 0
    n  = 0
    for x in listas:
        for y in listas:
            a = i+x
            b = j+y
            try:
                if analis[a,b] and (x!=a and y!=b):
                    promedio += analis[a,b] 
                    n +=1            
            except IndexError:
                pass
            try:
                promedio=int(promedio/n)
                return promedio
            except ZeroDivisionError:
                return 0  

def obtener_pixel(i,j,listas,analis,ancho,alto):
    lista_pixel=[]
    for x in listas:
        for y in listas:
            a = i+x
            b = j+y
            try:
                if a >= 0 and a < ancho and b >= 0 and b < alto:
                  lista_pixel.append(analis[a,b])
            except IndexError:
                pass
         
    return lista_pixel

def erosion(image,analis):
	foto = image.load()
	ancho, alto =image.size
	analis_2 = numpy.empty((ancho, alto))
	listas = [-1,0,1]
	for i in range(ancho):
		for j in range(alto):
			valor_min = obtener_pixel(i,j,listas,analis,ancho,alto)
			valor_min = int(min(valor_min))
			#print 'valor minimo',valor_min
			analis_2[i,j] = valor_min
			foto[i,j] = (valor_min,valor_min,valor_min)
	image.save('erosion.png')
	return image,analis

def dilatacion(image,analis):
	foto = image.load()
	ancho, alto =image.size
	listas = [-1,0,1]
	for i in range(ancho):
		for j in range(alto):
			valor_max = obtener_pixel(i,j,listas,analis,ancho,alto)
			valor_max = int(max(valor_max))
			#print 'valor maximo',valor_max
			foto[i,j] = (valor_max,valor_max,valor_max)
	image.save('dilatacion.png')
	return image


if __name__ == "__main__":
	image,gx,gy,minimo,maximo,conv,analis=boton('estudio.png')
	erosion(image,analis)
	dilatacion(image,analis)
	
