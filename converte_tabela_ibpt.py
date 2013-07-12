#!/usr/bin/env python
# -*- coding: utf-8 -*-

IBPT_NCM = {}
IBPT_NBS = {}
IBPT_SERVIÇO = {}


class IBPTax(object):
    def __init__(self, código='', ex='', al_nacional='0', al_internacional='0'):
        self.código = código
        self.ex = ex
        self.al_nacional = al_nacional
        self.al_internacional = al_internacional
        self.extras = {}


def cria_análises_ibpt():
    f = open('tabelas/IBPTax.0.0.2.csv', 'r', encoding='iso8859-1')

    #
    # A primeira linha é desprezada porque contém o título das colunas
    #
    l = f.readline()

    for l in f.readlines():
        campos = l.split(';')
        tipo = campos[2]

        ibpt = IBPTax(campos[0], campos[1], campos[4], campos[5])

        # NCM
        if tipo == '0':
            if ibpt.código not in IBPT_NCM:
                IBPT_NCM[ibpt.código] = ibpt
                IBPT_NCM[ibpt.código].extras[ibpt.ex] = ibpt
            else:
                if ibpt.ex not in IBPT_NCM[ibpt.código].extras:
                    IBPT_NCM[ibpt.código].extras[ibpt.ex] = ibpt

        elif tipo == '1':
            if ibpt.código not in IBPT_NBS:
                IBPT_NBS[ibpt.código] = ibpt
            else:
                print('repetido', l)

        elif tipo == '2':
            if ibpt.código not in IBPT_SERVIÇO:
                IBPT_SERVIÇO[ibpt.código] = ibpt
            else:
                print('repetido', l)


def ibpt_para_ncm(ncm, ex):
    if ncm not in IBPT_NCM:
        return IBPTax(código=ncm)

    ibpt = IBPT_NCM[ncm]
    if ex in ibpt.extras:
        return ibpt.extras[ex]
    else:
        return ibpt

def ibpt_para_nbs(nbs):
    if nbs not in IBPT_NBS:
        return IBPTax(código=nbs)
    else:
        return IBPT_NBS[nbs]

def ibpt_para_serviço(serviço):
    if serviço not in IBPT_SERVIÇO:
        return IBPTax(código=serviço)
    else:
        return IBPT_SERVIÇO[serviço]