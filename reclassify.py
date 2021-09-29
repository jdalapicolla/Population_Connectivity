#!/usr/bin/env python

import sys, os
import arcpy
import numpy as np

def SubDirPath (d):
    return filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)])


def findMin (mapa):
    minimum = float ('inf')	

    for row in mapa:
        for cell in row:
            if cell < minimum and cell != -9999: minimum = cell
	
    return minimum

def changeMap2 (mapa, minimum):
    mask1 = (mapa <= 1.01*minimum) & (mapa != -9999)
    mask2 = (mapa <= 1.02*minimum) & (mapa > 1.01*minimum)
    mask3 = (mapa <= 1.05*minimum) & (mapa > 1.02*minimum)
    mask4 = mapa > 1.05*minimum

    mapa[mask1] = 5
    mapa[mask2] = 2
    mapa[mask3] = 1
    mapa[mask4] = 0

    return mapa

def changeMap (mapa, minimum):
    rows = len (mapa)
    cols = len (mapa[0])

    pos1 = []
    pos2 = []
    pos3 = []
    pos4 = []

    for i in range (rows):
        for j in range (cols):
            if mapa[i][j] <= 1.01*minimum and mapa[i][j] != -9999: pos1.append ( (i,j) )
            if mapa[i][j] > 1.01*minimum and mapa[i][j] <= 1.02*minimum: pos2.append ( (i,j) )
            if mapa[i][j] > 1.02*minimum and mapa[i][j] <= 1.05*minimum: pos3.append ( (i,j) )
            if mapa[i][j] > 1.05*minimum: pos4.append ( (i,j) )
	
    for i, j in pos1: mapa[i][j] = 5
    for i, j in pos2: mapa[i][j] = 2
    for i, j in pos3: mapa[i][j] = 1
    for i, j in pos4: mapa[i][j] = 0

    return mapa

def saveMap (mapa, arq):
    rows = len (mapa)
    cols = len (mapa[0])

    for i in range (rows):
        for j in range (cols):
            arq.write ('%d '%(int(mapa[i][j])))
        arq.write ('\n')

def reclassifica2 (arqEntrada, arqSaida):
    lines = arqEntrada.readlines()
    for line in lines[0:6]:
        arqSaida.write (line)

    mapa = np.array ([[float(y) for y in x.split()] for x in lines[6:]])

    mask = mapa != -9999
    minimum = np.min (mapa[mask])
    mapa = changeMap2 (mapa, minimum)
    saveMap (mapa, arqSaida)

def reclassifica (arqEntrada, arqSaida):
    lines = arqEntrada.readlines()
    for line in lines[0:6]:
        arqSaida.write (line)

    mapa = [[float(y) for y in x.split()] for x in lines[6:]]

    minimum = findMin (mapa)
    mapa = changeMap (mapa, minimum)
    saveMap (mapa, arqSaida)


def reclassifica(subPastaCorredores):


    inputFolder = os.path.join (os.getcwd(), "Corredores\\%s"%(subPastaCorredores))
    arcpy.env.overwriteOutput = True

    for folder in SubDirPath (inputFolder):
        reclassFolder = os.path.join (folder, 'Reclassificados')
        if not os.path.exists(reclassFolder): os.makedirs(reclassFolder)

        for subfolder in SubDirPath (folder):
            if os.path.basename(subfolder) not in ["info", "Reclassificados"]:
                print subfolder
                
                # Criando primeiro arquivo ASC
                name = subfolder + ".asc"
                if os.path.exists(name): os.remove(name)
                print 'Convertendo para ASC...'
                arcpy.RasterToASCII_conversion(subfolder, name)

                # Reclassificando
                arqEntrada = open (name, 'r')
                reclassName = os.path.join (reclassFolder, os.path.basename(name))
                arqSaida = open (reclassName, 'w')
                print 'Calculando a reclassificacao...'
                reclassifica2 (arqEntrada, arqSaida)
                arqSaida.close ()
                arqEntrada.close ()
                os.remove(name)

                # Criando o GRID reclassificado
                gridName = os.path.join (reclassFolder, os.path.basename(subfolder))
                print 'Convetendo para GRID...'
                arcpy.ASCIIToRaster_conversion(reclassName, gridName, 'FLOAT')
                os.remove(reclassName)

