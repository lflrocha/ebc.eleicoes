#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import requests
import datetime
import time
import socket
from slugify import slugify
import pickle


TCP_IP = '10.61.172.140'
#TCP_IP = '10.61.6.34'
TCP_PORT = 5250
BUFFER_SIZE = 4096
MESSAGE = ""


def main():

    devel = False
    if devel:
        DESTINO_LOCAL = "./saidas/foguetes/"
    else:
        DESTINO_LOCAL = "/opt/ebc.eleicoes/saidas/foguetes/"

    if not os.path.isdir(DESTINO_LOCAL):
        os.makedirs(DESTINO_LOCAL)

    req = requests.get('https://eleicoes.ebc.com.br/2020/municipal/primeiro-turno/complemento/prefeito/eventos_capitais.json')
#    req = requests.get('https://eleicoes.ebc.com.br/dev/2020/municipal/primeiro-turno/complemento/prefeito/eventos_capitais.json')
    dados = req.json()

    for cidade in dados:
        agora = datetime.datetime.now()
        agora = agora.strftime("%Y%m%d%H%M%S")

        with open(DESTINO_LOCAL + agora + "-foguetes.txt", 'w') as f:
            f.write(req.text)

        if os.path.isfile('cidades_apresentadas.p'):
            with open ('cidades_apresentadas.p', 'rb') as fp:
                cidades_apresentadas = pickle.load(fp)
        else:
            cidades_apresentadas = []

        cod = cidade['codigo_abrangencia']
        if cod not in cidades_apresentadas:
            nome_cidade =  cidade['abrangencia']
            status = cidade['tipo_evento']
            aux = cidade['descricao']
            nome = aux.split(': ', 1)
            nome = nome[1].split(' (')[0]
            print(status)

            if status != "Haverá Segundo Turno.":
                if status == "Eleito" or status == "Eleita":
                    linha = 'CG 1-100 ADD 1 \"eleicoes/ELEICOES_TARJA_FOGUETE_ELEITO\" 1 '
                    linha = linha + '\"<templateData>'
                    linha = linha + '<componentData id=\\"f0\\">'
                    linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % nome_cidade
                    linha = linha + '</componentData>'
                    linha = linha + '<componentData id=\\"f1\\">'
                    linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % nome
                    linha = linha + '</componentData>'
                    linha = linha + '</templateData>\" \r\n'
                else:
                    nome2 = aux.split('enfrentará ')
                    nome2 = nome2[1].split(' (')[0]
                    linha = 'CG 1-100 ADD 1 \"eleicoes/ELEICOES_TARJA_FOGUETE_2TURNO\" 1 '
                    linha = linha + '\"<templateData>'
                    linha = linha + '<componentData id=\\"f0\\">'
                    linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % nome_cidade
                    linha = linha + '</componentData>'
                    linha = linha + '<componentData id=\\"f1\\">'
                    linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % nome
                    linha = linha + '</componentData>'
                    linha = linha + '<componentData id=\\"f2\\">'
                    linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % nome2
                    linha = linha + '</componentData>'
                    linha = linha + '</templateData>\" \r\n'

                print(linha)
                with open(DESTINO_LOCAL + agora + "-comandos.txt", 'w') as f:
                    f.write(linha)

                # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # s.connect((TCP_IP, TCP_PORT))
                # print(s)
                # s.send(linha.encode())
                # print(s)
                # data = s.recv(BUFFER_SIZE)
                # s.close()
                # time.sleep(300)
                cidades_apresentadas.append(cod)
                with open('cidades_apresentadas.p', 'wb') as fp:
                    pickle.dump(cidades_apresentadas, fp)


if __name__ == "__main__":
    main()
