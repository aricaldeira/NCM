#!/usr/bin/env python

import re
from converte_tabela_pis_cofins import cria_análises_pis_cofins, ncm_pertence_a_st_pis_cofins
from converte_tabela_ibpt import cria_análises_ibpt, ibpt_para_ncm

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
    al_pis = ''
    al_cofins = ''
    unidade = ''
    al_ibpt_nacional = '0'
    al_ibpt_internacional = '0'

    if al_ipi == 'NT' or al_ipi == '':
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
        análise_pis_cofins = ncm_pertence_a_st_pis_cofins(ncm, ex)
        ibpt = ibpt_para_ncm(ncm, ex)

        código_pis_cofins = ''
        cst_pis_cofins_saída = '01'
        cst_pis_cofins_entrada = '50'

        if análise_pis_cofins is not None:
            código_pis_cofins = análise_pis_cofins.código_justificativa
            cst_pis_cofins_saída = análise_pis_cofins.st_pis_cofins
            cst_pis_cofins_entrada = análise_pis_cofins.st_pis_cofins_entrada
            al_pis = análise_pis_cofins.al_pis
            al_cofins = análise_pis_cofins.al_cofins
            unidade = análise_pis_cofins.unidade

        if ibpt is not None:
            al_ibpt_nacional = ibpt.al_nacional
            al_ibpt_internacional = ibpt.al_internacional

        print('"%s"|"%s"|"%s"|%s|"%s"|"%s"|"%s"|"%s"|"%s"|%s|%s|"%s"|%s|%s' % (ncm, ex, descrição, al_ipi, cst_ipi_entrada, cst_ipi_saída, cst_pis_cofins_entrada, cst_pis_cofins_saída, código_pis_cofins, al_pis, al_cofins, unidade, al_ibpt_nacional, al_ibpt_internacional))
        return ncm


if __name__ == '__main__':

    cria_análises_pis_cofins()
    cria_análises_ibpt()
    arq = open('tabelas/tabela_ncm_ipi.txt', 'r', encoding='utf-8')

    print('"NCM"|"EX"|"DESCRIÇÃO"|"AL_IPI"|"CST_IPI_ENTRADA"|"CST_IPI_SAÍDA"|"CST_PIS_COFINS_ENTRADA"|"CST_PIS_COFINS_SAÍDA"|"CÓDIGO_JUSTIFICATIVA_ENQUADRAMENTO_PIS_COFINS"|"AL_PIS"|"AL_COFINS"|"UNIDADE"|"AL_IBPT_NACIONAL"|"AL_IBPT_INTERNACIONAL"')
    for linha in arq.readlines():
        #
        # Corrige alguns caracteres nas descrições
        #
        linha = linha.replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '')
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
            #print(linha)
            ncm = processa_linha(linha)

        elif 'EX' in linha.upper():
            #print(linha)
            processa_linha(ncm + linha.replace('Ex0', 'Ex 0'))
