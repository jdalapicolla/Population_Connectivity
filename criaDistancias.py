#!/usr/bin/env python

import sys, os
import arcpy, arcinfo
import mylib
import numpy as np

def criaDistancias(subDirMapa, nomeMapa, subDirShape, nomeShape):

    arcpy.CheckOutExtension("spatial")
    arcpy.env.overwriteOutput = True

    folderMapa = os.path.join (os.getcwd(), subDirMapa)
    filenameMapa = os.path.join (folderMapa, nomeMapa)
    
    folderShape = os.path.join (os.getcwd(), subDirShape)
    filenameShape = os.path.join (folderShape, nomeShape)
    folderShape = os.path.join (folderShape, 'TEMP')
    if not os.path.exists(folderShape): os.makedirs(folderShape)
    if not os.path.exists(os.path.join (os.getcwd(), 'Distancia')): os.makedirs(os.path.join (os.getcwd(), 'Distancia'))
    
    if not os.path.exists(filenameMapa):
        print 'Arquivo GRID invertido nao encontrado. Impossivel prosseguir...'
    else:
        
        cursor = arcpy.SearchCursor(filenameShape)
        index=0
        for row in cursor:
            municipio = row.getValue("municipio")
            outputFolder = os.path.join (os.getcwd(), 'Distancia\\'+municipio)
            arcpy.MakeFeatureLayer_management(filenameShape, municipio, " municipio = '%s'"%(municipio))
            arcpy.CopyFeatures_management(municipio, os.path.join (folderShape, municipio))
            arcpy.gp.CostDistance_sa(os.path.join (folderShape, municipio)+'.shp', filenameMapa, outputFolder, "#", "#")
            print 'Distancias criadas para localidade', municipio

        del cursor

