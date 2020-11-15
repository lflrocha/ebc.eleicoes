#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import requests
import datetime
import time
import socket
from slugify import slugify

TCP_IP = '10.61.6.234'
TCP_PORT = 5250
BUFFER_SIZE = 4096
MESSAGE = ""

destino_fotos = "/Volumes/D/#CasparEBC/rundown/eleicoes/fotos/"

def main():
    req = requests.get('https://eleicoes.ebc.com.br/2020/municipal/primeiro-turno/complemento/prefeito/capitais.json')
    dados = req.json()

    for num_cidade, cidade in enumerate(dados):
        nome_cidade =  cidade['nome_cidade']
        sigla_uf = cidade['sigla_uf']
        urnas_apuradas = "%s%%" % (cidade['secoes_totalizadas_percent'])
        urnas_apuradas = urnas_apuradas.replace("100,00", "100")
        dados_candidatos = []
        data_hora = datetime.datetime.now()
        data_hora = data_hora.strftime("%Y%m%d%H%M%S")
        arquivo = slugify(nome_cidade + '-' + sigla_uf + '-' + data_hora)
        candidatos = cidade['candidatos']

        linha = 'CG 1-90 ADD 1 \"eleicoes/eleicoes_resultado_render\" 1 '
        linha = linha + '\"<templateData>'
        linha = linha + '<componentData id=\\"f1\\">'
        linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % nome_cidade
        linha = linha + '</componentData>'
        linha = linha + '<componentData id=\\"f2\\">'
        linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % sigla_uf
        linha = linha + '</componentData>'
        linha = linha + '<componentData id=\\"f3\\">'
        linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % urnas_apuradas
        linha = linha + '</componentData>'
        linha = linha + '<componentData id=\\"f4\\">'
        linha = linha + '<data id=\\"text\\" value=\\"Eleição para prefeito\\"/>'
        linha = linha + '</componentData>'
        linha = linha + '<componentData id=\\"f5\\">'
        linha = linha + '<data id=\\"text\\" value=\\"Urnas apuradas\\"/>'
        linha = linha + '</componentData>'
        linha = linha + '<componentData id=\\"f6\\">'
        linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % arquivo
        linha = linha + '</componentData>'
        camada = (num_cidade % 7) + 1
        print(camada)
        camada = 1
        linha = linha + '<componentData id=\\"f90\\">'
        linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % str(camada)
        linha = linha + '</componentData>'

        linha = linha + '<componentData id=\\"f91\\">'
        linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % ("20")
        linha = linha + '</componentData>'


        for index, candidato in enumerate(candidatos[:4]):

            nome = candidato['nome_gc'],

            if len(nome) > 21:
                aux = nome.rfind(' ', 1)
                nome = nome[:aux]

            partido = candidato['partido'],
            votos_percent = candidato['votos_percent']
            votos = candidato['votos_total']
            foto = candidato['cod_imagem']

            caminho_foto = destino_fotos + '/' + sigla_uf + '/' + str(foto) + '.jpg'
            url_fotos = 'http://web1-prod-eleicoes.ebc/fotos/' + sigla_uf + '/' + foto + '.jpg'
            url_fotos = 'http://web1-prod-eleicoes.ebc/2020/municipal/primeiro-turno/complemento/prefeito/fotos/' + sigla_uf.lower() + '/' + foto + '.jpg'
#            url_fotos = 'http://web1-prod-eleicoes.ebc/fotos/AC/10000644872.jpg'
            r = requests.get(url_fotos, allow_redirects=True)
            open(caminho_foto, 'wb').write(r.content)
            if not os.path.isfile(caminho_foto):
                r = requests.get(url_fotos, allow_redirects=True)
                open(caminho_foto, 'wb').write(r.content)
            else:
                print("ja existe")

            status = ""
            if 'status' in candidato.keys():
                status = candidato['status']

            linha = linha + '<componentData id=\\"f%s0\\">' % str(index + 1)
            linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % nome
            linha = linha + '</componentData>'
            linha = linha + '<componentData id=\\"f%s1\\">' % str(index + 1)
            linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % partido
            linha = linha + '</componentData>'
            linha = linha + '<componentData id=\\"f%s2\\">' % str(index + 1)
            linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % votos
            linha = linha + '</componentData>'
            linha = linha + '<componentData id=\\"f%s3\\">' % str(index + 1)
            linha = linha + '<data id=\\"text\\" value=\\"%s%%\\"/>' % votos_percent
            linha = linha + '</componentData>'
            linha = linha + '<componentData id=\\"f%s4\\">' % str(index + 1)
            linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % foto
            linha = linha + '</componentData>'
            linha = linha + '<componentData id=\\"f%s5\\">' % str(index + 1)
            linha = linha + '<data id=\\"text\\" value=\\"%s\\"/>' % status
            linha = linha + '</componentData>'

        linha = linha + '</templateData>\"\r\n'

        print(linha)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        print(s)
        s.send(linha.encode())
        print(s)
        data = s.recv(BUFFER_SIZE)
        print(data)
        s.close()
        time.sleep(10)


if __name__ == "__main__":
    main()
