import sys
import os
import re 
import sqlite3
from functionsorganism import *
from functionsprotein import protsearch
from functionscomments import getextcomments

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

def trim(inputlist):## To take out the end of lines
    listatrim=[]
    for i in inputlist:
        listatrim.append(i[0:-1])
    return listatrim

###Getting all the organism fields
def getorganismfields(gbff):
    accesion=trim(findaccesion(gbff))
    name=trim(findname(gbff))
    source=trim(findsource(gbff))
    base_pairs=findbasepairs(gbff)
    date=trim(finddate(gbff))
    structure=findstructure(gbff)
    type=findtype(gbff)
    definition=findddefinition(gbff)# before comma
    completeness=finddcompleteness(gbff)# after comma en definition
    taxonomy=finddtaxonomy(gbff)
    print('cantidad de registros a organismo que le entraran',len(taxonomy),len(completeness),len(accesion))
    return accesion, name, source, base_pairs, date, structure, type, definition, completeness, taxonomy
#
def validatorfieldscomments(description,value,accs):
    if len(description)==len(value) and len(value)==len(accs):
        pass
    else:
        raise Exception('Error in reading the file!')

def uploadorganismsql(accesion, name, source, base_pairs, date, structure, type, definition, completeness, taxonomy,conn):
    for i in range (0,len(accesion)):
        insertions = [(accesion[i], base_pairs[i], type[i], structure[i], date[i], definition[i], completeness[i], source[i], name[i], taxonomy[i])]
        conn.executemany('INSERT INTO Organism VALUES (?,?,?,?,?,?,?,?,?,?)', insertions)

def uploadcommentssql(accs,description,value,conn):
    ## Commentaries
    for i in range (0,len(accs)):
        insertions1 = [(accs[i], description[i], value[i])]
        conn.executemany('INSERT INTO "Extended comments" VALUES (?,?,?)', insertions1)

def uploadproteins(proteinid, accesion1, position, translationt, translation, product, conn):
    for i in range (0,len(accesion1)):
        insertions2 = [(proteinid[i], accesion1[i], position[i], translationt[i], translation[i], product[i])]
        conn.executemany('INSERT INTO Protein VALUES (?,?,?,?,?,?)', insertions2)

def verifyuniqueness(conn,accesion):
    crsr = conn.cursor()
    crsr.execute("SELECT accesion FROM Organism")
    accsp=crsr.fetchall() 
    variab=[]
    for i in accsp:
        variab.append(str(i)[2:-3])
    for i in accesion:
        if i in variab:
            raise Exception("Duplicate accesion is already present " )
        else:
            pass

def main():
    gbff,database=verifarchivoaimportar()
    ###Getorganism
    accesion, name, source, base_pairs, date, structure, type, definition, completeness, taxonomy=  getorganismfields(gbff)
    ####Extended comments get
    description,value,accs=getextcomments(gbff)
    print('cantidad de registros a comentarios que le entraran',len(description),len(value),len(accs))
    validatorfieldscomments(description,value,accs)
    ####Proteins get
    position,product,proteinid,translation,translationt,accesion1 = protsearch(gbff)
    print('cantidad de registros a proteinas que le entraran',len(position),len(product),len(proteinid),len(translation),len(accesion1))
    ###SQLITE
    conn = sqlite3.connect(database)
    # Verify uniqueness:
    verifyuniqueness(conn,accesion)
    ## Organismaqlupload
    uploadorganismsql(accesion, name, source, base_pairs, date, structure, type, definition, completeness, taxonomy,conn)
    ## Comments upload
    uploadcommentssql(accs,description,value,conn)
    ## Proteins upload
    uploadproteins(proteinid, accesion1, position, translationt, translation, product, conn)
    ## Undo this comment to register the data
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    #como raisear uniqueness

## running if main is function  
if __name__ == "__main__":
    main()
else:
    pass

##Command to try
#python SQLjoining.py db=data/Probiodb.db gbff=data/GCA_003972325.1_ASM397232v1_genomic.gbff
#python SQLjoining.py db=data/Probiodb.db gbff=data/sequence.gbff
