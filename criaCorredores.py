#!/usr/bin/env python

import sys, os
import arcpy, arcinfo
import mylib
import numpy as np
import itertools


def criaCorredores(subDirTabela, nomeTabela):

    arcpy.CheckOutExtension("spatial")
    arcpy.env.overwriteOutput = True

    folderTabela = os.path.join (os.getcwd(), subDirTabela)
    filenameTabela = os.path.join (folderTabela, nomeTabela)
    
    if not os.path.exists(filenameTabela):
        print 'Tabela', nomeTabela, 'nao encontrada. Impossivel prosseguir...'
    else:

        grupos = mylib.leituraOcorrencias (filenameTabela)

        outputFolder = os.path.join (os.getcwd(), "Corredores\\%s"%(nomeTabela[0:-4]))
        if os.path.exists(outputFolder): mylib.removeDir(outputFolder)
        for grupo, lista in grupos:
            for local1, local2 in itertools.combinations(lista, 2):
                outputFolder2 = os.path.join (outputFolder, local1)
                if not os.path.exists(outputFolder2): os.makedirs(outputFolder2)
                outputFile = os.path.join (outputFolder2, local2)
                if not os.path.exists(outputFile):
                    print 'Criando corredor entre %s e %s (grupo %s)...'%(local1, local2, grupo)
                    dist1 = os.path.join (os.getcwd(), "Distancia\\%s"%(local1))
                    dist2 = os.path.join (os.getcwd(), "Distancia\\%s"%(local2))

                    print outputFile
                    arcpy.gp.Corridor_sa(dist1,dist2,outputFile)
                else:
                    print 'Corredor entre %s e %s (grupo %s) ja foi criado anteriormente.'%(local1, local2, grupo)
