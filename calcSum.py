#!/usr/bin/env python

import sys, os, itertools
import arcpy
import mylib

def calcSum(subPastaCorredores):

    arcpy.CheckOutExtension("Spatial")

    folderCor = os.path.join (os.getcwd(), "Corredores\\%s"%(subPastaCorredores))
    folderSum = os.path.join (os.getcwd(), "Somatoria\\%s"%(subPastaCorredores))
    arcpy.env.overwriteOutput = True

    if not os.path.exists(os.path.join (os.getcwd(), "Somatoria")): os.makedirs(os.path.join (os.getcwd(), "Somatoria"))

    filenameLocalidades = os.path.join (os.getcwd(), "TabelaCSV\\%s.csv"%(subPastaCorredores))
    grupos = mylib.leituraOcorrencias (filenameLocalidades)

    todosCorredores = []
    for grupo, lista in grupos:
        pares = list (itertools.combinations(lista, 2))
        todosCorredores += pares

    print todosCorredores
    cidade1, cidade2 = todosCorredores[0]
    filenameGrid = os.path.join (folderCor, "%s\\Reclassificados\\%s"%(cidade1, cidade2))
    print 'Abrindo primeiro grid entre cidades %s e %s'%(cidade1, cidade2)
    calcTotal = arcpy.Raster(filenameGrid)

    for cidade1, cidade2 in todosCorredores[1:]:
        filenameGrid = os.path.join (folderCor, "%s\\Reclassificados\\%s"%(cidade1, cidade2))
        print 'Abrindo grid entre cidades %s e %s'%(cidade1, cidade2)
        calcTotal += arcpy.Raster(filenameGrid)

    print 'Salvando somatorio final'
    calcTotal.save (folderSum)


