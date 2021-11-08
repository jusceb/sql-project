# -*- coding: utf-8 -*-

import sqlite3
import collections
import numpy as np

def dh(mandaty, listy, glosy, gl_w, wszystkie):
    prog1 = 0.05 * wszystkie
    prog2 = 0.08 * wszystkie
    man = dict()
    listy_d =[]
    glosy_d = []
    for i in range(len(gl_w)):
        if listy[i] != 6 and listy[i] != 16:
            if gl_w[i] >= prog1:
                listy_d.append(listy[i])
                glosy_d.append(glosy[i])
        if listy[i] == 6:
            if gl_w[i] >= prog2:
                listy_d.append(listy[i])
                glosy_d.append(glosy[i])
        if listy[i] == 16:
                listy_d.append(listy[i])
                glosy_d.append(glosy[i])
    for j in range(1, mandaty + 1):
        for i in range(len(glosy_d)):
             man[glosy_d[i] / j] = listy_d[i]            
    sorted_man = sorted(man.items(), key=lambda kv: kv[0], reverse = True)
    wynik = sorted_man[:mandaty]
    lis = []
    for i in wynik:
        lis.append(i[1])
    w = collections.Counter(lis)
    lista = []
    mand = []
    for i in w.keys():
        lista.append(i)
    for i in w.values():
        mand.append(i)
    return lista, mand

def hn(glosy, mandaty, wszystkie):
    wyniki = []
    reszta = []
    for i in range(len(glosy)):
        wyniki.append(int((glosy[i] * mandaty) / wszystkie))
        reszta.append(((glosy[i] * mandaty) / wszystkie) - (int((glosy[i] * mandaty) / wszystkie)))
    while sum(wyniki) < mandaty:
        for i in range(len(reszta)):
            naj = max(reszta)
            if reszta[i] == naj:
                reszta[i] = 0
                wyniki[i] += 1
    return wyniki

def get_data(c):
        c.execute('''select LICZBA_GŁOSÓW from wyniki where NR_KOMITETU = 0''')
        wszystkie_okreg = []
        for i in c.fetchall():
            wszystkie_okreg.append(list(i)[0])
        wszystkie = sum(wszystkie_okreg)
        c.execute(''' select SUM(w.LICZBA_GŁOSÓW) from WYNIKI w  WHERE NR_KOMITETU > 0 group by NR_KOMITETU; ''')
        wszystkie_partia = []
        for i in c.fetchall():
            wszystkie_partia.append(list(i)[0])
        wyniki_dh1 = []
        wyniki_hn1 = []
        for i in range(1,len(wszystkie_okreg) + 1):
            c.execute('''select w.LICZBA_GŁOSÓW, w.NR_KOMITETU, w.NR_OKRĘGU, o.MANDATY from WYNIKI w join OKRĘGI o 
                      on o.NUMER = w.NR_OKRĘGU where NR_OKRĘGU = {} and NR_KOMITETU > 0 group by NR_KOMITETU'''.format(i))
            dane = c.fetchall()
            mandaty = list(dane)[0][-1]
            listy = []
            glosy = []
            for j in dane:
                 listy.append(list(j)[1])
                 glosy.append(list(j)[0])
            wszystkie_partie_wazne = []
            for j in listy:
                    wszystkie_partie_wazne.append(wszystkie_partia[j-1])
            wyn_hn = hn(glosy, mandaty, wszystkie_okreg[i-1])
            wyn_dh,komit = dh(mandaty, listy, glosy,wszystkie_partie_wazne, wszystkie) 
            wyniki_hn = list(np.zeros(len(wszystkie_partia)))
            wyniki_dh = list(np.zeros(len(wszystkie_partia)))
            for j in range(len(wyniki_dh)):
                for jj in range(len(wyn_dh)):
                    if wyn_dh[jj] == j + 1:
                        wyniki_dh[j] = komit[jj]
            wyniki_dh1.append(wyniki_dh)
            for j in range(len(wyn_hn)):
                wyniki_hn[j] = wyn_hn[j]
            wyniki_hn1.append(wyniki_hn)
        return wyniki_dh1, wyniki_hn1, wszystkie_partia

def check(db, table):
    c = db.cursor()
    c.execute('select count(*) from {}'.format(table))
    n, = c.fetchone()
    return n

if __name__ == '__main__':
    DB = 'Wybory.db'
    table = '''create table if not exists PRZYDZIAŁY
            (NR_KOMITETU int references KOMITETY,
             NR_OKRĘGU int references OKRĘGI,
             DH_MANDATY int,
             HN_MANDATY int,
             primary key (NR_KOMITETU, NR_OKRĘGU));'''
     
    with sqlite3.connect(DB, isolation_level = None) as db:
        c = db.cursor()
        c.execute(table)
        wyniki_dh1, wyniki_hn1, wszystkie_partia = get_data(c)
        for i in range(len(wyniki_dh1)):
            for j in range(len(wszystkie_partia)):
                 to_przydzialy = [j+1, i+1, int(wyniki_dh1[i][j]), int(wyniki_hn1[i][j])]
                 c.executemany('''INSERT OR REPLACE into PRZYDZIAŁY values (?,?,?,?)''', (to_przydzialy,))                 
        n = check(db, 'PRZYDZIAŁY')
        print('Do tabeli {} zostało wstawionych {} wierszy.'.format('PRZYDZIAŁY',n))