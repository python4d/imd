#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 2 déc. 2012
Regroupe toutes les fonctions concernant le Panel NoteBook
Ce module/Class a été créé uniquement pour alléger le fichier MainApp
@author: Python4D
'''
import Common,vtk2obj,Projet,pystl
import wx,os
import logging


class NoteBook(object):
  def __init__(self,frame):
    self.f=frame
    self.f.cache_liste_points={}
  
  def OnNotebookPageChanged(self,event):
    st=self.f.m_notebook.GetCurrentPage().GetName()
    logging.warning( st)
    event.Skip()
    
  #
  # Fonctions concernant la wxListBox des fichiers VTK
  #
   
  def OnListBox_vtk(self, event):
    if self.f.debug==False:
      #cas utilisation du multiprocessing (attention pas de debug possible lance un interpréteur Python par process!!)
      from multiprocessing import Process, Queue
    else:
      #cas utilisation des thread (n'utilise qu'un interpréteur et n'utilise donc pas le cpu à plein, 
      #permet juste de lancer en parralléle des taches pour ne pas 'trop' bloqué l'IHM
      from threading import Thread as Process
     
    _filein=str(event.String.split(" from ")[1]+"\\"+event.String.split(" from ")[0])
    if (_filein in self.f.cache_liste_points):
      self.f.oVueOpenGL.q.put([self.f.cache_liste_points[_filein],1,"no_file"])#on prévient que les données viennent du cache
    else:  
      # On lance un Thread pour récupérer les données du nouveau fichier
      #threading.Thread(target=vtk2obj.get_quad_from_vtk, args=(_filein,7735,_frame.oVueOpenGL.q,_frame.cache_liste_points)).start()
      if _filein[len(_filein)-3:len(_filein)]=="vtk":
        Process(target=vtk2obj.get_quad_from_vtk, args=(_filein,0,self.f.oVueOpenGL.q)).start()   
      elif _filein[len(_filein)-3:len(_filein)]=="obj":
        Process(target=vtk2obj.get_tri_from_obj, args=(_filein,0,self.f.oVueOpenGL.q)).start()  
      else  :
        Process(target=pystl.get_tri_from_stl, args=(_filein,self.f.oVueOpenGL.q)).start()  
    self.f.oVueOpenGL.flag_new_set_of_points+=1 #on augmente le compteur du nombre de set de points dans la queue (VisuOpenGL va décrémenter ce compteur)
    self.f.oTimer.oVueOpenGLTimer.Start(500)
    event.Skip()

  
   
  def RefreshOnListBox_vtk(self,chemin='.'):  
    """
    Rafraichit la liste des fichiers VTK/OBJ et STL dans la fenêtre OpenGL-VTK
    """
    _s=self.f.m_listBox_vtk.GetSelection() #on récupére le fichier sélectionné
    # Init ListBox_vtk
    list_fichiers_vtk=Common.ListOfFiles(chemin)
    #on vérifie qu'il n'y a pas eu de problème pour récupérer la liste des fichier vtk       
    #TODO:problème potentiel si on ouvre une boite de dialog fichiers ou directory, alors conflit avec os.walk (cf Common.ListOfFiles
    if not list_fichiers_vtk==-1:  
      #on va rajouter les fichiers obj et stl à la liste vtk
      list_fichiers_obj=Common.ListOfFiles(chemin,extension="obj")
      if list_fichiers_obj!=-1:
        for _i in list_fichiers_obj :
          list_fichiers_vtk.append(_i)
      list_fichiers_stl=Common.ListOfFiles(chemin,extension="stl")
      if list_fichiers_stl!=-1:
        for _i in list_fichiers_stl:
          list_fichiers_vtk.append(_i)
      self.f.m_listBox_vtk.Set([a.split('\\')[-1]+" from "+"\\".join(a.split('\\')[:-1]) for a in list_fichiers_vtk])
      self.f.m_listBox_vtk.SetSelection(_s)
      self.f.m_listBox_vtk.SetFocus()
      return 0
    else:
      return -1
  
  #  
  # Fonctions concernant l'onglet données du projet PLAST: Répertoires et Importations
  #
     
  def OnDirChanged_PLAST3D( self, event ):
    if not self.f.m_dirPicker_PLAST3D.GetTextCtrl().FindFocus()==self.f.m_dirPicker_PLAST3D.GetTextCtrl():
      #cas où l'on a changé le directory via le bouton et non pas en tapant directement le chemin
      self.f.OnKillFocus_DIR_PLAST3D(self.f, event)
    event.Skip()
      
  def OnKillFocus_DIR_PLAST3D(self, event):
    logging.warning("KillFocus-event OnChangeText_DIR_PLAST3D \n")
    _dir=self.f.m_dirPicker_PLAST3D.GetTextCtrl().GetValue()
    _plast3d=os.path.join(_dir,"plast3d.exe")
    if not self.f.oProjetIMD.ValiderDirFile(_plast3d)==0:
      self.f.m_dirPicker_PLAST3D.SetPath(self.f.oProjetIMD.projet["root"]["dir"]["plast3d"])   
    else:    
      self.f.m_dirPicker_PLAST3D.SetPath(_dir) 
      self.f.oProjetIMD.projet["root"]["dir"]["plast3d"]=_dir
      self.f.oProjetIMD.not_saved=1
      self.f.oProjetIMD.Projet2IHM(self.f.oProjetIMD.projet,self.f.oProjetIMD.frame)
      self.RefreshOnListBox_vtk(_dir)
    event.Skip()  
       
  def OnSetFocus_DIR_PLAST3D( self, event ):
    logging.warning("SetFocus-event OnChangeText_DIR_PLAST3D \n")
    event.Skip()       
        
  def OnButtonClick_m_button_generer_film( self, event ):   
    logging.warning("OnButtonClick_m_button_generer_film")
    
    self.f.oSTLFilm.pointsSTL=self.f.oPlastProcess.GenererFilm(hauteur=self.f.m_int_hauteur_cadre.GetValue(),
                                                               largeur=self.f.m_int_largeur_cadre.GetValue(),
                                                               pas=self.f.m_int_pas_film.GetValue(),
                                                               z=0)
    self.f.oSTLFilm.flag_new_STL=True
    self.f.oSTLFilm.Refresh(True)
    
  def OnFileChanges_STLFilm( self, event ):
    logging.warning("OnFileChanges_STLFilm")
    _dir=self.f.m_filePicker_Film.GetTextCtrl().GetValue()
    a=pystl.cSTL(_dir)
    self.f.oSTLFilm.pointsSTL=a.read(scale=1)
    self.f.oSTLFilm.flag_new_STL=True
    self.f.oSTLFilm.Refresh(True)
    self.f.oProjetIMD.projet["root"]["fichier STL film"]=_dir
    
      
  def OnFileChanges_STLMoule( self, event ):
    logging.warning("OnFileChanges_STLMoule")
    _dir=self.f.m_filePicker_Moule.GetTextCtrl().GetValue()
    a=pystl.cSTL(_dir)
    self.f.oSTLMoule.pointsSTL=a.read(scale=1)
    self.f.oSTLMoule.flag_new_STL=True
    self.f.oSTLMoule.Refresh(True)
    self.f.oProjetIMD.projet["root"]["fichier STL moule"]=_dir
      
  def OnButtonClick_LaunchPlast( self, event ):
    logging.warning("launch plast")
    self.MessageLog("Vérification des Paramêtres et données Plast3D:\n", "INFO")
    
    Log="-CheckBox d'utilisation d'un fichier DAT?"
    if self.f.m_checkBox_FichierDAT.GetValue()==True:
      self.MessageLog(Log+"OUI \n","INFO")      
      if not self.f.oProjetIMD.projet["root"]["fichier plast.dat"]=="":
        self.f.oPlastProcess.LaunchProcessPlast(self.f)
        self.MessageLog("Lancement de l'éxécutable PLAST avec le fichier %s!\n" % self.f.oProjetIMD.projet["root"]["fichier plast.dat"], "INFO")
        return 0
      else:
        self.MessageLog("Lancement IMPOSSIBLE de l'éxécutable PLAST: Fichier .DAT mal/non renseigné !\n","ERROR")
        return 1
    else: self.MessageLog(Log+"NON \n","INFO")   
    
    Log="-Vérification des fichiers STL Film et Moule:"


  def OnFileChanges_FichierDAT( self, event ):
    """
    Récupération du directory du fichier DAT
    Récupération des données film et moule (cf PlastProcess)
    Préparation des données pour éventuellement les afficher (cf OnCheckBox_FichietDAT)
    """
    logging.warning("dat select")  
    _dir=self.f.m_filePicker_FichierDAT.GetTextCtrl().GetValue()
    self.f.oProjetIMD.projet["root"]["fichier plast.dat"]=_dir
    self.f.oSTLFilm.pointsDAT,self.f.oSTLMoule.pointsDAT=self.f.oPlastProcess.ExtractFilmMouleFromDAT(_dir) 
    logging.warning(Common.FindCorners(self.f.oSTLFilm.pointsDAT))
    logging.warning(Common.FindCorners(self.f.oSTLMoule.pointsDAT))
    self.f.oSTLFilm.flag_new_DAT=True
    self.f.oSTLMoule.flag_new_DAT=True
    if self.f.m_checkBox_FichierDAT.GetValue()==False: #on force le passage de STL=>DAT si on est en mode STL
      self.f.m_checkBox_FichierDAT.Enabled=True
      self.f.m_checkBox_FichierDAT.SetValue(True) 
      self.OnCheckBox_FichierDAT(event)#Vérifier que la case est cochée  
    else:
      self.f.oSTLFilm.Refresh(True)
      self.f.oSTLMoule.Refresh(True)   

   
  def OnCheckBox_FichierDAT( self, event ):
    """
    Si Case Cochée: Vérouiller les parmêtres PLAST et éventuellement afficher les données du fichiet DAT sélectionné
    Sinon Déverouiller les paramêtres Plast
    """
    if self.f.m_checkBox_FichierDAT.GetValue()==True: 
      logging.warning("OnCheckBox_FichierDAT => True")  
      self.f.m_filePicker_Film.Shown=False 
      self.f.m_filePicker_Moule.Shown=False     
      self.f.m_staticText_Moule.Label="Données Moule Extraites du fichier .DAT"
      self.f.m_staticText_Film.Label="Données Film Extraites du fichier .DAT" 
      self.f.m_panel_param_plast.Enabled=False
      self.f.oSTLFilm.flag_DAT=True
      self.f.oSTLMoule.flag_DAT=True
      self.f.oSTLFilm.Refresh(True)
      self.f.oSTLMoule.Refresh(True)          
    else:
      logging.warning("OnCheckBox_FichierDAT => False")  
      self.f.m_filePicker_Film.Shown=True 
      self.f.m_filePicker_Moule.Shown=True
      self.f.m_staticText_Moule.Label="Fichier STL du Moule à Utiliser"
      self.f.m_staticText_Film.Label="Fichier STL du Film à Utiliser" 
      self.f.m_panel_param_plast.Enabled=True   
      self.f.oSTLFilm.flag_STL=True
      self.f.oSTLMoule.flag_STL=True
      self.f.oSTLFilm.Refresh(True)
      self.f.oSTLMoule.Refresh(True)    
  
  #
  #  Fonctions concernant les wxSlider, choix couleur et reset view de l'onglet visualisation vtk
  #
      
  def OnScroll_slider_vtk( self, event ):      
    self.f.oVueOpenGL.flag_color_change=1
    self.f.oVueOpenGL.Refresh(True)
    event.Skip()
          
  def OnButtonClick_vtk( self, event ):
    self.f.oVueOpenGL.flag_reset_view=1
    self.f.oVueOpenGL.Refresh(True)  
    event.Skip()
      
  def OnScroll_slider_vtk_color( self, event ):      
    self.f.oVueOpenGL.flag_color_change=1
    self.f.oVueOpenGL.Refresh(True)
    event.Skip()
      
  def OnChoice_vtk_color(self, event):
    self.f.oVueOpenGL.TableCouleur=self.f.m_choice_vtk_color.GetStringSelection()
    self.f.oVueOpenGL.mCacheColor()
    self.f.oVueOpenGL.flag_color_change=1 #permet de recréer la Display_List (cf VisuOpenGL)
    self.f.oVueOpenGL.Refresh(True)
    event.Skip()
  
  #
  #  Fonctions concernant le wxSlider et choix texture de l'onglet visualisation vtk
  #
      
  def OnCheckBox_lines( self, event ):
    if self.f.m_checkBox_lines.GetValue():
      self.f.oVueOpenGL.only_lines=1
    else:
      self.f.oVueOpenGL.only_lines=0
    self.f.oVueOpenGL.dl_surf,_,_,_=self.f.oVueOpenGL.mCreerDisplayList()
    self.f.oVueOpenGL.Refresh(True)
    event.Skip()
        
  def OnChoice_texture( self, event ):
    self.f.oVueOpenGL.flag_texture_change=2 
    self.f.oVueOpenGL.Refresh(True)
    event.Skip() 
      
  def OnScroll_slider_texture( self, event ):
    self.f.oVueOpenGL.flag_texture_change=3
    self.f.oVueOpenGL.Refresh(True)
    event.Skip()   
      
  def OnCheckBox_texture( self, event ):
    if self.f.m_checkBox_texture.GetValue():
      self.f.oVueOpenGL.flag_texture_change=1
    else:
      self.f.oVueOpenGL.flag_texture_change=-1
    self.f.oVueOpenGL.Refresh(True)
    event.Skip()
  
  
  #
  # Fonction concernant les splitters
  #
      
  def OnSplitterChanging(self,event):
    """
    Redessine le Frame car il semble que le Splitter ne le demande pas (tout le temps??)
    """
    self.f.Refresh(True)
    event.Skip()
    
    
  #
  # Fonctions pour La fenetre de LOG
  #
   
  def MessageLog(self,sMessage,sType,bVisuel=False):
    DateHeure=self.f.m_statusBar.GetStatusText()
    if sType=="INFO":
      self.f.m_textCtrl_console.SetDefaultStyle(wx.TextAttr(wx.GREEN ))
    elif sType=="ERROR":
      self.f.m_textCtrl_console.SetDefaultStyle(wx.TextAttr(wx.RED))
    self.f.m_textCtrl_console.AppendText(DateHeure+">>"+sType+">>>"+sMessage)
    self.f.m_textCtrl_console.SetDefaultStyle(wx.TextAttr(wx.BLACK))
    if bVisuel: self.f.oTimer.oMessageLogTimer.Start(1)
    


