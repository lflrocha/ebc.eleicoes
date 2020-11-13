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
    DESTINO_LOCAL = "./saidas/crawl/"
else:
    DESTINO = "/mnt/casparcg/rundown/eleicoes/"
    DESTINO_LOCAL = "/opt/ebc.eleicoes/saidas/crawl/"

URL = 'https://eleicoes.ebc.com.br'

if not os.path.isdir(DESTINO_LOCAL):
    os.makedirs(DESTINO_LOCAL)

def main():
    req = requests.get(URL + '/2020/municipal/primeiro-turno/complemento/prefeito/capitais.json')
    dados = req.json()
    lista_ordenada = sorted(dados, key=lambda k: datetime.datetime.strptime(k['ultima_atualizacao'], "%d/%m/%Y %H:%M:%S"), reverse=True)
    cidades = []
    espacador = '   '

    for item in lista_ordenada[:10]:
        dados_cidade =  item['nome_cidade'] + '/' + item['sigla_uf']
        dados_resultado = "<b>URNAS APURADAS:</b> %s%%" % (item['secoes_totalizadas_percent'])
        dados_resultado = dados_resultado.replace("100,00", "100")
        dados_candidatos = []

        candidatos = item['candidatos']
        if 'status' in candidatos[0]:
            status0 = candidatos[0]['status']
            if status0 == "Eleito":
                dados_resultado = "Eleito"
            elif status0 == "2º turno":
                if 'status' in candidatos[1]:
                    status1 = candidatos[1]['status']
                    if status1 == "2º turno":
                        dados_resultado = "2º turno"
        saida = ""
        if dados_resultado == "Eleito":
            candidato = candidatos[0]
            saida = "<c>%s</c>%s<e>%s</e>%s"% (dados_cidade, espacador, dados_resultado, espacador)
            saida = saida + "<b>%s (%s)</b> %s%% %s" % (candidato['nome_gc'], candidato['partido'], candidato['votos_percent'], espacador)
            saida = saida + espacador
        elif dados_resultado == "2º turno":
            candidato0 = candidatos[0]
            candidato1 = candidatos[1]
            saida = "<c>%s</c>%s<e>%s</e>%s"% (dados_cidade, espacador, dados_resultado, espacador)
            saida = saida + "<b>%s (%s)</b> %s%% %s" % (candidato0['nome_gc'], candidato0['partido'], candidato0['votos_percent'], espacador)
            saida = saida + "<b>%s (%s)</b> %s%% %s" % (candidato1['nome_gc'], candidato1['partido'], candidato1['votos_percent'], espacador)
        else:
            saida = "<c>%s</c>%s%s%s"% (dados_cidade, espacador, dados_resultado, espacador)
            for candidato in candidatos[:4]:
                saida = saida + "<b>%s (%s)</b> %s%% %s" % (candidato['nome_gc'], candidato['partido'], candidato['votos_percent'], espacador)
        #cidades.append(saida.replace('<', '&lt;').replace('>','&gt;'))
        cidades.append(saida)

    txt = "\n".join(cidades)
    agora = datetime.datetime.now()
    agora = agora.strftime("%Y%m%d%H%M%S")

    with open(DESTINO_LOCAL + agora + "-crawl.txt", 'w') as f:
        f.write(txt)

    with open(DESTINO + "crawl.txt", 'w') as f:
        f.write(txt)

if __name__ == "__main__":
    main()
