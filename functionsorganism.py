import re
import numpy as np

def findaccesion(filename):# this is to find the accession
    accesion=[]
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            if re.search(r'\bACCESSION\b', line):
                acc=line.split("   ")[1]
                if re.search(r'\b \b', acc):
                    acc = acc.split(" ")[0]
                accesion.append(acc)
    return accesion


def findname(filename): ## This is when a name of the organism is given only
    names=[]
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            if re.search(r'\bORGANISM\b', line):
                name=line.split("  ")[2]
                names.append(name)
    return names

def findsource(filename): ## This is when a name of the organism is given only
    sources=[]
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            if re.search(r'\bSOURCE\b', line):
                source=line.split("      ")[1]
                sources.append(source)
    return sources

def findbasepairs(filename): ## This is when a name of the organism is given only
    sources=[]
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            if re.search(r'\bLOCUS\b', line):
                source=line.split()[2]
                sources.append(int(source))
    return sources

def findtype(filename): ## This is when a name of the organism is given only
    sources=[]
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            if re.search(r'\bLOCUS\b', line):
                source=line.split()[4]
                sources.append(source)
    return sources

def findstructure(filename): ## This is when a name of the organism is given only
    sources=[]
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            if re.search(r'\bLOCUS\b', line):
                source=line.split()[5]
                sources.append(source)
    return sources

def finddate(filename): ## This is when a name of the organism is given only
    sources=[]
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            if re.search(r'\bLOCUS\b', line):
                source=line[-12:]
                sources.append(source)
    return sources

  
def findddefinition(filename): ## This is when a name of the organism is given only
    sources=[]
    finales=[]
    with open(filename) as file:
        lines = file.readlines()
        enter=0
        for line in lines:
            if re.search(r'\bACCESSION\b', line) and enter==1:
                enter=0
                a=''.join(sources).split(',')
                finales.append(''.join(a[0:-1]))
                sources=[]
            if enter ==1:
                source= line.strip()
                sources.append(source)
            if re.search(r'\bDEFINITION\b', line):
                enter=1
                sourci=line.split('  ')[1]
                sources.append(sourci)
    return finales

def finddcompleteness(filename): ## This is when a name of the organism is given only
    sources=[]
    finales=[]
    with open(filename) as file:
        lines = file.readlines()
        enter=0
        for line in lines:
            if re.search(r'\bACCESSION\b', line) and enter==1:
                enter=0
                a=''.join(sources).split(',')[-1]
                if a[-1]=='\n':
                    a=a[:-1]
                finales.append(a)
                sources=[]
            if enter ==1:
                source= line.strip()
                sources.append(source)
            if re.search(r'\bDEFINITION\b', line):
                enter=1
                sourci=line.split('  ')[1]
                sources.append(sourci)
    return finales

def finddtaxonomy(filename): ## This is when a name of the organism is given only
    sources=[]
    finale=[]
    with open(filename) as file:
        lines = file.readlines()
        enter=0
        for line in lines:
            if re.search(r'\bREFERENCE\b', line) and enter==1:## This when the name of the organism has ended
                enter=0
                finale.append(''.join(sources))
                sources=[]
            if enter == 1:
                source=line.strip()
                sources.append(source[:-1])
            if re.search(r'\bORGANISM\b', line) and enter == 0:# This is the start of organism to save
                source=line.split('  ')[2]
                sources.append(source[:-1])
                enter=1
    return finale




