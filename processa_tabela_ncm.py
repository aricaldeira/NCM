#!/usr/bin/env python

import re
from converte_tabela_pis_cofins import cria_analises_pis_cofins, ncm_pertence_a_st_pis_cofins


grupo = {
    1: '',
    2: '',
    3: '',
    4: '',
    5: '',
    6: '',
    7: '',
    }

código = {
    1: '',
    2: '',
    3: '',
    4: '',
    5: '',
    6: '',
    7: '',
    }


def processa_grupo(ncm, descrição):
    t = len(ncm)

    if t < 8:
        grupo[t] = descrição
        código[t] = ncm

        t += 1
        while t <= 7:
            grupo[t] = ''
            código[t] = ''
            t += 1

        nome = ''
    else:
        t = 1
        nome = ''
        while t <= 7:
            if grupo[t] != '' and código[t] == ncm[:t]:
                nome += grupo[t] + ' - '
            t += 1

        nome += descrição

    return nome


def processa_linha(linha):
    campos = linha.split('|')
    ncm = campos[0].strip()
    descrição = campos[1].strip()
    al_ipi = campos[2].strip()
    ex = ''

    cst_ipi_entrada = ''
    cst_ipi_saída = ''

    if al_ipi == 'NT':
        al_ipi = '-1'
        cst_ipi_entrada = '03'
        cst_ipi_saída = '53'

    elif al_ipi == '0':
        #al_ipi = 0
        cst_ipi_entrada = '01'
        cst_ipi_saída = '51'

    elif al_ipi != '':
        #al_ipi = int(al_ipi)
        cst_ipi_entrada = '00'
        cst_ipi_saída = '50'

    ncm = ncm.replace('.', '')

    #
    # Detecta o código EX
    #
    if re.search('^Ex [0-9]{2}', descrição):
        ex = re.sub('^Ex ([0-9]{2}).*', r'\1', descrição)
        descrição = re.sub('^Ex [0-9]{2}', '', descrição)
        descrição = descrição.strip()

    while descrição[0] == '-':
        descrição = descrição[1:]

    while descrição[-1] == ':':
        descrição = descrição[:-1]

    while descrição[-1] == '.':
        descrição = descrição[:-1]

    descrição = descrição.strip()
    processa_grupo(ncm, descrição)

    if len(ncm) == 8:
        descrição = processa_grupo(ncm, descrição)
        análise_pis_cofins = ncm_pertence_a_st_pis_cofins(ncm)

        código_pis_cofins = ''
        cst_pis_cofins_saída = ''
        cst_pis_cofins_entrada = ''

        if análise_pis_cofins is not None:
            código_pis_cofins = análise_pis_cofins.código_justificativa
            cst_pis_cofins_saída = análise_pis_cofins.st_pis_cofins
            cst_pis_cofins_entrada = análise_pis_cofins.st_pis_cofins_entrada

        print('"%s"|"%s"|"%s"|%s|"%s"|"%s"|"%s"|"%s"|"%s"' % (ncm, ex, descrição, al_ipi, cst_ipi_entrada, cst_ipi_saída, cst_pis_cofins_entrada, cst_pis_cofins_saída, código_pis_cofins))
        return ncm


if __name__ == '__main__':

    cria_analises_pis_cofins()
    arq = open('tabelas/tabela_ncm_ipi.txt', 'r', encoding='utf-8')

    print('"NCM"|"EX"|"DESCRIÇÃO"|"AL_IPI"|"CST_IPI_ENTRADA"|"CST_IPI_SAÍDA"|"CST_PIS_COFINS_ENTRADA"|"CST_PIS_COFINS_SAÍDA"|"CÓDIGO_JUSTIFICATIVA_ENQUADRAMENTO_PIS_COFINS"')
    for linha in arq.readlines():
        #
        # Corrige alguns caracteres nas descrições
        #
        linha = linha.replace('\n', '').replace('\t', '').replace(' ', '')
        linha = linha.replace('– ', '')
        linha = re.sub('([0-9¾½])"', r'\1″', linha)
        linha = re.sub('([0-9])\'', r'\1′', linha)
        linha = re.sub('N\'', r'N′', linha)
        linha = re.sub('\'', r'’', linha)
        linha = re.sub('"([a-zA-Zé])', r'“\1', linha)
        linha = re.sub('([a-zA-Zé])"', r'\1”', linha)
        linha = re.sub('([0-9])([a-zA-Z])', r'\1 \2', linha)
        linha = re.sub('([0-9])ºC', r'\1°C', linha)
        linha = re.sub('([0-9])º', r'\1°', linha)

        while '  ' in linha:
            linha = linha.replace('  ', ' ')

        if linha[0].isdigit():
            ncm = processa_linha(linha)

        elif 'EX' in linha.upper():
            processa_linha(ncm + linha.replace('Ex0', 'Ex 0'))