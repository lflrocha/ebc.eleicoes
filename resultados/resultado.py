#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from slugify import slugify
import codecs
import json
import os
import requests
from multiprocessing.dummy import Pool
from cidades import cidades

def gera_resultado(itens):

    cidade = itens[0]
    subtitulo = itens[1]
    urnas = itens[2]
    candidatos = itens[3]

    pasta_saida = itens[4]
    arquivo_saida = itens[5]

    w = 1920
    h = 1080
    base = Image.new('RGBA', (w, h), (255,255,255,0))
    baseImg = ImageDraw.Draw(base)

    fonte_cidade = ImageFont.truetype('fonts/OpenSansCondensed-Bold.ttf', 50)
    fonte_subtitulo = ImageFont.truetype('fonts/OpenSans-Regular.ttf', 40)
    fonte_urnas = ImageFont.truetype('fonts/OpenSans-Italic.ttf', 40)

    fonte_nome = ImageFont.truetype('fonts/OpenSansCondensed-Bold.ttf', 30)
    fonte_partido = ImageFont.truetype('fonts/OpenSans-Regular.ttf', 25)
    fonte_percentual = ImageFont.truetype('fonts/OpenSans-Bold.ttf', 46)
    fonte_votos = ImageFont.truetype('fonts/OpenSans-Regular.ttf', 25)
    fonte_status = ImageFont.truetype('fonts/OpenSans-Bold.ttf', 45)

    cor_textos = "#ffffff"
    cor_borda = "#FFD007"
    cor_eleito = "#0f8225"
    cor_normal = "#2c4854"

    bg = Image.open('./assets/bg.png').convert('RGBA')
    base.paste(bg, (0, 0), mask=bg)

    tamanho = baseImg.textsize(cidade.strip(), font=fonte_cidade)
    linha1X = 960 - (tamanho[0] / 2 )
    linha1Y = 90
    baseImg.text((linha1X, linha1Y), cidade.strip(), font=fonte_cidade, fill=cor_textos)

    tamanho = baseImg.textsize(subtitulo.strip(), font=fonte_subtitulo)
    linha1X = 960 - (tamanho[0] / 2 )
    linha1Y = 150
    baseImg.text((linha1X, linha1Y), subtitulo.strip(), font=fonte_subtitulo, fill=cor_textos)

    urnas = urnas + '%'
    tamanho = baseImg.textsize(urnas.strip(), font=fonte_urnas)
    linha1X = 1536 - (tamanho[0] )
    linha1Y = 145
    baseImg.text((linha1X, linha1Y), urnas.strip(), font=fonte_urnas, fill=cor_textos)

    numero = len(candidatos)
    largura = (numero - 1) * 10 + numero * 300

    base_X = int((1920 - largura) / 2)
    base_Y = 375


    for i, candidato in enumerate(candidatos):
        nome = candidato[0]
        partido = candidato[1]
        percent = candidato[2]
        votos = f"{int(candidato[3]):,}".replace(',','.')
        status = candidato[4]
        foto = candidato[5]

        if status == "":
            cor = cor_normal
        else:
            cor = cor_eleito

        linha1X = base_X + (i * 310)
        baseImg.rectangle( [(linha1X, base_Y), (linha1X + 300, base_Y + 500)], fill=cor)
        baseImg.rectangle( [(linha1X + 42, base_Y + 100), (linha1X + 42 + 216, base_Y + 100 + 300)], fill=cor_borda)

        foto = Image.open('./fotos/' + foto + '.jpg').convert('RGBA')
        foto = foto.resize((202, 290), Image.ANTIALIAS)
        base.paste(foto, (linha1X + 50 ,base_Y + 108), mask=foto)

        if status != "":
            baseImg.rectangle( [(linha1X, 880), (linha1X + 300, 880 + 75)], fill=cor)

            status = status.upper()
            tamanho = baseImg.textsize(status.strip(), font=fonte_status)
            nome_X = (300 - tamanho[0]) / 2 + linha1X
            baseImg.text((nome_X, 885), status.strip(), font=fonte_status, fill=cor_textos)


        nome = nome[:17].upper()

        tamanho = baseImg.textsize(nome.strip(), font=fonte_nome)
        nome_X = (300 - tamanho[0]) / 2 + linha1X
        baseImg.text((nome_X, 390), nome.strip(), font=fonte_nome, fill=cor_textos)

        tamanho = baseImg.textsize(partido.strip(), font=fonte_partido)
        nome_X = (300 - tamanho[0]) / 2 + linha1X
        baseImg.text((nome_X, 430), partido.strip(), font=fonte_partido, fill=cor_textos)

        tamanho = baseImg.textsize(percent.strip(), font=fonte_percentual)
        nome_X = (300 - tamanho[0]) / 2 + linha1X
        baseImg.text((nome_X, 778), percent.strip(), font=fonte_percentual, fill=cor_textos)

        tamanho = baseImg.textsize(votos.strip(), font=fonte_votos)
        nome_X = (300 - tamanho[0]) / 2 + linha1X
        baseImg.text((nome_X, 833), votos.strip(), font=fonte_votos, fill=cor_textos)


    if not os.path.isdir(pasta_saida):
        os.makedirs(pasta_saida)

    caminho_saida = pasta_saida + arquivo_saida + '.png'
    base.save(caminho_saida)
    #base.show()



def main():


    inicio = datetime.now()


    itens = []
    for cidade in cidades:
        url = "https://eleicoes.ebc.com.br/dev/2020/municipal/primeiro-turno/dados/prefeito/%s.json" % cidade
        req = requests.get(url)
        resultado = req.json()

        cidade = resultado['nome_cidade'] + '-' + resultado['sigla_uf']
        subtitulo = "Prefeito"
        urnas = resultado['secoes_totalizadas_percent']
        candidatos = resultado['candidatos']
        cands = []
        for candidato in candidatos:
            destinacao = candidato['destinacao_voto']
            if destinacao == 'Válido':
                nome = candidato['nome_gc']
                partido = candidato['partido']
                percent = candidato['votos_percent'] + '%'
                votos = candidato['votos_total']
                status = candidato['status']
                foto = resultado['sigla_uf'] + '/' + candidato['cod_imagem']
                foto = 'AC' + '/' + '10000644872'
                cands.append([nome, partido, percent, votos, status, foto])
        cands = cands[:4]

        arq_urnas = urnas.split(',')
        if len(arq_urnas) > 1:
            arq_urnas = arq_urnas[0]
        else:
            arq_urnas = arq_urnas[0]
        arq_urnas = arq_urnas.zfill(3)

        data = datetime.now()
        data = data.strftime("%y%m%d-%H%M%S")

        arquivo = arq_urnas + '_' + data + '_' + cidade.replace(' ', '-').replace('---', '-')
        arquivo = slugify(arquivo)
        pasta_saida = './saida/' + resultado['sigla_uf'].lower() + '/' + slugify(resultado['nome_cidade']) + '/'
        itens.append([cidade, subtitulo, urnas, cands, pasta_saida, arquivo])

    pool = Pool(20)
    result = pool.map(gera_resultado, itens)

    fim = datetime.now()
    print(fim-inicio)


if __name__ == "__main__":
    main()