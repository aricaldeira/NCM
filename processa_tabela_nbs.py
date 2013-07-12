#!/usr/bin/env python

import re
from converte_tabela_ibpt import cria_análises_ibpt, ibpt_para_nbs

CÓDIGO_NBS = re.compile(r'^1\.[0-9]{4}\.[0-9]{2}\.[0-9]{2}')
DESCRIÇÃO = ['', '', '']

def põe_descrição(texto):
    texto = texto.strip()
    if len(texto) and (texto[0].upper() == texto[0]):
        DESCRIÇÃO.pop(0)
        DESCRIÇÃO.pop(0)
        DESCRIÇÃO.pop(0)
        DESCRIÇÃO.append('')
        DESCRIÇÃO.append('')
        DESCRIÇÃO.append(texto)

    else:
        DESCRIÇÃO.pop(0)
        DESCRIÇÃO.append(texto)
    #print(texto, DESCRIÇÃO)

def _descrição():
    ret = ' '.join(DESCRIÇÃO).strip().replace('  ', ' ')
    DESCRIÇÃO.pop(0)
    DESCRIÇÃO.pop(0)
    DESCRIÇÃO.pop(0)
    DESCRIÇÃO.append('')
    DESCRIÇÃO.append('')
    DESCRIÇÃO.append('')
    return ret


if __name__ == '__main__':

    cria_análises_ibpt()
    arq = open('tabelas/nbs.txt', 'r', encoding='utf-8')

    print('"NBS"|"DESCRIÇÃO"|"AL_IBPT_NACIONAL"|"AL_IBPT_INTERNACIONAL"')

    #
    # Guarda 3 linhas para a DESCRIÇÃO
    #
    código_anterior = ''
    código = ''
    terceira_linha = False
    for linha in arq.readlines():
        linha = linha.strip()

        if terceira_linha:
            põe_descrição(linha)
            terceira_linha = False
            ibpt = ibpt_para_nbs(código)
            print('"%s"|"%s"|%s|%s' % (código, _descrição(), ibpt.al_nacional, ibpt.al_internacional))

        if CÓDIGO_NBS.search(linha):
            código = linha[0:12].replace('.', '')
            desc = linha[12:].strip()
            põe_descrição(desc)
            ibpt = ibpt_para_nbs(código)

            if desc == '' or desc[0].lower() == desc[0]:
                terceira_linha = True
            else:
                print('"%s"|"%s"|%s|%s' % (código, _descrição(), ibpt.al_nacional, ibpt.al_internacional))

        else:
            põe_descrição(linha)

    #print('"%s"|"%s"' % (código_anterior, _descrição()))
    arq.close()
