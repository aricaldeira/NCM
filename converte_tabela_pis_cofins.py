#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime


ST_PIS_TRIB_NORMAL = '01'
ST_PIS_TRIB_DIFERENCIADA = '02'
ST_PIS_TRIB_QUANTIDADE = '03'
ST_PIS_TRIB_MONOFÁSICA = '04'
ST_PIS_TRIB_SUBSTITUIÇÃO = '05'
ST_PIS_TRIB_ALÍQUOTA_ZERO = '06'
ST_PIS_ISENTA = '07'
ST_PIS_SEM_INCIDÊNCIA = '08'
ST_PIS_COM_SUSPENSÃO = '09'
ST_PIS_AQUIS_SEM_CREDITO = '70'
ST_PIS_AQUIS_ISENTA = '71'
ST_PIS_AQUIS_COM_SUSPENSAO = '72'
ST_PIS_AQUIS_ALIQUOTA_ZERO = '73'
ST_PIS_AQUIS_SEM_INCIDENCIA = '74'
ST_PIS_AQUIS_SUBSTITUICAO = '75'


ST_PIS_TRIB_DIFERENCIADA_MONOFÁSICA = '02/04'
ST_PIS_TRIB_QUANTIDADE_MONOFÁSICA = '03/04'

ARQUIVO = {
    #ST_PIS_TRIB_DIFERENCIADA_MONOFÁSICA: 'tabelas/tb379.txt',
    ST_PIS_TRIB_DIFERENCIADA_MONOFÁSICA: 'tabelas/tb415.txt', # 01/10/2012
    #ST_PIS_TRIB_QUANTIDADE_MONOFÁSICA: 'tabelas/tb380.txt',
    ST_PIS_TRIB_QUANTIDADE_MONOFÁSICA: 'tabelas/tb431.txt', # 01/10/2012
    ST_PIS_TRIB_SUBSTITUIÇÃO: 'tabelas/tb318.txt',
    #ST_PIS_TRIB_ALÍQUOTA_ZERO: 'tabelas/tb381.txt',
    ST_PIS_TRIB_ALÍQUOTA_ZERO: 'tabelas/tb414.txt', # 01/10/2012
    #ST_PIS_ISENTA: 'tabelas/tb217.txt',
    ST_PIS_ISENTA: 'tabelas/tb406.txt', # 01/10/2012
    ST_PIS_SEM_INCIDÊNCIA: 'tabelas/tb218.txt',
    #ST_PIS_COM_SUSPENSÃO: 'tabelas/tb374.txt',
    ST_PIS_COM_SUSPENSÃO: 'tabelas/tb417.txt', # 01/10/2012
    }

COLUNA_CÓDIGO = 0
COLUNA_NCM = 1
COLUNA_EX = 2
COLUNA_NCM_EXCLUÍDO = 3
COLUNA_AL_PIS = 4
COLUNA_AL_COFINS = 5

#
# COLUNAS = {
#     ST_PIS: [COLUNA_CÓDIGO, COLUNA_NCM, COLUNA_EX, COLUNA_NCM_EXCLUÍDO,
#         COLUNA_AL_PIS, COLUNA_AL_COFINS],
#
COLUNAS = {
    ST_PIS_TRIB_DIFERENCIADA_MONOFÁSICA: [0, 4, 6, 5, 7, 8],
    ST_PIS_TRIB_QUANTIDADE_MONOFÁSICA: [0, 4, 6, 5, 8, 9],
    ST_PIS_TRIB_SUBSTITUIÇÃO: [0, 4, 6, 5, 7, 8],
    ST_PIS_TRIB_ALÍQUOTA_ZERO: [0, 4, 6, 5],
    ST_PIS_ISENTA: [0, 4, 6, 5],
    ST_PIS_SEM_INCIDÊNCIA: [0, 4, 6, 5],
    ST_PIS_COM_SUSPENSÃO: [0, 4, 6, 5],
    }

