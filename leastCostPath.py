#!/usr/bin/env python

import sys, os
import arcpy
import inverteMapa, criaDistancias, criaCorredores, reclassify, calcSum



def main():

    arcpy.CheckOutExtension("Spatial")

    ############# ALTERAR PASTA COM MAPA ORIGINAL E NOME DO MAPA ############
    subDir = 'MapaOriginal'
    nome = 'mapa'
    ############# ALTERAR PASTA COM SHAPEFILE DAS LOCALIDADES ###############
    subDirShape = 'Shapefile'
    nomeShape = 'exemplo.shp'
    ############# ALTERAR PASTA COM TABELA ORIGINAL E NOME DA TABELA ########
    subDirTabela = 'TabelaCSV'
    nomeTabela = 'Nec15.csv'
    #########################################################################


    #############              SCRIPT: INVETE_MAPA               ############
    #inverteMapa.inverte(subDir, nome)

    #############              SCRIPT: CRIA_DISTANCIAS           ############
    #criaDistancias.criaDistancias(subDir, 'mapa_inv', subDirShape, nomeShape)

    #############              SCRIPT: CRIA_CORREDORES           ############
    criaCorredores.criaCorredores(subDirTabela, nomeTabela)

    #############              SCRIPT: RECLASSIFICA              ############
    subPastaCorredores = nomeTabela[:-4]
    reclassify.reclassifica(subPastaCorredores)

    #############              SCRIPT: SOMATORIO                 ############
    calcSum.calcSum(subPastaCorredores)


if __name__ == '__main__':
	main()


