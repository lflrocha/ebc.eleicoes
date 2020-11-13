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
    DESTINO_FOTOS = "/Volumes/casparcg/rundown/eleicoes/fotos/"
    DESTINO_FOTOS2 = "/Volumes/#CasparEBC/rundown/eleicoes/fotos/"
    DESTINO_LOCAL =  "./saidas/resultados/"
    if not os.path.isdir(DESTINO):
       os.system("mkdir /Volumes/casparcg; mount -t cifs -o username=casparcg,password=casparcg //10.61.30.37/casparcg /Volumes/casparcg")
else:
    DESTINO = "/mnt/casparcg/rundown/eleicoes/"
    DESTINO_FOTOS = "/mnt/casparcg/rundown/eleicoes/fotos/"
    DESTINO_LOCAL =  "/opt/ebc.eleicoes/saidas/resultados/"
    if not os.path.isdir(DESTINO):
        os.system("mkdir /mnt/casparcg; mount -t cifs -o username=casparcg,password=casparcg //10.61.30.37/casparcg /mnt/casparcg")

if not os.path.isdir(DESTINO_LOCAL):
    os.makedirs(DESTINO_LOCAL)

URL = 'https://eleicoes.ebc.com.br'
URL_FOTOS = 'http://web1-prod-eleicoes.ebc/fotos/'

portas = ['8080', '8081', '8082', '8083']
porta = random.choice(portas)
url = "http://gcebc-prod01.ebc:%s/ebcgceleicoes/resultados/getCidadesResultadosText" % porta


def geraXMLCidade(cidade):
    url = URL + "/2020/municipal/primeiro-turno/dados/prefeito/%s.json" % cidade
    req = requests.get(url)
    resultado = req.json()

    cidade = resultado['nome_cidade']
    uf = resultado['sigla_uf']
    urnas = resultado['secoes_totalizadas_percent']
    candidatos = resultado['candidatos']

    destino_fotos = DESTINO_FOTOS + uf.lower()
    if not os.path.isdir(destino_fotos):
        os.makedirs(destino_fotos)

    destino_fotos2 = DESTINO_FOTOS2 + uf.lower()
    if not os.path.isdir(destino_fotos2):
        os.makedirs(destino_fotos2)


    dados_candidatos = []
    for candidato in candidatos[:4]:
        nome = candidato['nome']
        partido = candidato['partido']
        votos = candidato['votos_total']
        votos_percentual = candidato['votos_percent']
        foto = candidato['cod_imagem']

        caminho_foto = destino_fotos + '/' + str(foto) + '.jpg'
        url_fotos = URL_FOTOS + uf + '/' + foto + '.jpg'
        url_fotos = 'https://eleicoes.ebc.com.br/fotos/AC/10000644872.jpg'
        print(url_fotos)
        if not os.path.isfile(caminho_foto):
            r = requests.get(url_fotos, allow_redirects=True)
            open(caminho_foto, 'wb').write(r.content)

        caminho_foto2 = destino_fotos2 + '/' + str(foto) + '.jpg'
        print(caminho_foto2)
        url_fotos = URL_FOTOS + uf + '/' + foto + '.jpg'
        url_fotos = 'https://eleicoes.ebc.com.br/fotos/AC/10000644872.jpg'
        print(url_fotos)
        if not os.path.isfile(caminho_foto2):
            r = requests.get(url_fotos, allow_redirects=True)
            open(caminho_foto2, 'wb').write(r.content)


        if "status" in  candidato.keys():
            status = candidato['status']
        else:
            status = ""
        dados_candidatos.append({"nome": nome, "partido": partido, "votos": votos, "votos_percentual": votos_percentual, "foto": foto, "status": status })

    urnas = urnas
    #urnas = str("%0.2f" % round(float(urnas), 2)).replace(".", ",")
    aux = ""
    aux = aux + '<item>\n'
    aux = aux + '<type>TEMPLATE</type>\n'
    aux = aux + '<devicename>Local CasparCG</devicename>\n'
    aux = aux + '<label>%s/%s - %s</label>\n' % (cidade, uf, urnas)
    aux = aux + '<name>eleicoes/eleicoes_resultado</name>\n'
    aux = aux + '<channel>1</channel>\n'
    aux = aux + '<videolayer>%s</videolayer>\n' % 90
    aux = aux + '<delay>0</delay>\n'
    aux = aux + '<duration>0</duration>\n'
    aux = aux + '<allowgpi>false</allowgpi>\n'
    aux = aux + '<allowremotetriggering>true</allowremotetriggering>\n'
    aux = aux + '<remotetriggerid></remotetriggerid>\n'
    aux = aux + '<storyid></storyid>\n'
    aux = aux + '<flashlayer>1</flashlayer>\n'
    aux = aux + '<invoke></invoke>\n'
    aux = aux + '<usestoreddata>false</usestoreddata>\n'
    aux = aux + '<useuppercasedata>false</useuppercasedata>\n'
    aux = aux + '<triggeronnext>false</triggeronnext>\n'
    aux = aux + '<sendasjson>false</sendasjson>\n'
    aux = aux + '<templatedata>\n'
    aux = aux + '<componentdata>\n'
    aux = aux + '<id>f1</id>\n'
    aux = aux + '<value>%s</value>\n' % cidade
    aux = aux + '</componentdata>\n'
    aux = aux + '<componentdata>\n'
    aux = aux + '<id>f2</id>\n'
    aux = aux + '<value>%s</value>\n' % uf
    aux = aux + '</componentdata>\n'
    aux = aux + '<componentdata>\n'
    aux = aux + '<id>f3</id>\n'
    aux = aux + '<value>%s%%</value>\n' % urnas
    aux = aux + '</componentdata>\n'

    aux = aux + '<componentdata>\n'
    aux = aux + '<id>f4</id>\n'
    aux = aux + '<value>Eleição para prefeito</value>\n'
    aux = aux + '</componentdata>\n'
    aux = aux + '<componentdata>\n'
    aux = aux + '<id>f5</id>\n'
    aux = aux + '<value>Urnas apuradas</value>\n'
    aux = aux + '</componentdata>\n'
    aux = aux + '<componentdata>\n'
    aux = aux + '<id>f6</id>\n'
    aux = aux + '<value></value>\n'
    aux = aux + '</componentdata>\n'


    for i, item in enumerate(dados_candidatos):
        index = (i + 1) * 10
        aux = aux + '<componentdata>\n'
        aux = aux + '<id>f%s</id>\n' % str(index)
        aux = aux + '<value>%s</value>\n' % item["nome"]
        aux = aux + '</componentdata>\n'
        aux = aux + '<componentdata>\n'
        aux = aux + '<id>f%s</id>\n' % str(index+1)
        aux = aux + '<value>%s</value>\n' % item["partido"]
        aux = aux + '</componentdata>\n'
        aux = aux + '<componentdata>\n'
        aux = aux + '<id>f%s</id>\n' % str(index+2)
        aux = aux + '<value>%s</value>\n' % "{:,}".format(int(item["votos"])).replace(",",".")
        aux = aux + '</componentdata>\n'
        aux = aux + '<componentdata>\n'
        aux = aux + '<id>f%s</id>\n' % str(index+3)
        aux = aux + '<value>%s%%</value>\n' % item["votos_percentual"]
        aux = aux + '</componentdata>\n'
        aux = aux + '<componentdata>\n'
        aux = aux + '<id>f%s</id>\n' % str(index+4)
        aux = aux + '<value>%s</value>\n' % item["foto"]
        aux = aux + '</componentdata>\n'
        aux = aux + '<componentdata>\n'
        aux = aux + '<id>f%s</id>\n' % str(index+5)
        aux = aux + '<value>%s</value>\n' % item["status"]
        aux = aux + '</componentdata>\n'

    aux = aux + '</templatedata>\n'
    aux = aux + '<color>rgba(63, 0, 123, 128)</color>\n'
    aux = aux + '</item>\n'

    return aux


