#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import requests
import ast
import datetime
import random
from multiprocessing.dummy import Pool

from slugify import slugify


devel = False

if devel:
    DESTINO = "/Volumes/casparcg/rundown/eleicoes/"
    DESTINO_LOCAL =  "./saidas/tarjas/"
    if not os.path.isdir(DESTINO):
       os.system("mkdir /Volumes/casparcg; mount -t cifs -o username=casparcg,password=casparcg //10.61.30.37/casparcg /Volumes/casparcg")
else:
    DESTINO = "/mnt/casparcg/rundown/eleicoes/"
    DESTINO_LOCAL =  "/opt/ebc.eleicoes/saidas/tarjas/"
    if not os.path.isdir(DESTINO):
        os.system("mkdir /mnt/casparcg; mount -t cifs -o username=casparcg,password=casparcg //10.61.30.37/casparcg /mnt/casparcg")

if not os.path.isdir(DESTINO_LOCAL):
    os.makedirs(DESTINO_LOCAL)


portas = ['8080', '8081', '8082', '8083']
porta = random.choice(portas)
url = "http://gcebc-prod01.ebc:%s/ebcgceleicoes/getPendentes" % porta

def baixaLista(url):
    req = requests.get(url)
    aux = req.text
    if len(aux) > 0:
        x = ast.literal_eval(aux)
        return x
    else:
        return []


def baixa_dados(aux):
    arquivo = aux[0]
    programa = aux[1]
    url = aux[2]
    req = requests.get(url + '/getEdicaoText')
    dados = req.text

    agora = datetime.datetime.now()
    agora = agora.strftime("%Y%m%d%H%M%S")

    if not os.path.exists(DESTINO):
        os.makedirs(DESTINO)

    with open(DESTINO_LOCAL + agora + arquivo, 'w') as f:
        f.write(dados)

    with open(DESTINO + '/' + arquivo, 'w') as f:
        f.write(dados)


lista_itens = baixaLista(url)
itens = []
for item in lista_itens:
    endereco = item['endereco']
    titulo = item['titulo']
    programa = endereco.split('/')
    programa = programa[4]
    data = item['data']
    id = slugify(titulo)
    arquivo =  data + '_' +  id + '.xml'
    itens.append([arquivo, programa, endereco])

pool = Pool(20)
result = pool.map(baixa_dados, itens)
