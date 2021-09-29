#!/usr/bin/env python


import sys, os
import arcpy
import mylib

def inverteMapa (mapa):
    print 'Invertendo o mapa.'
    cabecalho, dados = mapa

    rows, cols = dados.shape
    dados[dados!=-9999] = 1 - dados[dados!=-9999]

    return cabecalho, dados

    
def inverte(subDir, nome):


    inputFolder = os.path.join (os.getcwd(), subDir)
    filename = os.path.join (inputFolder, nome)
    arcpy.env.overwriteOutput = True
    #inputFolder = "C:\Nectomys squamipes\Conectividade Populacional\Corredores"

    if not os.path.isfile(filename+'.asc'):
        print 'Arquivo ASC nao encontrado. Tentando converter...'
        try:
            arcpy.RasterToASCII_conversion(filename+'.tif', filename+'.asc')
            print 'Mapa convertido.'
        except:
            print 'Impossivel converter.'
        
    if not os.path.isfile(filename+'.asc'):
        print 'Arquivo ASC nao encontrado novamente. Impossivel continuar.'
    else:
        mapa = mylib.loadASCII (filename+'.asc')
        mapa = inverteMapa (mapa)
        mylib.saveASCII (mapa, filename+'_inv.asc')
        arcpy.ASCIIToRaster_conversion(filename+'_inv.asc', filename+'_inv', 'FLOAT')