#
# ANÁLISE_ST_PIS
#
class AnálisePIS(object):
    def __init__(self, st_pis_cofins=''):
        self.ncm = None
        self.código_justificativa = ''
        self.ex = ''
        self.ncm_excluído = None
        self.al_pis = ''
        self.al_cofins = ''

        if st_pis_cofins == ST_PIS_TRIB_DIFERENCIADA_MONOFÁSICA:
            st_pis_cofins = ST_PIS_TRIB_MONOFÁSICA
        elif st_pis_cofins == ST_PIS_TRIB_QUANTIDADE_MONOFÁSICA:
            st_pis_cofins = ST_PIS_TRIB_MONOFÁSICA

        self.st_pis_cofins = st_pis_cofins
        self.st_pis_cofins_entrada = ''

        #
        # Conversão das ST de saída para entrada
        #
        if st_pis_cofins == ST_PIS_TRIB_MONOFÁSICA:
            self.st_pis_cofins_entrada = ST_PIS_AQUIS_SEM_CREDITO
        elif st_pis_cofins == ST_PIS_TRIB_SUBSTITUIÇÃO:
            self.st_pis_cofins_entrada = ST_PIS_AQUIS_SUBSTITUICAO
        elif st_pis_cofins == ST_PIS_TRIB_ALÍQUOTA_ZERO:
            self.st_pis_cofins_entrada = ST_PIS_AQUIS_ALIQUOTA_ZERO
        elif st_pis_cofins == ST_PIS_ISENTA:
            self.st_pis_cofins_entrada = ST_PIS_AQUIS_ISENTA
        elif st_pis_cofins == ST_PIS_SEM_INCIDÊNCIA:
            self.st_pis_cofins_entrada = ST_PIS_AQUIS_SEM_INCIDENCIA
        elif st_pis_cofins == ST_PIS_COM_SUSPENSÃO:
            self.st_pis_cofins_entrada = ST_PIS_AQUIS_COM_SUSPENSAO


ANÁLISES_ST_PIS = []


def cria_regex_ncm(campo):
    ncms = campo.split(';')
    rex = ''

    for ncm in ncms:
        if len(ncm) < 8:
            ncm += '.*'

        ncm = '|' + ncm

        if not ncm in rex:
            rex = rex + ncm

    return re.compile(rex[1:])


def cria_regex_tabela(st_pis_cofins):
    #
    # As tabelas baixadas do site do SPED vem codificadas em ISO-8859-1
    #
    f = open(ARQUIVO[st_pis_cofins], 'r', encoding='iso8859-1')

    #
    # A primeira linha é desprezada porque contém o título das colunas
    #
    l = f.readline()
    rex_ncm = ''
    rex_ncm_excluído = ''

    for l in f.readlines():
        campos = l.split('|')
        #
        # Se houver data de vencimento da regra, ignorar
        #
        if campos[3] != '':
            data_final = datetime.date(int(campos[3][4:]), int(campos[3][2:4]), int(campos[3][0:2]))
            if data_final < datetime.date.today():
                continue

        análise = AnálisePIS(st_pis_cofins)

        #
        # Possui NCMs listados
        #
        if campos[COLUNAS[st_pis_cofins][COLUNA_NCM]] != '':
            análise.ncm = cria_regex_ncm(campos[COLUNAS[st_pis_cofins][COLUNA_NCM]])

        if campos[COLUNAS[st_pis_cofins][COLUNA_NCM_EXCLUÍDO]] != '':
            análise.ncm_excluído = cria_regex_ncm(campos[COLUNAS[st_pis_cofins][COLUNA_NCM_EXCLUÍDO]])

        if campos[COLUNAS[st_pis_cofins][COLUNA_CÓDIGO]] != '':
            análise.código_justificativa = campos[COLUNAS[st_pis_cofins][COLUNA_CÓDIGO]]

        if campos[COLUNAS[st_pis_cofins][COLUNA_EX]] != '':
            análise.ex = campos[COLUNAS[st_pis_cofins][COLUNA_EX]]

        if len(campos) <= COLUNA_AL_PIS and campos[COLUNAS[st_pis_cofins][COLUNA_AL_PIS]] != '':
            análise.al_pis = campos[COLUNAS[st_pis_cofins, AL_PIS]]

        if len(campos) <= COLUNA_AL_COFINS and campos[COLUNAS[st_pis_cofins][COLUNA_AL_COFINS]] != '':
            análise.al_cofins = campos[COLUNAS[st_pis_cofins, AL_COFINS]]

        ANÁLISES_ST_PIS.append(análise)


def cria_analises_pis_cofins():
    for st_pis_cofins in ARQUIVO.keys():
        cria_regex_tabela(st_pis_cofins)


def ncm_pertence_a_st_pis_cofins(ncm):
    for análise in ANÁLISES_ST_PIS:
        if análise.ncm is not None:
            if análise.ncm.match(ncm):
                if análise.ncm_excluído is None:
                    return análise

                elif not análise.ncm_excluído.match(ncm):
                    return análise

    return None
