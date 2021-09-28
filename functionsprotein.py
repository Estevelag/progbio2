import re
import numpy as np

def protsearch(filename):# protein table variables
    translation=[]
    translationt=[]
    position=[]
    proteinid=[]
    product=[]
    accesion=[]
    trans=[]
    protid={}
    with open(filename) as file:
        lines = file.readlines()
        enter=0
        transentro=0
        extranst=0
        exproduct=0
        for line in lines:
            if not (line[:21]=='                     ') and enter == 1:## getting out of the CDS
                enter=0
                transentro=0
                if extranst==1:# to make a space when translation table is no t encountered
                    translationt.append('')
                if exproduct==1:
                    product.append('')
                exproduct=0
                extranst=0
                t=''.join(trans)
                translation.append(t)
                accesion.append(acc)
                trans=[]
            if re.search(r'\bproduct\b', line) and enter==1:#Product saving
                prod=line.split('=')[1]
                product.append(prod[1:-2])
                exproduct=0
            if line[:21]=='                     ' and re.search(r'\bprotein_id\b', line) and enter==1:# proteinid getting
                proid=line.split('=')[1]
                proteinid.append(proid[1:-2])
            if re.search(r'\bACCESSION\b', line):### copy as many accesions as value or sources
                acc=line.split("   ")[1]
                if re.search(r'\b \b', acc):
                    acc = acc.split(" ")[0]
                if acc[-1] =='\n':
                    acc=acc[:-1]
            if re.search(r'\db_xref\b', line)and enter==1:
                extranst=0
                ref=line.split('=')[1]
                translationt.append(ref[1:-2])
            if line[:21]=='                     ' and transentro==1 and enter==1:# Saving the translation
                trans.append(line.strip()[:-1])
            if line[:21]=='                     ' and re.search(r'\btranslation\b', line) and enter==1 and transentro==0:##Starting to save the translation 
                if not ('product' in line):
                    transentro=1
                    id=line.split('=')[1][1:-1].replace('"','')
                    trans.append(id)
            if re.search(r'\bCDS\b', line) and enter==0:#Entering CDS
                enter=1
                extranst=1
                exproduct=1
                posit=line.split()[1]
                position.append(posit[:-1])

    return position,product,proteinid,translation,translationt,accesion