req = requests.get(url)
aux = req.text
regioes = ast.literal_eval(aux)

aux = ""
aux = aux + '<?xml version="1.0" encoding="UTF-8"?>\n'
aux = aux + '<items>\n'
aux = aux + '<allowremotetriggering>true</allowremotetriggering>\n'

for regiao in regioes:
    aux = aux + '<item>\n'
    aux = aux + '<type>GROUP</type>\n'
    aux = aux + '<label>%s</label>\n' % (regiao)
    aux = aux + '<expanded>true</expanded>\n'
    aux = aux + '<channel>1</channel>\n'
    aux = aux + '<videolayer>10</videolayer>\n'
    aux = aux + '<delay>0</delay>\n'
    aux = aux + '<duration>0</duration>\n'
    aux = aux + '<allowgpi>false</allowgpi>\n'
    aux = aux + '<allowremotetriggering>true</allowremotetriggering>\n'
    aux = aux + '<remotetriggerid></remotetriggerid>\n'
    aux = aux + '<storyid></storyid>\n'
    aux = aux + '<notes></notes>\n'
    aux = aux + '<autostep>false</autostep>\n'
    aux = aux + '<autoplay>false</autoplay>\n'
    aux = aux + '<items>\n'

    cidades = regioes[regiao]
    for cidade in cidades:
        xml = geraXMLCidade(cidade)
        aux = aux + str(xml)
    aux = aux + '</items>\n'
    aux = aux + '</item>\n'

aux = aux + '</items>\n'

agora = datetime.datetime.now()
agora = agora.strftime("%Y%m%d%H%M%S")

with open(DESTINO_LOCAL + agora + '-resultados.xml', 'w') as f:
    f.write(aux)

with open(DESTINO + 'resultados.xml', 'w') as f:
    f.write(aux)



#
#
# itens = []
# for item in lista_itens:
#     endereco = item['endereco']
#     titulo = item['titulo']
#     programa = endereco.split('/')
#     programa = programa[4]
#     data = item['data']
#     id = slugify(titulo)
#     arquivo = destino + programa + '/' + data + '_' +  id + '.xml'
#     if not os.path.exists(destino + programa):
#         os.makedirs(destino + programa)
#     itens.append([arquivo, endereco])
#
# pool = Pool(20)
# result = pool.map(baixa_dados, itens)
