import sys
import os
import re 
import sqlite3
#from gbfviewer import listaArchivos
from functionsorganism import *
from functionsprotein import protsearch
from functionscomments import getextcomments
#filelist=listaArchivos

def verifarchivoaimportar():
    a= sys.argv
    if len(a)<3:
         raise Exception('database or gff is missing')
    else:
        if a[1][0:3]=='db=':
            database=a[1].split('=')[1]
            if database[len(database)-2:len(database)]=='db':
                pass
            else:
                raise Exception('database is null')
        else:
            raise Exception('specify the db= in the first input')
        if a[2][0:5]=='gbff=':
            gbff=a[2].split('=')[1]
            if gbff[len(gbff)-4:len(gbff)]=='gbff':
                pass
            else:
                raise Exception('gbff is null')
        else:
            raise Exception('specify the gbff= in the first input')
    return gbff,database

gbff,database=verifarchivoaimportar()

def trim(inputlist):## To take out the end of lines
    listatrim=[]
    for i in inputlist:
        listatrim.append(i[0:-1])
    return listatrim

###Getting all the organism fields
accesion=trim(findaccesion(gbff))
name=trim(findname(gbff))
source=trim(findsource(gbff))
base_pairs=findbasepairs(gbff)
date=trim(finddate(gbff))
structure=findstructure(gbff)
type=findtype(gbff)
definition=findddefinition(gbff)# beffore comma
completeness=finddcompleteness(gbff)# after comma en definition
taxonomy=finddtaxonomy(gbff)
print('cantidad de registros a organismo que le entraran',len(taxonomy),len(completeness),len(accesion))


####Extended comments get
description,value,accs=getextcomments(gbff)
print('cantidad de registros a comentarios que le entraran',len(description),len(value),len(accs))

if len(description)==len(value) and len(value)==len(accs):
    pass
else:
    raise Exception('Error in reading the file!')

####Proteins get

position,product,proteinid,translation,translationt,accesion1 = protsearch(gbff)

print('cantidad de registros a proteinas que le entarran',len(position),len(product),len(proteinid),len(translation),len(accesion1))

###SQLITE

conn = sqlite3.connect(database)

## Organism
for i in range (0,len(accesion)):
    insertions = [(accesion[i], base_pairs[i], type[i], structure[i], date[i], definition[i], completeness[i], source[i], name[i], taxonomy[i])]
    conn.executemany('INSERT INTO Organism VALUES (?,?,?,?,?,?,?,?,?,?)', insertions)


## Commentaries
for i in range (0,len(accs)):
    insertions1 = [(accs[i], description[i], value[i])]
    conn.executemany('INSERT INTO "Extended comments" VALUES (?,?,?)', insertions1)


## Protein # When there is something missing fill it with blank
for i in range (0,len(accesion1)):
    insertions2 = [(proteinid[i], accesion1[i], position[i], translationt[i], translation[i], product[i])]
    conn.executemany('INSERT INTO Protein VALUES (?,?,?,?,?,?)', insertions2)

## Undo this comment to register the data
#conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

##Command to try
#python SQLjoining.py db=data/Probiodb.db gbff=data/GCA_003972325.1_ASM397232v1_genomic.gbff
#python SQLjoining.py db=data/Probiodb.db gbff=data/sequence.gbff
