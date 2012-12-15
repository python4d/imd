#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Module Créé le 13 déc. 2012
Gére le Process PLAST3D
Lien pour rediriger la sortie d'un fichier
@note: http://stackoverflow.com/questions/8712466/wxpython-redirect-text-dynamically-to-text-control-box
@author: Python4D/damien
'''


"""
à faire:
-créer les fichiers pour plast les sauvegarder dans le projet
-lancer plast dans un subprocess
-controler la sortie/info donnée par plast cia le fichier tempsdecalcul.txt
-explorer le dernier fichier vtk produit pour connaitre la distance film/moule (!)
-arrêter le subprocess avant que le moule soit en dessous du film...
-?
"""

import subprocess,os,time,sys
from threading import Thread as Process

def seeout(p):
  while True:
    inline = p.stdout.readline()
    if p.poll() != None:
        break
    sys.stdout.write(inline)
    sys.stdout.flush()
    
_path=os.getcwd()
os.chdir("C:/Users/damien/Documents/Projets/IMD3D/Plast/Plast+ exemple d'application")
p=subprocess.Popen("plast3d.exe",shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE)

print "Done"
p.stdin.write("simulation_demioeuf.dat\n0\n1000\n100\n")
Process(target=seeout, args=(p,)).start() #on doit créer un thread pour la lecture de sortie du PIPE

time.sleep(10)
p.kill()
time.sleep(100)
os.chdir(_path)
print os.getcwd()

