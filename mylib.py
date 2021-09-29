#!/usr/bin/env python

import sys, os
import arcpy
import numpy as np

def leituraOcorrencias (filename):
    linhas = open (filename, 'r').readlines()
    linhas = linhas[1:]
    linhas = [ l.strip().split(',') for l in linhas ]
    linhas = [ l for l in linhas if l[0] != '' ]

    haplots = [ l[1] for l in linhas ]
    haplots = semRepeticao (haplots)

    grupos = []

    for haplot in haplots:
        grupo = (haplot, [])

        for linha in linhas:
            if linha[1] == haplot: grupo[1].append (linha[0])

        grupo[1].sort()
        grupos.append (grupo)

    return grupos


def semRepeticao (l):
    l.sort()
    l2 = [ l[0] ]

    for x in l[1:]:
        if l2[-1] != x: l2.append (x)

    return l2

def removeDir (top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
        
def saveASCII (mapa, name):
    print 'Salvando arquivo', name
    arq = open (name, 'w')
    cabecalho, dados = mapa

    for line in cabecalho: arq.write (line)

    rows = len (dados)
    cols = len (dados[0])

    for i in range (rows):
        for j in range (cols):
            if dados[i][j] == -9999: arq.write ('%d '%(dados[i][j]))
            else: arq.write ('%f '%(dados[i][j]))
        arq.write ('\n')

    arq.close ()
    print 'Arquivo', name, 'salvo com sucesso.'

def loadASCII (name):
    print 'Lendo arquivo', name
    arq = open (name, 'r')
    lines = arq.readlines()

    cabecalho = lines[0:6]
    dados = np.array ([[float(y) for y in x.split()] for x in lines[6:]])

    arq.close ()
    print 'Arquivo', name, 'lido com sucesso.'
    return (cabecalho, dados)


