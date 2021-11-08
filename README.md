# sql-project
Creation of database and code for mandates distribution between electoral districts (Code written as final project for Database Technology class)

The project consists of 3 files:

- import.py – creates sqlite3 database and fills it with data from a given file.

- przydzialy.py – contains functions calculating the distribution of mandates between
electoral districts committees based on election results. Creates an extra table in the
database and fills it with appropriate data.

- raport.py – creates formatted table with election results. Based on chosen starting
parameters it can also show election summary: percent of votes for each committee
and results of mandate distribution.
