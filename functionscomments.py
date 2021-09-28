import re
import numpy as np


def getextcomments(filename): ## This is when a name of the organism is given only
    sources=[]
    finale=[]
    accesion=[]
    count=0
    with open(filename) as file:
        lines = file.readlines()
        enter=0
        for line in lines:
            if re.search(r'\bData-END\b', line) and enter==1:## When one annotation is over
                enter=0
                accs=np.repeat(acc,count, axis=0)
                for i in accs:
                    accesion.append(i)
                count=0
            if enter == 1 and '::' in line:### To save each pair of description and value
                description=line.split(' :: ')[0].strip()
                value=line.split(' :: ')[1].strip()
                count=count+1
                sources.append(description)
                finale.append(value)
            if re.search(r'\bACCESSION\b', line):### copy as many accesions as value or sources
                acc=line.split("   ")[1]
                if re.search(r'\b \b', acc):
                    acc = acc.split(" ")[0]
                if acc[-1] =='\n':
                    acc=acc[:-1]
            if re.search(r'\b-Data-START\b', line) and enter == 0:# Starting to save
                enter=1
    return sources,finale,accesion

