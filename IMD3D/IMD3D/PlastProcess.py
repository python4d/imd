#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Module Créé le 13 déc. 2012
Gére le Process PLAST3D
Lien pour rediriger la sortie d'un fichier
@note: http://stackoverflow.com/questions/8712466/wxpython-redirect-text-dynamically-to-text-control-box
@author: Python4D/damien
'''
from send2trash import send2trash
import shutil


"""
à faire:
-créer les fichiers pour plast les sauvegarder dans le projet
-lancer plast dans un subprocess
-controler la sortie/info donnée par plast via le fichier tempsdecalcul.txt
-explorer le dernier fichier vtk produit pour connaitre la distance film/moule (!)
-arrêter le subprocess avant que le moule soit en dessous du film...
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
    self.points_externes_film=[] #correspond aux points exterieurs du film généré automatiquement (cf GenererFilm())
    self.datas=collections.OrderedDict()
    
    #(Tous Constants)
    self.datas["#Generalities line 1"]   ="         1        100        100          0          0          0          0          0          0          0 "
    
    #                           Nb noeuds total / Nb éléments total / 8(const) /   Nb points limités /  Nb materiaux(ou corps?)(2voir3) /  0(const)   
    self.datas["#Generalities line 2"]   ="     10240       9986          8        348          2          0 "

    #                                  (Tous Constants)
    self.datas["#Generalities line 3"]   ="         6          0          0  5.000000000000000e-01 "
    
    #QUADRANGLES, RESPECTER L'ORDRE DE NUMEROTATION CONTINUE          
    #N° element(1-n) / N° materiau(film=1,moule=2ou3) / N° noeud A / N° noeud B / N° noeud C / N° noeud D
    self.datas["#Elements"]              ="         1          1          1          2         93         92 "
    
    #N° noeud(1-m) / X(mm) / Y(mm) / Z(mm) / N° corps(1ou2voir3)
    self.datas["#Nodes"]                 ="         1  1.125000000000000e+02  8.681209560000001e+01  -1.03000000000000e+01          1 "
    
    #N° noeud / X:0ou1 / Y:0ou1 / Z:0ou1
    self.datas["#Degrees of freedom"]    =""
    
    # 1(const) / 3(const)          
    # 2.100000000000000e+01(const) /  3.000000000000000e-01(const) /  Epaisseur(mm) / Masse_surfacique(?) / 0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  C1(SI) / C2(SI)
    # T°(°C) / Nb_tps_relaxation(1à10) / lambda1(s) / G1(MPa) / lambda2(s) / G2(MPa) / lambda3(s) / G3(MPa)
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
    
    #displacements=>à définir ous
    #Possibilité (non utilisée) de définir un déplacement par noeud => ici tous les noeuds à zéro
    #     Nb noeuds total  / 0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0.000000000000000e+00(const) /  0(const)
    self.datas["#Displacements"]         ="     10240  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00          0 "
    
    #Possibilités (non utilisée) de définir par noeud une vitesse => ici zéro...
    self.datas["#Velocities"]            ="     10240  0.000000000000000e+00  0.000000000000000e+00  0.000000000000000e+00 "
    
    #  Fponctuelles?(0ou1) / 0(const) /  0(const) /   0(const) /    / Nb face sous pression (0ou1?)
    self.datas["#Loads header"]          ="         0          0          0          0          1 "
    
    #Possibilité (non utilisé) de définir une pression pour chaque noeud si Fponctuelles=1 (cf précédent)=> N° noeud / Fx(N) / Fy(N) / Fz(N)
    self.datas["#Punctual loads"]        =""

    #Possibilité (non utilisé) de définir une pression gravitationnelle => 1/x / 2/y / 3/z  / Const de Gravité m/s2
    self.datas["#Gravity loads"]         =""
    
    #????
    self.datas["#Non follower surface loads"]=""
    
    #N° corps(1) / coté(1ou2) / Pression(+)/depression(-)(unite?)
    self.datas["#Follower surface loads"]="         1          1  -1.00000000000000e+02 "
    
    #TOUS CONSTANTS
    self.datas["#fich_utilis.f"]         ="         0  0.000000000000000e+00          0          0          0          0          0          0          0          0          0          0 "  
    
    #?LIGNE COMMENTAIRE?
    self.datas["#################################################"]=""
    
    #?LIGNE COMMENTAIRE?
    self.datas["# Entete contact"]       =""
    
    #Définition de un ou deux contacts (un seul sera utilisé, appelé #Couple)
    # Nb de contacts(1ou2) /  100(const) /   1.000000000000000E-07(const) /    4(const) /   0(const) /   0(const) /   0  10000(const) /   10000(const) / 
    self.datas["#    NBCCT      NMIGS                  TOLCB      ISPLI      ILAGR      IVISM      N_MPC      MDNOC      MDFAT"]="         1        100  1.000000000000000E-07          4          0          0          0      10000      10000"

    #TOUS CONSTANTS (suite de la définition d'un contact (couple)
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
    
    #MASTER SURFACE=MOULE (matériaux 2 et 3[non utilisé])
    # N°corps(2) / 1(const) 
    self.datas["#master surface"]="         2          1 "
    

    self.app=app
    self.wait_SeeOut=self.wait_SeeErr=False

  def ExtractFilmMouleFromDAT(self,filein):
    """
    @param filein:full path du fichier spécifique plast.DAT à traiter 
    @return points_film, points_moule: "list" des faces trouvées [[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)],...,[(xn,yn,zn),(xn+1,yn+1,zn+1),(xn+2,yn+2,zn+2)]]
    @note: utilisation d'une state machine pour parser le début du fichier DAT
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
#parsing suffisant pour créer les deux listes de pts moule et film            
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
    _ihm_temp=self.f.m_int_temp_film.GetValue()
    #TODO: pas de controle de la température venant de l'IHM
    temp=float(_ihm_temp)
    with open("./plast3d/thermique.dat","w") as _f:
      _f.write("#Noeuds\n{:d}\n".format(nb_noeuds))    
      for i in range(nb_noeuds):
        _f.write("{:10d} {:10.3f}\n".format(i+1,temp))

  
  def CreateDat(self,fileout,points_film=None,points_moule=None):
    """
    Création des lignes du fichier plast DAT
    Création du fichier plast .DAT
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
  
#Données du film : 
#  1) Récupération de la liste de tous les noeuds uniques
#  2) Re-Création des faces en utilisant uniquement les numéros des noeuds de cette liste 
#  3) Re-Création des la liste des "degres de liberté" en utilisant uniquement les numérso des noeuds de cette liste 
    _z=self.f.m_int_distance_moule_film.GetValue() #Distance Moule Film à intégrer
    logging.warning(">>CreateDat>>DEBUT CREATION DATA FILM")
    noeuds_data=[]
    faces_data=[] 
    dol_data=[]           
    for face in self.points_film:
      new_face=[]
      for noeud in face:
        try: #on essaye de trouver la place du noeud dans la liste déjà constitué
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
    noeuds_data=(numpy.array(noeuds_data)+(0,0,_z)).tolist()
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
    self.datas["#Degrees of freedom"]=self.datas["#Degrees of freedom"][:-1] #il faut retirer le dernier retour à la ligne
       
    #Création du fichier thermique.dat indispensable pour le fonctionnement de plast
    if self.f==None or not self.f.m_checkBox_fichier_thermique.GetValue()==True:
      self.CreateThermique(len(noeuds_data))  
       
    
     
#Données du moule : 
#  1) Récupération de la liste de tous les noeuds uniques
#  2) Re-Création des  faces en utilisant uniquement les numéros des noeuds de cette liste 
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
    
    #Modification des noeuds et des faces si un ou plisieurs noeuds ont plus de 19 segments...
    noeuds_data,faces_data=self.VerifNbSegmentsParNoeud(noeuds_data,faces_data,_n-1,19)
    
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
      
    #Construction de la ligne #Generalities line 2 =  Nb noeuds total  Nb éléments total  8   Nb points limités  Nb materiaux(ou corps?)(2voir3)  0
    self.datas["#Generalities line 2"]="{:10d} {:10d} {:10d} {:10d} {:10d} {:10d} ".format(_n-1,_f-1,8,len(dol_data),2,0)
    
    if self.f!=None: #Utilisation de données IHM en direct
      
    #Construction de Materials: Epaisseur et Vitesse moule dz (du .dat) = mm /pas  = V_ihm(mm/s) x T_IHM(s)/Nb_pas ou encore  dz=mm/s X durée critique (constante pour l'instant)
      self.datas["#Materials"]=self.datas["#Materials"][0:69]+"{:+22.14e}".format(float(self.f.m_float_epaiseur_film.GetValue()))+self.datas["#Materials"][69+22:]   
      self.datas["#Materials"]=self.datas["#Materials"][0:1432]+ "{:+22.14e}".format(float(self.f.m_float_deplacement_moule.GetValue())*float(self.f.m_float_tps_critique.GetValue()))+ self.datas["#Materials"][1432+22:]   
    
    #Construction de #Follower surface loads Pression/Depression/Aspiration (a priori négatif si film au dessus)
    #N° corps(1) / coté(1ou2) / Pression(+)/depression(-)(unite?)
    self.datas["#Follower surface loads"]="         1          1 {:+22.14e} ".format(float(self.f.m_float_pression.GetValue()))
    
    #Construction  #SLAVE SURFACE=FILM 
    self.datas["#Slave surface"]="         1          1          0 \n         0  {:+22.14e} ".format(float(self.f.m_float_frottement.GetValue()))
    
    #Construction Nb de pas suivant le temps de simu: on touche uniquement (pour l'instant) au nb de pas premier = Tps de simu/Durée Critique 
    self.datas["#Time control"] ="{:10d}".format(int(float(self.f.m_float_tps_simulation.GetValue())/float(self.f.m_float_tps_critique.GetValue())))+self.datas["#Time control"][10:]
    
    
    #TODO:Construction 'provisoire' de #Displacements et #Velocities
    self.datas["#Displacements"]="{:10d}".format(_n-1)+self.datas["#Displacements"][10:]
    self.datas["#Velocities"]="{:10d}".format(_n-1)+self.datas["#Velocities"][10:]
    
    
    logging.warning(">>CreateDat>>ECRITURE DU FICHIER DAT")     
    with open("./plast3d/test.dat","w") as _f:
      for i in self.datas.items():
        _f.write(i[0]+"\n")
        if i[1]!="": _f.write(i[1]+"\n")
    self.f.oProjetIMD.projet["root"]["fichier plast.dat"]="./plast3d/test.dat"
    return True
        
  def SurfaceTriagle3D(self,face,noeuds):
    """
    @param face: [noeud1,noeud2,neud3]
    @param noeuds: les coords de tous les noeuds ATTENTION NUMPY.ARRAY
    @note: http://www.mathopenref.com/heronsformula.html
    """
    a=numpy.linalg.norm(noeuds[face[1]]-noeuds[face[0]])#segment AB et AC et BC du triangle
    b=numpy.linalg.norm(noeuds[face[2]]-noeuds[face[0]])
    c=numpy.linalg.norm(noeuds[face[1]]-noeuds[face[2]])
    p=(a+b+c)/2
    S=numpy.sqrt(p*(p-a)*(p-b)*(p-c))
    return S
    
  def VerifNbSegmentsParNoeud(self,noeuds_data,faces_data,offset,critere=19):     
    """
    Vérification qu'il n'y pas plus de '@critere' segments partant d'un noeud
    Modification de la liste des noeuds: 
      -suppression des 2 autres noeuds du triangle du noeud ayant plus de @critère segments 
      -création un nouveau noeud (barycentre des 2 noeuds supprimés)
    Modification de la liste des faces: 
      -supprimer les deux triangles qui appartenaient aux noeuds supprimés
      -modifier les références des noeuds dans les faces (la liste des noeuds à changer, il manque un noeud)
    On recommence l'ensemble de ces opération de modification tant qu'il a des noeuds avec plus de @critère segments pour un noeud
    @param noeuds: liste des noeuds du moule
    @param faces_data: liste des faces du moule avec référence des noeuds
    @param offset: décalage entre les références présentes dans les faces et l'ordre des noeuds
    @param critere: contrainte du nombre de segments qui partent de chaque noeud
    """
    _n=numpy.array(noeuds_data)
    _f=numpy.array(faces_data)-offset-1
    while True:
      _f_histo=numpy.histogram(_f,bins=_f.max()-_f.min())
      _noeuds_pb=[_f_histo[1][i] for i in range(len(_f_histo[0])) if _f_histo[0][i]>critere]
      if len(_noeuds_pb)!=0:
        logging.warning("{} noeuds avec problème(s) potentiel(s) ({} segments pour un noeuds).".format(_noeuds_pb,critere))
        i=_noeuds_pb[0]
        _all_faces=[_f[j] for j in range(len(_f)) if i in _f[j]] #on récupère toutes les faces du noeud qui pose problème
        _all_surfs=map(lambda k:self.SurfaceTriagle3D(k,_n),_all_faces)# on calcule toutes les surfaces de ces faces
        tri_min=_all_faces[_all_surfs.index(min(_all_surfs))]# on récupère la surface la plus petite
        _noeuds_b_c=filter(lambda k:k!=i,tri_min)# on récupère les 2 autres points du triangle/face du noeud à problème
        coords_middle=(_n[_noeuds_b_c[0]]+_n[_noeuds_b_c[1]])/2 #on calcule les coordonnées milieu de ces deux points
        _n[_noeuds_b_c[0]]=coords_middle #on remplace les coords du  noeud b du triangle par les nouvelles coords milieu
        _n=numpy.delete(_n,_noeuds_b_c[1],0)# on retire de la liste le noeud c

        _new_f=[]
        for l in _f:
          if (_noeuds_b_c[0] in l) and (_noeuds_b_c[1] in l):
            continue
          else:
            if (_noeuds_b_c[1] in l):
              l[numpy.where(l==_noeuds_b_c[1])]=_noeuds_b_c[0]
            j=0
            for k in l:# il faut décaler toutes les références de noeuds dans les triangles
              if k>_noeuds_b_c[1] : 
                l[j]=l[j]-1
              j+=1
          _new_f.append(list(l))
      else:
        break
      _f=numpy.array(_new_f)
    _n=list(_n)
    _f=list(_f+offset+1)#on n'oublie pas de remettre l'offset d'origine entre référence des noeuds dans les faces
    return _n,_f
 
  def quad2tri(self,points): 
    """
    Transforme Les points/faces QUAD en points/faces TRI (ne touche pas aux points)
    @param points: points, "list" des faces générées en QUAD [[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3),(x4,y4,z4)],...,[(xn,yn,zn),(xn+1,yn+1,zn+1),(xn+2,yn+2,zn+2),(xn+3,yn+3,zn+3)]]
    @return: points, "list" des faces générées [[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)],...,[(x2n,y2n,z2n),(x2n+1,y2n+1,z2n+1),(x2n+2,y2n+2,z2n+2)]]

    """
    points_tri=[]
    for face in points:
        points_tri.append([face[0],face[1],face[3]])
        points_tri.append([face[1],face[2],face[3]])
    return points_tri

  def GenererFilm(self,largeur=100,hauteur=100,pas=1,z=0,tri=False):
    """
    @param largeur: en mm, correspond à la largeur intérieure du cadre entourant le film (base du cadre)
    @param hauteur:  en mm, correspond à la hauteur/longueur intérieure du cadre entourant le film         
    @param pas: en mm, pas entre chaque noeud
    @param z: hauteur du film
    @return: points_film, "list" des faces générées [[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3),(x4,y4,z4)],...,[(xn,yn,zn),(xn+1,yn+1,zn+1),(xn+2,yn+2,zn+2),(xn+3,yn+3,zn+3)]]
    """
    self.points_film=[]
    self.points_externes_film=[]
    #on arrondit largeur et au hauteur au multiple de pas juste supérieur
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
    if tri:
      self.points_film=(self.quad2tri(self.points_film))
            
    #On ne retourne que les points du film, le tour sera gérer par l'objet de la class au moment dans la génération du fichier .DAT
    return self.points_film
        
  def VerifAndLaunch(self):        
    if self.Verif():
      self.Launch()
      self.MessageLog(u"Lancement de l'éxécutable PLAST avec le fichier créé %s!\n" % self.f.oProjetIMD.projet["root"]["fichier plast.dat"], "INFO")
      return True
    else:
      self.MessageLog(u"La Vérification a échoué... Lancement IMPOSSIBLE de l'éxécutable PLAST !\n","ERROR")
      return False   
   
  def Verif(self):
    Log=u"-Vérification de l'existence des données MOULES (celles que vous visualisez actuellement)?"
    if len(self.f.oSTLMoule.pointsSTL)<=3: # CORRESPOND AU FICHIER DE DEMARRAGE 3 FACES ou inférieur
      self.f.oNoteBook.MessageLog(Log+u" NON \n","ERROR") 
      return False
    else:
      self.f.oNoteBook.MessageLog(Log+u" OUI \n","INFO") 
      self.points_moule=list(self.f.oSTLMoule.pointsSTL)
    Log=u"-Vérification de l'existence des données FILM (celles que vous visualisez actuellement)?"
    if len(self.f.oSTLFilm.pointsSTL)<=3: # CORRESPOND AU FICHIER DE DEMARRAGE 3 FACES ou inférieur
      self.f.oNoteBook.MessageLog(Log+u" NON \n","ERROR") 
      return False    
    else:
      self.f.oNoteBook.MessageLog(Log+u" OUI \n","INFO") 
      self.points_film=list(self.f.oSTLFilm.pointsSTL)
    Log=u"-Vérification de l'existence des noeuds externes du film?\n"
    if self.points_externes_film==[]: 
      self.f.oNoteBook.MessageLog(Log+u" NON (si film STL -> non géré actuellement)\n","ERROR") 
      return False    
    else:
      self.f.oNoteBook.MessageLog(Log+u" OUI \n","INFO") 
    self.f.oNoteBook.MessageLog(u"-Utilisation de l'épaisseur du Film (#Materials)={}mm\n".format(self.f.m_float_deplacement_moule.GetValue()),"INFO")
    self.f.oNoteBook.MessageLog(u"-Utilisation de la vitesse de déplacement du moule dZ(#Materials)={}m/s \n".format(self.f.m_float_epaiseur_film.GetValue()),"INFO")
    self.f.oNoteBook.MessageLog(u"-Utilisation de la Pression/Dépression (#Follower surface loads)={}? \n".format(self.f.m_float_pression.GetValue()),"INFO")
    
    self.f.oNoteBook.MessageLog(u"-Création du fichier {}... Patientez...\n".format("./plast3d/test.dat"),"INFO") 
    return self.CreateDat("./plast3d/test.dat",self.points_film,self.points_moule)    
    
   
   
  def SeeOut(self,p):
    i=0
    while True:
      inline = p.stdout.readline()
      logging.warning(inline)
      while (self.wait_SeeErr):pass
      self.wait_SeeOut=True
      self.app.oNoteBook.MessageLog(u"Line n°<{}> from PLAST>>>{}".format(i,inline.decode('cp1252')),"INFO")
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
      self.app.oNoteBook.MessageLog(u"Line n°<{}> from PLAST>>>{}".format(i,inline.decode('cp1252')),"ERROR")
      self.wait_SeeErr=False     
      i+=1
      sys.__stderr__.flush()
      if p.poll() != None:
        break
    
         
  def Launch(self):
    _path=os.getcwd()      
    os.chdir(self.f.oProjetIMD.projet["root"]["dir"]["plast3d"])
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for i in files:
      if i[0:3]=="GMV" or i[-3:]=="vtk":
        send2trash(i)
    self.f.oNoteBook.cache_liste_points={}
    self.ProcessPlastInProgress=subprocess.Popen("plast3d.exe",shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    self.ProcessPlastInProgress.stdin.write(os.path.split(self.f.oProjetIMD.projet["root"]["fichier plast.dat"])[1]+"\n1\n30000\n100\n")
    Process(target=self.app.oPlastProcess.SeeOut, args=(self.ProcessPlastInProgress,)).start() #on doit créer un thread pour la lecture de sortie stdout du PIPE
    Process(target=self.app.oPlastProcess.SeeErr, args=(self.ProcessPlastInProgress,)).start() #on doit créer un thread pour la lecture de sortie stderr du PIPE
    os.chdir(_path)
    return self.ProcessPlastInProgress

if __name__=="__main__":
  p=PlastProcess(None)
  
  state=20
  if state==10 : #utilisation d'un dat avec moule/film QUAD  puis créer des TRI
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
    
  if state==20:#utilisation d'un STL calcul des dimensions de l'objet puis création du film
    a=pystl.cSTL(u"C:/Users/damien/Documents/Projets/IMD3D/Plast/export 3DS_moule+plan_sans epaisseur.stl")
    mouleSTL=a.read(scale=1)
    c1,c2,c3,c4=Common.FindCorners(mouleSTL)
    print c1,c2,c3,c4 #-x,-y,x,y
    largeur=c3[0]-c1[0]
    hauteur=c4[1]-c2[1]
    print largeur,hauteur
    filmSTL=p.GenererFilm(310,200,4,56,tri=True)    
    p.CreateDat("../plast3d/test.dat",filmSTL,mouleSTL)
  