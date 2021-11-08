# -*- coding: utf-8 -*-

import sqlite3
import csv

DB = 'Wybory.db'
TABLES = {
    'OKRĘGI': {
       'NUMER'           :       'INT PRIMARY KEY',
       'SIEDZIBA'        :       'TEXT NOT NULL',
       'MANDATY'         :       'INT NOT NULL',
       'LICZBA_WYBORCÓW' :       'INT NOT NULL'
             },
    'KOMITETY' :{
        'NUMER'          :       'INT PRIMARY KEY',
        'NAZWA'          :       'TEXT NOT NULL'
            },
    'WYNIKI' :{
        'NR_KOMITETU'    :       'INT  references  KOMITETY',
        'NR_OKRĘGU'      :       'INT references OKRĘGI',
        'LICZBA_GŁOSÓW'  :       'INT NOT NULL',
        'primary key'    :       '(NR_KOMITETU, NR_OKRĘGU)'
            }
    }
    

def create_db(db):
    c = db.cursor()    
    for table, ddl in TABLES.items():
        coldefs = ','.join(' '.join(col) for col in sorted(ddl.items()))
        sql = 'create table {} ({})'.format(table, coldefs)
        c.execute('drop table if exists {}'.format(table))
        c.execute(sql)

def get_rows():
    with open('2015-gl-lis-okr.csv', encoding = 'utf-8') as f:
        reader = csv.reader(f, delimiter=',') 
        line = f.readline().split(',')
        to_komitety = []
        to_okregi = []
        to_wyniki = []   
        for i in range(5,7):
            to_komitety.append([line[i].split('\n')[0], i-6])
        for i in range(7, 24):
            to_komitety.append([line[i].split('-')[1].split('\n')[0], line[i].split('-')[0]])
        for row in reader:  
            to_okregi.append([int(row[4]), int(row[2]), int(row[0]), row[1]])
            for i in range(5, 7):
                to_wyniki.append([row[i], i-6, row[0]])
            for i in range(7, 24):
                if row[i] != '':
                    to_wyniki.append([row[i], line[i].split('-')[0], row[0]])
        return  to_komitety, to_okregi, to_wyniki
    
def fill_table(db,table, rows):
    c = db.cursor()
    ddl = TABLES[table]
    ddl = {name:dfn for name, dfn in ddl.items() if not name.lower().startswith('primary ')}
    sql = ('insert into {} ({}) values ({})'.format(table, ",".join(sorted(ddl.keys())), ",".join(["?"] * len(ddl))))
    c.executemany(sql, rows)
    
def check(db, table):
    c = db.cursor()
    c.execute('select count(*) from {}'.format(table))
    n, = c.fetchone()
    return n

if __name__ == '__main__':
    with sqlite3.connect(DB, isolation_level = None) as db:
        create_db(db)
        i = 0
        for table in sorted(TABLES):
            fill_table(db, table, get_rows()[i])
            i += 1
        for table in TABLES:
            n = check(db, table)
            print('Do tabeli {} zostało wstawionych {} wierszy.'.format(table, n))

