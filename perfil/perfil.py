#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from slugify import slugify
import codecs
import json
import os
import requests
from multiprocessing.dummy import Pool

def gera_perfil(itens):

    titulo = itens[0]
    subtitulo = itens[1]
    cidade = itens[2]
    idade = itens[3]
    profissao = itens[4]
    perfil = itens[5]
    nome = itens[6]
    partido = itens[7]
    foto = itens[8]
    pasta_saida = itens[9]
    arquivo_saida = itens[10]


    w = 1920
    h = 1080
    base = Image.new('RGBA', (w, h), (255,255,255,0))
    baseImg = ImageDraw.Draw(base)

    fonte_titulo = ImageFont.truetype('fonts/OpenSans-Bold.ttf', 50)
    fonte_subtitulo = ImageFont.truetype('fonts/OpenSans-Regular.ttf', 38)

    fonte_cidade = ImageFont.truetype('fonts/OpenSansCondensed-Bold.ttf', 50)
    fonte_idade = ImageFont.truetype('fonts/OpenSans-Bold.ttf', 50)
    fonte_profissao = ImageFont.truetype('fonts/OpenSansCondensed-Bold.ttf', 50)

    fonte_perfil = ImageFont.truetype('fonts/OpenSansCondensed-Bold.ttf', 48)

    fonte_nome = ImageFont.truetype('fonts/OpenSansCondensed-Bold.ttf', 60)
    fonte_partido = ImageFont.truetype('fonts/OpenSansCondensed-Bold.ttf', 46)

    cor_textos = "#2c4854"

    bg = Image.open('./assets/bg.png').convert('RGBA')
    base.paste(bg, (0, 0), mask=bg)

    tamanho = baseImg.textsize(titulo.strip(), font=fonte_titulo)
    linha1X = (((1430 - 490) - tamanho[0]) / 2 ) + 490
    linha1Y = 70
    baseImg.text((linha1X, linha1Y), titulo.strip(), font=fonte_titulo, fill=cor_textos)

    tamanho = baseImg.textsize(subtitulo.strip(), font=fonte_subtitulo)
    linha1X = (((1430 - 490) - tamanho[0]) / 2 ) + 490
    linha1Y = 165
    baseImg.text((linha1X, linha1Y), subtitulo.strip(), font=fonte_subtitulo, fill=cor_textos)

    tamanho = baseImg.textsize(cidade.strip(), font=fonte_cidade)
    linha1X = 660
    linha1Y = 359
    baseImg.text((linha1X, linha1Y), cidade.strip(), font=fonte_cidade, fill=cor_textos)

    tamanho = baseImg.textsize(idade.strip(), font=fonte_idade)
    linha1X = 660
    linha1Y = 462
    baseImg.text((linha1X, linha1Y), idade.strip(), font=fonte_idade, fill=cor_textos)

    tamanho = baseImg.textsize(profissao.strip(), font=fonte_profissao)
    linha1X = 660
    linha1Y = 565
    baseImg.text((linha1X, linha1Y), profissao.strip(), font=fonte_profissao, fill=cor_textos)

    tamanho = baseImg.textsize(nome.strip(), font=fonte_nome)
    linha1X = 600 - tamanho[0]
    linha1Y = 836
    baseImg.text((linha1X, linha1Y), nome.strip(), font=fonte_nome, fill=cor_textos)

    tamanho = baseImg.textsize(partido.strip(), font=fonte_partido)
    #linha1X = (((613 - 265) - tamanho[0]) / 2 ) + 265
    linha1X = 600 - tamanho[0]
    linha1Y = 935
    baseImg.text((linha1X, linha1Y), partido.strip(), font=fonte_partido, fill=cor_textos)

    foto = Image.open('fotos/' + foto).convert('RGBA')
    foto = foto.resize((322,450), Image.ANTIALIAS)
    base.paste(foto, (277,365), mask=foto)


    linhas = [[],[],[],[],[],[],[],[]]
    partes = perfil.split(' ')
    tamanho = 0
    linha = 0
    for parte in partes:
        tamParte = baseImg.textsize(parte + ' ', font=fonte_perfil)
        tamanho = tamanho + tamParte[0]
        if tamanho < 775:
            linhas[linha].append(parte)
        else:
            linha = linha + 1
            linhas[linha].append(parte)
            tamanho = tamParte[0]

    for i, linha in enumerate(linhas):
        texto = " ".join(linha)
        linha1X = 660
        linha1Y = 670 + (i * 50)
        baseImg.text((linha1X, linha1Y), texto.strip(), font=fonte_perfil, fill=cor_textos)

    caminho_saida = pasta_saida + arquivo_saida
    base.save(caminho_saida)
    #base.show()


def get_key(cidades, val):
    for key, value in cidades.items():
         if val == value:
             return key

    return "key doesn't exist"


def main():
    with open('./dados/dados_ebc.json') as f:
        dados = json.load(f)

    with open('./dados/busca_municipios.json') as f:
        cidades = json.load(f)

    print(len(dados))
    itens = []
    for i, dado in enumerate(dados):
        cidade = get_key(cidades, dado['cod_cidade'])
        cidade = cidade.split(' - ')[0]
        titulo = cidade + '/' + dado['cod_uf']
        subtitulo = "Candidato eleito"
        cidade_natal = dado['cidade_natal'] + '/' + dado['uf_natal']
        idade = dado['idade'] + " anos"
        profissao = dado['profissao']
        perfil = dado['perfil']
        nome = dado['nome_ebc']
        partido = dado['sigla_partido']
        foto = "/%s/%s.jpg" % (dado['cod_uf'], dado['seq_candidato'])

        pasta_saida = './saida/' + dado['cod_uf'] + '/'

        if not os.path.isdir(pasta_saida):
            os.makedirs(pasta_saida)

        arquivo_saida = "VT_" + dado['cod_uf'] + '_' + slugify(cidade.replace(' ', '-')) + '_' + slugify(nome.replace(' ', '-')) + '.png'
        arquivo_saida = arquivo_saida.upper()
        itens.append([titulo, subtitulo, cidade_natal, idade, profissao, perfil, nome, partido, foto, pasta_saida, arquivo_saida])


    pool = Pool(20)
    result = pool.map(gera_perfil, itens)

    #    gera_perfil(titulo, subtitulo, cidade, idade, profissao, perfil, nome, partido, foto, pasta_saida, arquivo_saida)


if __name__ == "__main__":
    main()
