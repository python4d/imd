#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Module Cr�� le 13 d�c. 2012
G�re le Process PLAST3D
Lien pour rediriger la sortie d'un fichier
@note: http://stackoverflow.com/questions/8712466/wxpython-redirect-text-dynamically-to-text-control-box
@author: Python4D/damien
'''
from send2trash import send2trash


"""
� faire:
-cr�er les fichiers pour plast les sauvegarder dans le projet
-lancer plast dans un subprocess
-controler la sortie/info donn�e par plast via le fichier tempsdecalcul.txt
-explorer le dernier fichier vtk produit pour connaitre la distance film/moule (!)
-arr�ter le subprocess avant que le moule soit en dessous du film...
-?
"""
import pystl,Common
import subprocess,os,time,sys
from threading import Thread as Process
import logging
import collections
import numpy

class PlastProcess(object):
  def __init__(self,app):
    self.ProcessPlastInProgress=None
    self.f = app
    self.points_moule=[]
    self.points_film=[]
    self.points_externes_film=[] #correspond aux points exterieurs du film g�n�r� automatiquement (cf GenererFilm())
    self.datas=collections.OrderedDict()
    
    #(Tous Constants)
    self.datas["#Generalities line 1"]   ="         1        100        100          0          0          0          0          0          0          0 "
    
    #                           Nb noeuds total / Nb �l�ments total / 8(const) /   Nb points limit�s /  Nb materiaux(ou corps?)(2voir3) /  0(const)   
    self.datas["#Generalities line 2"]   ="     10240       9986          8        348          2          0 "

    #                                  (Tous Constants)
    self.datas["#Generalities line 3"]   ="         6          0          0  5.000000000000000e-01 "
    
    #QUADRANGLES, RESPECTER L'ORDRE DE NUMEROTATION CONTINUE          
    #N� element(1-n) / N� materiau(film=1,moule=2ou3) / N� noeud A / N� noeud B / N� noeud C / N� noeud D
    self.datas["#Elements"]              ="         1          1          1          2         93         92 "
    
    #N� noeud(1-m) / X(mm) / Y(mm) / Z(mm) / N� corps(1ou2voir3)
    self.datas["#Nodes"]                 ="         1  1.125000000000000e+02  8.681209560000001e+01  -1.03000000000000e+01          1 "
    
    #N� noeud / X:0ou1 / Y:0ou1 / Z:0ou1
    self.datas["#Degrees of freedom"]    =""
    
    # 1(const) / 3(const)          
    # 2.100000000000000e+01(const) /  3.000000000000000e-01(const) /  Epaisseur(mm) / Masse_surfacique(?) / 0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  C1(SI) / C2(SI)
    # T�(�C) / Nb_tps_relaxation(1�10) / lambda1(s) / G1(MPa) / lambda2(s) / G2(MPa) / lambda3(s) / G3(MPa)
    # lambda4(s) /  G4(MPa) / lambda5(s) / G5(MPa) / lambda6(s) / G6(MPa) / lambda7(s) / G7(MPa) 
    # lambda8(s) / G8(MPa) / lambda9(s) / G9(MPa) / lambda10(s) / G10(MPa)  9.000000000000000e+00(const) / 5.000000000000000e+02(const)
    # 5.000000000000000e+02(const) / 0.000000000000000e+00(const) / 5.000000000000000e-01(const) / 5.000000000000000e-01(const) / 0.000000000000000e+00(const) / 1.000000000000000e+02(const) / 0.000000000000000e+00(const)
    # 2(const) /  4(const)
    # 0.000000000000000e+00(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const)
    # deltaXmax(mm) / deltaYmax(mm) / deltaZmax(mm) / 0.000000000000000e+00(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const) / 0.000000000000000e+00(const)
    # 0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  dX(mm) / dY(mm) / dZ(mm) / 0.000000000000000e+00(const) /  0.000000000000000e+00(const) /
    # 0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) / 0.000000000000000e+00(const) 
    # 0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) / 0.000000000000000e+00(const) 
    self.datas["#Materials"]             ="""         1          3 
 2.100000000000000e+01  3.000000000000000e-01  0.100000000000000e+00  1.000000000000000e+01  0.000000000000000e+00  0.000000000000000e+00  1.050000000000000e+01  5.155000000000000e+01 
 1.300000000000000e+02  1.000000000000000e+00  0.100000000000000e+00  1.100000000000000e-01  1.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00 
 0.000000000000000e+00  0.000000000000000e+00  1.000000000000000e-02  5.000000000000000e+02  5.000000000000000e+02  4.100000000000000e+01  4.100000000000000e+01  0.000000000000000e+00 
 0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  9.000000000000000e+00  5.000000000000000e+02 
 5.000000000000000e+02  0.000000000000000e+00  5.000000000000000e-01  5.000000000000000e-01  0.000000000000000e+00  1.000000000000000e+02  0.000000000000000e+00  3.000000000000000e+02
         2          4 
 0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00 
 0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00 
 0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00 
 0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00 
 0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00 """
 
    #NOTION DE TEMPS POUR LA SIMULATION
    #    Nb pas /  duree_pas(=Tcritique)(s)(CALCULE) / 0.000000000000000e+00(const) /   -1.00000000000000e+00(const) /   1.000000000000000e-02(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const) /   0.000000000000000e+00(const) 
    self.datas["#Time control"]          ="    110000  1.000000000000000e-04  0.000000000000000e+00  -1.00000000000000e+00  1.000000000000000e-02  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00 "
    
    #displacements=>� d�finir ous
    #Possibilit� (non utilis�e) de d�finir un d�placement par noeud => ici tous les noeuds � z�ro
    #     Nb noeuds total  / 0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0(const)
    self.datas["#Displacements"]         ="     10240  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00          0 "
    
    #Possibilit�s (non utilis�e) de d�finir par noeud une vitesse => ici z�ro...
    self.datas["#Velocities"]            ="     10240  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00 "
    
    #  Fponctuelles?(0ou1) / 0(const) /  0(const) /   0(const) /    / Nb face sous pression (0ou1?)
    self.datas["#Loads header"]          ="         0          0          0          0          1 "
    
    #Possibilit� (non utilis�) de d�finir une pression pour chaque noeud si Fponctuelles=1 (cf pr�c�dent)=> N� noeud / Fx(N) / Fy(N) / Fz(N)
    self.datas["#Punctual loads"]        =""

    #Possibilit� (non utilis�) de d�finir une pression gravitationnelle => 1/x / 2/y / 3/z  / Const de Gravit� m/s2
    self.datas["#Gravity loads"]         =""
    
    #????
    self.datas["#Non follower surface loads"]=""
    
    #N� corps(1) / cot�(1ou2) / Pression(+)/depression(-)(unite?)
    self.datas["#Follower surface loads"]="         1          1  -1.00000000000000e+02 "
    
    #TOUS CONSTANTS
    self.datas["#fich_utilis.f"]         ="         0  0.000000000000000e+00          0          0          0          0          0          0          0          0          0          0 "  
    
    #?LIGNE COMMENTAIRE?
    self.datas["#################################################"]=""
    
    #?LIGNE COMMENTAIRE?
    self.datas["# Entete contact"]       =""
    
    #D�finition de un ou deux contacts (un seul sera utilis�, appel� #Couple)
    # Nb de contacts(1ou2) /  100(const) /   1.000000000000000E-07(const) /    4(const) /   0(const) /   0(const) /   0  10000(const) /   10000(const) / 
    self.datas["#    NBCCT      NMIGS                  TOLCB      ISPLI      ILAGR      IVISM      N_MPC      MDNOC      MDFAT"]="         1        100  1.000000000000000E-07          4          0          0          0      10000      10000"

    #TOUS CONSTANTS (suite de la d�finition d'un contact (couple)
    self.datas["#     NSEG  NMAXCCSEG      NGLOB                 DPGLOB"]="""       500        400        100  5.000000000000000E-01
 1.000000000000000E+02  0.000000000000000E+00  1.000000000000000E+01  1.000000000000000E+02"""
 
    #definition d'un couple
    #???LIGNE DE COMMENTAIRE???
    self.datas["#Couple 1"]=""
    
    #SLAVE SURFACE=FILM
    # 1(const) / 1(const) /  0(const) /
    # 0(const) /  coef_frottement(unite?)  
    self.datas["#Slave surface"]="""         1          1          0 
         0  0.300000000000000e+00 """
    
    #MASTER SURFACE=MOULE (mat�riaux 2 et 3[non utilis�])
    # N�corps(2) / 1(const) 
    self.datas["#master surface"]="         2          1 "
    

    self.app=app
    self.wait_SeeOut=self.wait_SeeErr=False

  def ExtractFilmMouleFromDAT(self,filein):
    """
    @param filein:full path du fichier sp�cifique plast.DAT � traiter 
    @return points_film, points_moule: "list" des faces trouv�es [[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)],...,[(xn,yn,zn),(xn+1,yn+1,zn+1),(xn+2,yn+2,zn+2)]]
    @note: utilisation d'une state machine pour parser le d�but du fichier DAT
    """
    statecase=10
    with open(filein) as _f:
      for i in _f.readlines():
        if statecase==10:
          if i.split("\n")[0]=="#Generalities line 2": statecase=20
        elif statecase==20:
          nb_noeuds_total,nb_elements_total,_,nb_noeuds_conditions_limites,nb_materiaux_differents,_=map(int,i.split())
          statecase=30
        elif statecase==30:
          if i.split("\n")[0]=="#Elements": 
            boucle_elements=0
            TableConnectiviteMoule=[]
            TableConnectiviteFilm=[]
            statecase=40
        elif statecase==40:
          table_connectivite_element=[]*8
          data= map(int,i.split())
          if data[5]==0:   #cas d'un triangle (cf doc plast)
            numero_element,nb_element_materiau,table_connectivite_element=data[0],data[1],data[2:5]  
          else:                    
            numero_element,nb_element_materiau,table_connectivite_element=data[0],data[1],data[2:]
          if nb_element_materiau==2: 
            TableConnectiviteMoule.append(table_connectivite_element)
          elif nb_element_materiau==1: 
            TableConnectiviteFilm.append(table_connectivite_element)
          else: logging.error("!Truc Bizarre dans ExtractFilmMouleFromDAT statecase 40 (parsing table_element !")
          boucle_elements+=1
          if boucle_elements==nb_elements_total:       
            statecase=50
        elif statecase==50:
          if i.split("\n")[0]=="#Nodes": 
            boucle_noeuds=0
            Noeuds=[]  
            statecase=60
        elif statecase==60: 
          data=i.split()        
          numero_noeud=int(data[0])
          coordxyz=list(map(float,data[1:4]))
          numero_corps_affecte_noeud=int(data[4])
          Noeuds.append(coordxyz)
          boucle_noeuds+=1
          if boucle_noeuds==nb_noeuds_total:
            statecase=100
#parsing suffisant pour cr�er les deux listes de pts moule et film            
        elif statecase==100:  
          pass
    points_moule=[]
    points_film=[]
    for i in TableConnectiviteFilm:
      face=[]
      for j in i:
        face.append(Noeuds[j-1])
      points_film.append(face)
    for i in TableConnectiviteMoule:
      face=[]
      for j in i:
        face.append(Noeuds[j-1])
      points_moule.append(face)
    return points_film,points_moule

  def CreateThermique(self,nb_noeuds,temp=100.0):
    with open("../plast3d/thermique.dat","w") as _f:
      _f.write("#Noeuds\n{:d}\n".format(nb_noeuds))    
      for i in range(nb_noeuds):
        _f.write("{:10d} {:10.3f}\n".format(i+1,temp))

  
  def CreateDat(self,fileout,points_film=None,points_moule=None):
    """
    Cr�ation des lignes du fichier plast DAT
    Cr�ation du fichier plast .DAT
    """
    if not points_moule==None: self.points_moule= points_moule
    if not points_film==None: self.points_film= points_film
    if self.points_moule==[]:
      a=pystl.cSTL("../plast3d/D216-moule+film.STL")
      self.points_moule=a.read(scale=1)
      
    _n,_f,_dol=(1,1,1) #nb de noeuds total, faces total, nb degree of liberty du film

    self.datas["#Nodes"]=""    
    self.datas["#Elements"]=""
    self.datas["#Degrees of freedom"]=""
  
#Donn�es du film : 
#  1) R�cup�ration de la liste de tous les noeuds uniques
#  2) Re-Cr�ation des faces en utilisant uniquement les num�ros des noeuds de cette liste 
#  3) Re-Cr�ation des la liste des "degres de libert�" en utilisant uniquement les num�rso des noeuds de cette liste 
    logging.warning(">>CreateDat>>DEBUT CREATION DATA FILM")
    noeuds_data=[]
    faces_data=[] 
    dol_data=[]           
    for face in self.points_film:
      new_face=[]
      for noeud in face:
        try: #on essaye de trouver la place du noeud dans la liste d�j� constitu�
          place=noeuds_data.index(noeud)
          new_face.append(place+1)
        except ValueError: # la valeur du noeud n'existe pas encore dans la liste, on l'ajoute 
          noeuds_data.append(noeud)
          new_face.append(len(noeuds_data))
      faces_data.append(new_face)
    for i in self.points_externes_film:
      try:
        place=noeuds_data.index(i)
        dol_data.append(place+1)
      except ValueError:
        pass
    logging.warning(">>CreateDat>>FIN CREATION DATA FILM")  
    for i in noeuds_data:     
      self.datas["#Nodes"]+="{0:10d} {2:+22.14e} {3:+22.14e} {4:+22.14e} {1:10d} \n".format(_n,1,*i)
      _n+=1
        
    for i in faces_data:
      if len(i) == 3 :
        self.datas["#Elements"]+="{0:10d} {1:10d} {3:10d} {4:10d} {5:10d} {2:10d} \n".format(_f,1,i[0],*i)
      else:
        self.datas["#Elements"]+="{:10d} {:10d} {:10d} {:10d} {:10d} {:10d} \n".format(_f,1,*i)
      _f+=1
    
    for i in dol_data:
        self.datas["#Degrees of freedom"]+="{:10d} {:10d} {:10d} {:10d} \n".format(i,1,1,0)
    self.datas["#Degrees of freedom"]=self.datas["#Degrees of freedom"][:-1]
       
    #Cr�ation du fichier thermique.dat indispensable pour le fonctionnement de plast
    if self.f==None or not self.f.m_checkBox_fichier_thermique.GetValue()==True:
      self.CreateThermique(len(noeuds_data))   
    
     
#Donn�es du moule : 
#  1) R�cup�ration de la liste de tous les noeuds uniques
#  2) Re-Cr�ation des  faces en utilisant uniquement les num�ros des noeuds de cette liste 
    logging.warning(">>CreateDat>>DEBUT CREATION DATA MOULE")
    noeuds_data=[]
    faces_data=[]            
    for face in self.points_moule:
      new_face=[]
      for noeud in face:
        try:
          place=noeuds_data.index(noeud)
          new_face.append(place+1+_n-1)
        except ValueError:
          noeuds_data.append(noeud)
          new_face.append(len(noeuds_data)+_n-1)
      faces_data.append(new_face)
    logging.warning(">>CreateDat>>FIN CREATION DATA MOULE")  
    for i in noeuds_data:     
      self.datas["#Nodes"]+="{0:10d} {2:+22.14e} {3:+22.14e} {4:+22.14e} {1:10d} \n".format(_n,2,*i)
      _n+=1
    self.datas["#Nodes"]=self.datas["#Nodes"][:-1]  

    for i in faces_data:
      if len(i) == 3 :
        self.datas["#Elements"]+="{0:10d} {1:10d} {3:10d} {4:10d} {5:10d} {2:10d} \n".format(_f,2,i[0],*i)
      else:
        self.datas["#Elements"]+="{:10d} {:10d} {:10d} {:10d} {:10d} {:10d} \n".format(_f,2,*i)
      _f+=1
    self.datas["#Elements"]=self.datas["#Elements"][:-1]
      
    #Construction de la ligne #Generalities line 2 =  Nb noeuds total  Nb �l�ments total  8   Nb points limit�s  Nb materiaux(ou corps?)(2voir3)  0
    self.datas["#Generalities line 2"]="{:10d} {:10d} {:10d} {:10d} {:10d} {:10d} ".format(_n-1,_f-1,8,len(dol_data),2,0)
    
    #TODO:Construction 'provisoire' de #Displacements et #Velocities
    self.datas["#Displacements"]="{:10d}".format(_n-1)+self.datas["#Displacements"][10:]
    self.datas["#Velocities"]="{:10d}".format(_n-1)+self.datas["#Velocities"][10:]
    
    
    logging.warning(">>CreateDat>>ECRITURE DU FICHIER DAT")     
    with open("../plast3d/test.dat","w") as _f:
      for i in self.datas.items():
        _f.write(i[0]+"\n")
        if i[1]!="": _f.write(i[1]+"\n")
    
        
  def GenererFilm(self,largeur=100,hauteur=100,pas=1,z=0):
    """
    @param largeur: en mm, correspond � la largeur int�rieure du cadre entourant le film (base du cadre)
    @param hauteur:  en mm, correspond � la hauteur/longueur int�rieure du cadre entourant le film         
    @param pas: en mm, pas entre chaque noeud
    @param z: hauteur du film
    @return: points_film, "list" des faces g�n�r�es [[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3),(x4,y4,z4)],...,[(xn,yn,zn),(xn+1,yn+1,zn+1),(xn+2,yn+2,zn+2),(xn+3,yn+3,zn+3)]]
    """
    self.points_film=[]
    self.points_externes_film=[]
    #on arrondit largeur et au hauteur au multiple de pas juste sup�rieur
    largeur=largeur+pas-largeur%pas if largeur%pas!=0 else largeur
    hauteur=hauteur+pas-hauteur%pas if hauteur%pas!=0 else hauteur
    for y in numpy.arange(-hauteur/2.0,hauteur/2.0,pas):
      for x in numpy.arange(-largeur/2.0,largeur/2.0,pas):
        self.points_film.append([(x,y,z),(x+pas,y,z),(x+pas,y+pas,z),(x,y+pas,z)])
        if x==-largeur/2.0 or y==-hauteur/2.0:
          self.points_externes_film.append((x,y,z))
        if x==largeur/2.0-pas:
          self.points_externes_film.append((x+pas,y,z))
        if y==largeur/2.0-pas:
          self.points_externes_film.append((x,y+pas,z))
        if x==largeur/2.0-pas and y==hauteur/2.0-pas:  
          self.points_externes_film.append((x+pas,y+pas,z))
          
    #le tour 
    return self.points_film
        
        
   
   
  def VerifParamPlast(self):
    pass

   
      
   
   
  def SeeOut(self,p):
    i=0
    while True:
      inline = p.stdout.readline()
      logging.warning(inline)
      while (self.wait_SeeErr):pass
      self.wait_SeeOut=True
      self.app.oNoteBook.MessageLog("Line n�<%d> from PLAST>>>%s" % (i,inline),"INFO")
      self.wait_SeeOut=False
      i+=1
      sys.__stdout__.flush()
      if p.poll() != None:
        break
      
  def SeeErr(self,p):
    i=0
    while True:
      inline =p.stderr.readline()
      logging.warning(inline)
      while (self.wait_SeeOut):pass
      self.wait_SeeErr=True      
      self.app.oNoteBook.MessageLog("Line n�<%d> from PLAST>>>%s" % (i,inline),"ERROR")
      self.wait_SeeErr=False     
      i+=1
      sys.__stderr__.flush()
      if p.poll() != None:
        break
          
  def LaunchProcessPlast(self,_f=None):
    if not self.ProcessPlastInProgress==None:
      self.app.oNoteBook.MessageLog("Process PLAST d�j� lanc�  >>> Killez-le !","ERROR")
    else:
      _path=os.getcwd()
      os.chdir(_f.oProjetIMD.projet["root"]["dir"]["plast3d"])
      files = [f for f in os.listdir('.') if os.path.isfile(f)]
      for i in files:
        if i[0:3]=="GMV" or i[-3:]=="vtk":
          send2trash(i)
      self.ProcessPlastInProgress=subprocess.Popen("plast3d.exe",shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      self.ProcessPlastInProgress.stdin.write(os.path.split(_f.oProjetIMD.projet["root"]["fichier plast.dat"])[1]+"\n1\n30000\n100\n")
      Process(target=self.app.oPlastProcess.SeeOut, args=(self.ProcessPlastInProgress,)).start() #on doit cr�er un thread pour la lecture de sortie stdout du PIPE
      Process(target=self.app.oPlastProcess.SeeErr, args=(self.ProcessPlastInProgress,)).start() #on doit cr�er un thread pour la lecture de sortie stderr du PIPE
      os.chdir(_path)
      return self.ProcessPlastInProgress
  
if __name__=="__main__":
  p=PlastProcess(None)
  
  state=20
  if state==10 : #utilisation d'un dat avec moule/film QUAD  puis cr�er des TRI
    p.GenererFilm(100,100,1,10)
    film_q,moule_q=p.ExtractFilmMouleFromDAT("../plast3d/simulation_demioeuf.dat")
    film_t=[]
    moule_t=[]
    for face in film_q:
        film_t.append([face[0],face[1],face[3]])
        film_t.append([face[1],face[2],face[3]])
    for face in moule_q:
        moule_t.append([face[0],face[1],face[3]])
        moule_t.append([face[1],face[2],face[3]])                  
    p.CreateDat("../plast3d/test.dat",film_t,moule_t)
    
  if state==20:#utilisation d'un STL calcul des dimensions de l'objet puis cr�ation du film
    a=pystl.cSTL(u"C:/Users/damien/Documents/Projets/IMD3D/Plast/untitled2.stl")
    mouleSTL=a.read(scale=1)
    c1,c2,c3,c4=Common.FindCorners(mouleSTL)
    print c1,c2,c3,c4 #-x,-y,x,y
    largeur=c3[0]-c1[0]
    hauteur=c4[1]-c2[1]
    print largeur,hauteur
    filmSTL=p.GenererFilm(largeur+10,hauteur+10,4,60)       
    p.CreateDat("../plast3d/test.dat",filmSTL,mouleSTL)
  