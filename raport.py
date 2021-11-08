# -*- coding: utf-8 -*-

import sqlite3

def tabelka(dane):
        napisy = []
        fmtstring = "| {:5s} | {:20s} | {:70s} | {:10s} | {:10s} |".format("NUMER", "SIEDZIBA", "NAZWA", "DH_MANDATY", "HN_MANDATY")
        napisy.append('')
        napisy.append(fmtstring)
        napisy.append('-'*131)
        for i in dane:
                    fmtstring = "| {:5.0f} | {:20s} | {:70s} | {:10.0f} | {:10.0f} |".format(i[0], i[1], i[2], i[3], i[4]) 
                    napisy.append(fmtstring)
        napisy.append('-'*131)
        return napisy

def podsumowanie(dane,dane1):
        suma = 0
        napisy = []
        for i in range(len(dane)):
            suma += dane[i][0]
        for i in range(len(dane1)):
             napisy.append("Partia {} uzyskala {:.2f}% głosów w skali kraju. Mandaty uzyskane metodą D'Hondta: {}, mandaty uzyskane metodą Hare’a-Niemeyera: {}".format(dane[i][1],(dane[i][0]/suma)*100,dane1[i][1],dane1[i][2]))
        return napisy

if __name__ == '__main__':

    DB = 'Wybory.db'
    with sqlite3.connect(DB, isolation_level = None) as db:
            c = db.cursor()
            c.execute(''' select o.NUMER, o.SIEDZIBA, k.NAZWA, p.DH_MANDATY, p.HN_MANDATY FROM OKRĘGI o, KOMITETY k JOIN PRZYDZIAŁY p ON k.NUMER = p.NR_KOMITETU AND o.NUMER = p.NR_OKRĘGU;''' )
            dane = c.fetchall()
            c.execute('''select sum(w.LICZBA_GŁOSÓW), k.NAZWA FROM WYNIKI w JOIN KOMITETY k ON k.NUMER = w.NR_KOMITETU where w.NR_KOMITETU > 0 GROUP BY k.NUMER;''')
            dane1 = c.fetchall()
            c.execute(''' select k.NAZWA, sum(p.DH_MANDATY), sum(p.HN_MANDATY) from KOMITETY k join PRZYDZIAŁY p on k.NUMER = p.NR_KOMITETU group by k.NUMER''')
            dane2 = c.fetchall()
    from sys import argv
    if len(argv) == 1:
        tab = tabelka(dane)
        for i in range(len(tab)):
            print(tab[i])
    elif argv[1] == 'podsumowanie':
        pod = podsumowanie(dane1,dane2)
        for i in range(len(pod)):
            print(pod[i])



