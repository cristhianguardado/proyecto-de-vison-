
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

    #masa,imagen,centros=formas(image)

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



def formas(img,im):

    imagen,masa,centros=c_colorear(img,im)

    return masa,imagen,centros



def c_colorear(im,imag):

    pixels=im.load()

    porcentajes=[]

    fondos=[]

    centro_masa=[]

    masa=[]

    ancho,alto=im.size

    t_pixels=ancho*alto

    c=0

    #pintar=[]

    f=0

    m=[]

    for i in range(ancho):

        for j in range(alto):

            pix = pixels[i,j]

            r,g,b= random.randint(0,255),random.randint(0,255), random.randint(0,255)

            fondo=(r,g,b)

            if (pix==(0,0,0)):

                #print 'entro'

                c +=1

                origen=(i,j)

                num_pixels,abscisa,ordenada,puntos=bfs(pix,origen,im,fondo)

                p=(num_pixels/float(t_pixels))*100

                if p>.3:

                    centro=(sum(abscisa)/float(num_pixels),sum(ordenada)/float(num_pixels))

                        #centro_masa.append(centro)

                    masa.append(num_pixels)

                    v=detectar_elipse(num_pixels,im,centro,puntos,fondo)

                    if v==True: 

                       # print 'ES CIRCULO'

                        porcentajes.append(p)

                        pintar(puntos,im)

                           # self.pintar(puntos)

                        fondos.append(fondo)

                        centro_masa.append(centro)

                        #print 'pintar',pintar

                        #pinta(pintar,imag)

    

                    #detectar_rectangulo(num_pixels,img,centro,puntos,fondo)

   # print 'pintar',pintar

    #pinta(pintar,imag)

    im.save('final.jpg')

    imprimir_porcentajes(porcentajes)



    return im,m,centro_masa





def pintar(puntos,im):

    pixels=im.load()

    putpixel = im.putpixel

        #r,g,b= random.randint(0,255),random.randint(0,255), random.randint(0,255)

        #fondo=(r,g,b)    

    fondo=(255,0,0)

    for m in puntos:

        #pixels[m[0],m[1]]==fondo

        putpixel((m[0], m[1]), fondo)

        im.save('resultado_final.png')

    return im



     

def detectar_elipse(num_pixeles,im,centro,puntos,fondo):

    pixels=im.load()

    inicio=centro

    x,y=int(centro[0]),int(centro[1])

    im.save('checar.png')

    a=semidiametrox(x,y,pixels,im,fondo)

   # print 'a',a

   # print 'area',area1

    area1=pi*pow(a,2)

    #print 'area',area1

    if  num_pixeles<area1<num_pixeles+40000:

        return True



def semidiametrox(aumenta,igual,pixels,im,fondo):

   # print 'sacando semidiametro'

    pixels=im.load()

    a=0

    while True:

        if (pixels[aumenta,igual]==fondo):

            aumenta +=1

            a +=1 

        else:

            break

    return a    



def imprimir_porcentajes(porcentajes):

    for i,p in enumerate(porcentajes):

        print 'Figura ID: %d  Porcentaje: %f' %(i,p)

        



def bfs(pix,origen,im,fondo):

    pixels=im.load()

    cola=list()

    lista=[-1,0,1]

    abscisa=[]

    ordenada=[]

    puntos=[]

    cola.append(origen)

    original = pixels[origen]

    num=1

    while len(cola) > 0:

        (i,j)=cola.pop(0)

        actual = pixels[i,j]

        if actual == original or actual==fondo:

            for x in lista:

                for y in lista:

                    a= i+x

                    b = j+y 

                    try:

                        if pixels[a,b]:

                            contenido = pixels[a,b]

                            if contenido == original:

                                pixels[a,b] = fondo

                                abscisa.append(a)

                                ordenada.append(b)

                                num +=1

                                cola.append((a,b))

                                puntos.append((a,b))

                    except IndexError:

                        pass

    im.save('FORMAS.png')

    return num,abscisa,ordenada,puntos



if __name__ == "__main__":

	image1,gx,gy,minimo,maximo,conv,analis=boton(argv[1])

	er,analis=erosion(image1,analis)

	image=dilatacion(er,analis)

        masa,imagen,centros=formas(image,image)

