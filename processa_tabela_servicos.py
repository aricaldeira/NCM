#!/usr/bin/env python

import re
from converte_tabela_ibpt import cria_análises_ibpt, ibpt_para_serviço

if __name__ == '__main__':

    cria_análises_ibpt()
    arq = open('tabelas/servicos.txt', 'r', encoding='utf-8')

    #
    # A primeira linha é desprezada porque contém o título das colunas
    #
    l = arq.readline()

    print('"CODIGO"|"DESCRIÇÃO"|"AL_IBPT_NACIONAL"|"AL_IBPT_INTERNACIONAL"')

    for linha in arq.readlines():
        linha = linha.strip()
        campos = linha.split('|')

        código = campos[0]
        descrição = campos[1]
        ibpt = ibpt_para_serviço(código)
        print('"%s"|"%s"|%s|%s' % (código, descrição, ibpt.al_nacional, ibpt.al_internacional))

    arq.close()
