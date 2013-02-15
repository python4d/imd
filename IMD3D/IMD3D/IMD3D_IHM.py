# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import VueOpenGL as ogl
from wx.lib.intctrl import IntCtrl
from floatctrl import FloatCtrl

###########################################################################
## Class wxMainFrame
###########################################################################

class wxMainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Interface IMD3D", pos = wx.DefaultPosition, size = wx.Size( 1221,730 ), style = wx.CAPTION|wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 400,400 ), wx.DefaultSize )
		
		bSizerAllPanel = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SP_3D )
		self.m_splitter1.SetSashGravity( 1 )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		self.m_splitter1.SetMinimumPaneSize( 100 )
		
		self.m_panel7 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel7.SetMinSize( wx.Size( 500,100 ) )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook = wx.Notebook( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, u"m_notebook_principal" )
		self.m_notebook.SetFont( wx.Font( 12, 70, 90, 92, False, wx.EmptyString ) )
		self.m_notebook.SetBackgroundColour( wx.Colour( 179, 255, 179 ) )
		
		self.Plast3D_IN = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, u"m_panel_Plast3D_IN" )
		self.Plast3D_IN.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		self.Plast3D_IN.SetMinSize( wx.Size( -1,5000 ) )
		self.Plast3D_IN.SetMaxSize( wx.Size( -1,5000 ) )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook_Projet = wx.Notebook( self.Plast3D_IN, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_TOP )
		self.m_notebook_Projet.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.m_notebook_Projet.SetBackgroundColour( wx.Colour( 215, 255, 215 ) )
		
		self.m_panel_Simple_OpenGL = wx.Panel( self.m_notebook_Projet, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"Panel des Répertoires et Importations" )
		self.m_panel_Simple_OpenGL.SetBackgroundColour( wx.Colour( 210, 255, 210 ) )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer23 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel_Simple_OpenGL, wx.ID_ANY, u"Répertoire de l'exécutable PLAST3D (plast3d.exe) et sorties fichiers VTK", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText3.Wrap( -1 )
		self.m_staticText3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer23.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_dirPicker_PLAST3D = wx.DirPickerCtrl( self.m_panel_Simple_OpenGL, wx.ID_ANY, u".", u"Choisissez le directory de PLAST3D", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_USE_TEXTCTRL )
		bSizer23.Add( self.m_dirPicker_PLAST3D, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer22.Add( bSizer23, 1, wx.EXPAND, 5 )
		
		self.m_LaunchPlast = wx.Button( self.m_panel_Simple_OpenGL, wx.ID_ANY, u"Verification des Paramêtres\n&& \nLancement de Plast3D", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_LaunchPlast.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer22.Add( self.m_LaunchPlast, 0, wx.ALL, 5 )
		
		bSizer7.Add( bSizer22, 0, wx.EXPAND, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.m_panel_Simple_OpenGL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer7.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox_FichierDAT = wx.CheckBox( self.m_panel_Simple_OpenGL, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_FichierDAT.Enable( False )
		
		bSizer24.Add( self.m_checkBox_FichierDAT, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText33 = wx.StaticText( self.m_panel_Simple_OpenGL, wx.ID_ANY, u"Utiliser un fichier DAT (optionnelle mais prioritaire !)", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText33.Wrap( -1 )
		self.m_staticText33.SetFont( wx.Font( 8, 74, 90, 92, False, "Times New Roman" ) )
		
		bSizer24.Add( self.m_staticText33, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_filePicker_FichierDAT = wx.FilePickerCtrl( self.m_panel_Simple_OpenGL, wx.ID_ANY, u"*.DAT", u"Choisissez un fichier .DAT", u"*.DAT", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_USE_TEXTCTRL )
		self.m_filePicker_FichierDAT.SetFont( wx.Font( 5, 74, 90, 90, False, "Terminal" ) )
		
		bSizer24.Add( self.m_filePicker_FichierDAT, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer7.Add( bSizer24, 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_staticline9 = wx.StaticLine( self.m_panel_Simple_OpenGL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer7.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter3 = wx.SplitterWindow( self.m_panel_Simple_OpenGL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter3.SetSashGravity( 1 )
		self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
		self.m_splitter3.SetMinimumPaneSize( 800 )
		
		self.m_panel_Moule = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText_Moule = wx.StaticText( self.m_panel_Moule, wx.ID_ANY, u"STL/OBJ du Moule", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText_Moule.Wrap( -1 )
		self.m_staticText_Moule.SetFont( wx.Font( 12, 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer16.Add( self.m_staticText_Moule, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_filePicker_Moule = wx.FilePickerCtrl( self.m_panel_Moule, wx.ID_ANY, u"*.ST;*.OBJ", u"Sélectionnez le fichier du MOULE au format .STL ou .OBJ", u"*.STL;*.OBJ", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_USE_TEXTCTRL )
		bSizer16.Add( self.m_filePicker_Moule, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer14.Add( bSizer16, 0, wx.EXPAND, 5 )
		
		self.oSTLMoule=ogl.cSimpleVueOpenGL(self.m_panel_Moule)
		self.oSTLMoule.SetMinSize( wx.Size( 100,100 ) )
		
		bSizer14.Add( self.oSTLMoule, 5, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5 )
		
		self.m_panel_Moule.SetSizer( bSizer14 )
		self.m_panel_Moule.Layout()
		bSizer14.Fit( self.m_panel_Moule )
		self.m_panel_Film = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer27 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText_Film = wx.StaticText( self.m_panel_Film, wx.ID_ANY, u"\nFilm Automatique\n", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText_Film.Wrap( -1 )
		self.m_staticText_Film.SetFont( wx.Font( 12, 74, 90, 92, False, "Tahoma" ) )
		
		bSizer27.Add( self.m_staticText_Film, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer13.Add( bSizer27, 0, wx.EXPAND, 5 )
		
		bSizer_generer_film = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer28 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText11 = wx.StaticText( self.m_panel_Film, wx.ID_ANY, u"Dimension intérieure du cadre  >10mm  <1000mm", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		self.m_staticText11.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer28.Add( self.m_staticText11, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5 )
		
		bSizer29 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1111 = wx.StaticText( self.m_panel_Film, wx.ID_ANY, u"X-Largeur (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1111.Wrap( -1 )
		bSizer29.Add( self.m_staticText1111, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		self.m_int_largeur_cadre=IntCtrl(parent=self.m_panel_Film,id=wx.ID_ANY,value=100,min=1,max=1000)
		bSizer29.Add( self.m_int_largeur_cadre, 1, wx.ALL, 5 )
		
		self.m_staticText111 = wx.StaticText( self.m_panel_Film, wx.ID_ANY, u"Y-Hauteur (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		bSizer29.Add( self.m_staticText111, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		self.m_int_hauteur_cadre=IntCtrl(parent=self.m_panel_Film,id=wx.ID_ANY,value=100,min=10,max=1000)
		bSizer29.Add( self.m_int_hauteur_cadre, 1, wx.ALL, 5 )
		
		self.m_staticText1112 = wx.StaticText( self.m_panel_Film, wx.ID_ANY, u"XY-Pas (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1112.Wrap( -1 )
		bSizer29.Add( self.m_staticText1112, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		self.m_int_pas_film=IntCtrl(parent=self.m_panel_Film,id=wx.ID_ANY,value=4,min=1,max=10)
		bSizer29.Add( self.m_int_pas_film, 1, wx.ALL, 5 )
		
		bSizer28.Add( bSizer29, 1, wx.EXPAND, 5 )
		
		bSizer_generer_film.Add( bSizer28, 1, wx.EXPAND, 5 )
		
		self.m_button_generer_film = wx.Button( self.m_panel_Film, wx.ID_ANY, u"Générer\nFilm", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer_generer_film.Add( self.m_button_generer_film, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer13.Add( bSizer_generer_film, 0, wx.EXPAND, 5 )
		
		self.oSTLFilm=ogl.cSimpleVueOpenGL(self.m_panel_Film)
		self.oSTLFilm.SetMinSize( wx.Size( 100,100 ) )
		
		bSizer13.Add( self.oSTLFilm, 5, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5 )
		
		bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_filePicker_Film = wx.FilePickerCtrl( self.m_panel_Film, wx.ID_ANY, u"*.STL", u"Choisissez le fichier STL du FILM", u"*.STL", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_USE_TEXTCTRL )
		self.m_filePicker_Film.Enable( False )
		
		bSizer15.Add( self.m_filePicker_Film, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_checkBox4 = wx.CheckBox( self.m_panel_Film, wx.ID_ANY, u"Fichier STL?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox4.Enable( False )
		
		bSizer15.Add( self.m_checkBox4, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer13.Add( bSizer15, 0, wx.EXPAND, 5 )
		
		self.m_panel_Film.SetSizer( bSizer13 )
		self.m_panel_Film.Layout()
		bSizer13.Fit( self.m_panel_Film )
		self.m_splitter3.SplitVertically( self.m_panel_Moule, self.m_panel_Film, 1000 )
		bSizer17.Add( self.m_splitter3, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		
		bSizer7.Add( bSizer17, 10, wx.EXPAND, 5 )
		
		self.m_panel_Simple_OpenGL.SetSizer( bSizer7 )
		self.m_panel_Simple_OpenGL.Layout()
		bSizer7.Fit( self.m_panel_Simple_OpenGL )
		self.m_notebook_Projet.AddPage( self.m_panel_Simple_OpenGL, u"Répertoires et Importations", True )
		self.m_panel_param_plast = wx.Panel( self.m_notebook_Projet, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"Panel des Procédés" )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer291 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer2 = wx.GridSizer( 2, 2, 0, 0 )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_param_plast, wx.ID_ANY, u"Paramêtres de vitesse de simulation (#Time Control)" ), wx.VERTICAL )
		
		bSizer34 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer37 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1911 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"#Durée max estimé de la simulation", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1911.Wrap( -1 )
		bSizer37.Add( self.m_staticText1911, 0, wx.ALL, 5 )
		
		
		self.m_float_tps_simulation=FloatCtrl(limited=True,parent=self.m_panel_param_plast,id=wx.ID_ANY,value=3.0,min=0.1,max=100)
		bSizer37.Add( self.m_float_tps_simulation, 1, wx.ALL, 5 )
		
		bSizer34.Add( bSizer37, 1, wx.EXPAND, 5 )
		
		bSizer371 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText19112 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"#Seuil d'immobilisme pour l'arrêt de Plast (mm)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19112.Wrap( -1 )
		bSizer371.Add( self.m_staticText19112, 0, wx.ALL, 5 )
		
		
		self.m_float_critere_arret=FloatCtrl(limited=True,parent=self.m_panel_param_plast,id=wx.ID_ANY,value=0.1,min=0.001,max=1)
		self.m_float_critere_arret.Enable( False )
		
		bSizer371.Add( self.m_float_critere_arret, 1, wx.ALL, 5 )
		
		bSizer34.Add( bSizer371, 1, wx.EXPAND, 5 )
		
		sbSizer1.Add( bSizer34, 1, wx.EXPAND|wx.SHAPED, 5 )
		
		gSizer2.Add( sbSizer1, 0, wx.EXPAND, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_param_plast, wx.ID_ANY, u"Paramêtres Moule-Film" ), wx.VERTICAL )
		
		bSizer30 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer38 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText15 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"#Distance entre MOULE et FILM (mm)   \n(Ajoute une composante Z aux données du Film)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		bSizer38.Add( self.m_staticText15, 0, wx.ALL, 5 )
		
		
		self.m_int_distance_moule_film=IntCtrl(parent=self.m_panel_param_plast,id=wx.ID_ANY,value=60,min=-1000,max=1000)
		bSizer38.Add( self.m_int_distance_moule_film, 1, wx.ALL, 5 )
		
		bSizer30.Add( bSizer38, 1, wx.EXPAND, 5 )
		
		bSizer35 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText19 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"#Vitesse de déplacement du Moule vers Film en z (mm/s)   \n(dZ du paramêtre #Matérial)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		bSizer35.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		
		self.m_float_deplacement_moule=FloatCtrl(limited=True,parent=self.m_panel_param_plast,id=wx.ID_ANY,value=0,min=-20,max=20)
		bSizer35.Add( self.m_float_deplacement_moule, 1, wx.ALL, 5 )
		
		bSizer30.Add( bSizer35, 1, wx.EXPAND, 5 )
		
		bSizer351 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText191 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"#Pression/Depression Film - 'Aspiration' (?)   \n(négatif pour attirer le film)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText191.Wrap( -1 )
		bSizer351.Add( self.m_staticText191, 0, wx.ALL, 5 )
		
		
		self.m_float_pression=FloatCtrl(limited=False,parent=self.m_panel_param_plast,id=wx.ID_ANY,value=-100,min=-200,max=200)
		bSizer351.Add( self.m_float_pression, 1, wx.ALL, 5 )
		
		bSizer30.Add( bSizer351, 1, wx.EXPAND, 5 )
		
		bSizer3511 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1912 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"#Coeff frottement Film - Moule (?)   ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1912.Wrap( -1 )
		bSizer3511.Add( self.m_staticText1912, 0, wx.ALL, 5 )
		
		
		self.m_float_frottement=FloatCtrl(limited=True,parent=self.m_panel_param_plast,id=wx.ID_ANY,value=0.3,min=0,max=10)
		bSizer3511.Add( self.m_float_frottement, 1, wx.ALL, 5 )
		
		bSizer30.Add( bSizer3511, 1, wx.EXPAND, 5 )
		
		sbSizer2.Add( bSizer30, 1, wx.EXPAND|wx.SHAPED, 5 )
		
		gSizer2.Add( sbSizer2, 0, wx.EXPAND, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_param_plast, wx.ID_ANY, u"Paramêtre Température Film (thermique.dat)" ), wx.VERTICAL )
		
		bSizer32 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText151 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"#Température (°C) (création fichier .DAT)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText151.Wrap( -1 )
		bSizer31.Add( self.m_staticText151, 0, wx.ALL, 5 )
		
		
		self.m_int_temp_film=IntCtrl(parent=self.m_panel_param_plast,id=wx.ID_ANY,value=100,min=10,max=200)
		bSizer31.Add( self.m_int_temp_film, 1, wx.ALL, 5 )
		
		bSizer32.Add( bSizer31, 1, wx.EXPAND, 5 )
		
		bSizer33 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBox_fichier_thermique = wx.CheckBox( self.m_panel_param_plast, wx.ID_ANY, u"Utilisation d'un fichier thermique.dat", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_fichier_thermique.Enable( False )
		
		bSizer33.Add( self.m_checkBox_fichier_thermique, 0, wx.ALL, 5 )
		
		self.m_filePicker_thermique_dat = wx.FilePickerCtrl( self.m_panel_param_plast, wx.ID_ANY, u"*.DAT", u"Choisissez le fichier thermique_dat du FILM", u"*.DAT", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_USE_TEXTCTRL )
		self.m_filePicker_thermique_dat.Enable( False )
		
		bSizer33.Add( self.m_filePicker_thermique_dat, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer32.Add( bSizer33, 1, wx.EXPAND, 5 )
		
		sbSizer3.Add( bSizer32, 0, wx.EXPAND, 5 )
		
		gSizer2.Add( sbSizer3, 1, wx.EXPAND, 5 )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel_param_plast, wx.ID_ANY, u"Sélection du Matériaux Film" ), wx.VERTICAL )
		
		bSizer3711 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText191121 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"#Temps Critique par pas (s) = 1e-4 s.\n (soit 30 000 pas pour 3s. simu)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText191121.Wrap( -1 )
		bSizer3711.Add( self.m_staticText191121, 0, wx.ALL, 5 )
		
		
		self.m_float_tps_critique=FloatCtrl(limited=True,parent=self.m_panel_param_plast,id=wx.ID_ANY,value=0.0001,min=0.00001,max=1)
		self.m_float_tps_critique.Enable( False )
		
		bSizer3711.Add( self.m_float_tps_critique, 1, wx.ALL, 5 )
		
		sbSizer4.Add( bSizer3711, 0, wx.EXPAND, 5 )
		
		bSizer40 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer39 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText19111 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"#Epaisseur du Matériaux Film (mm)   ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19111.Wrap( -1 )
		bSizer39.Add( self.m_staticText19111, 0, wx.ALL, 5 )
		
		
		self.m_float_epaiseur_film=FloatCtrl(limited=True,parent=self.m_panel_param_plast,id=wx.ID_ANY,value=0.1,min=0.01,max=10)
		bSizer39.Add( self.m_float_epaiseur_film, 1, wx.ALL, 5 )
		
		bSizer40.Add( bSizer39, 0, wx.EXPAND, 5 )
		
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText30 = wx.StaticText( self.m_panel_param_plast, wx.ID_ANY, u"Liste des Matérieaux (cf onglet Matériaux)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )
		bSizer41.Add( self.m_staticText30, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
		
		m_choice3Choices = []
		self.m_choice3 = wx.Choice( self.m_panel_param_plast, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice3Choices, 0 )
		self.m_choice3.SetSelection( 0 )
		bSizer41.Add( self.m_choice3, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer40.Add( bSizer41, 1, wx.EXPAND, 5 )
		
		sbSizer4.Add( bSizer40, 1, wx.EXPAND|wx.SHAPED, 5 )
		
		gSizer2.Add( sbSizer4, 1, wx.EXPAND, 5 )
		
		bSizer291.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		bSizer12.Add( bSizer291, 1, wx.EXPAND, 5 )
		
		gSizer1 = wx.GridSizer( 2, 2, 0, 0 )
		
		
		self.m_int_noeuds=IntCtrl(parent=self.m_panel_param_plast,id=wx.ID_ANY,value=0,min=-10,max=10)
		self.m_int_noeuds.Hide()
		
		gSizer1.Add( self.m_int_noeuds, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_float_noeuds=FloatCtrl(limited=True,parent=self.m_panel_param_plast,id=wx.ID_ANY,value=0,min=-9.5,max=11.10)
		self.m_float_noeuds.Hide()
		
		gSizer1.Add( self.m_float_noeuds, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_bitmap_test = wx.StaticBitmap( self.m_panel_param_plast, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_bitmap_test.Hide()
		
		gSizer1.Add( self.m_bitmap_test, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		bSizer12.Add( gSizer1, 0, wx.EXPAND, 5 )
		
		self.m_panel_param_plast.SetSizer( bSizer12 )
		self.m_panel_param_plast.Layout()
		bSizer12.Fit( self.m_panel_param_plast )
		self.m_notebook_Projet.AddPage( self.m_panel_param_plast, u"Paramêtres Procédés", False )
		self.VISUALISATION_VTK = wx.Panel( self.m_notebook_Projet, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"Panel des Sorties VTK" )
		self.VISUALISATION_VTK.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.VISUALISATION_VTK.SetBackgroundColour( wx.Colour( 187, 255, 187 ) )
		
		bSizerContentPLAST3D_visu = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter2 = wx.SplitterWindow( self.VISUALISATION_VTK, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.SetSashGravity( 0.1 )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 100 )
		
		self.m_panel10 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self.m_panel10, wx.ID_ANY, u"Fichiers VTK", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText2.Wrap( -1 )
		bSizer19.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		m_listBox_vtkChoices = [ u"test", u"de", u"la liste" ]
		self.m_listBox_vtk = wx.ListBox( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), m_listBox_vtkChoices, wx.LB_HSCROLL|wx.VSCROLL )
		self.m_listBox_vtk.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		bSizer19.Add( self.m_listBox_vtk, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		self.m_gauge_vtk = wx.Gauge( self.m_panel10, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,-1 ), wx.GA_HORIZONTAL )
		bSizer19.Add( self.m_gauge_vtk, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		bSizer3.Add( bSizer19, 1, wx.EXPAND, 5 )
		
		self.m_staticline7 = wx.StaticLine( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline7, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer20 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox_texture = wx.CheckBox( self.m_panel10, wx.ID_ANY, u"Texture", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.m_checkBox_texture, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline8 = wx.StaticLine( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer18.Add( self.m_staticline8, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_checkBox_lines = wx.CheckBox( self.m_panel10, wx.ID_ANY, u"Only Lines", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.m_checkBox_lines, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		bSizer20.Add( bSizer18, 1, wx.EXPAND, 5 )
		
		m_choice_textureChoices = [ u"splash.png", u"Mire_R.bmp", u"logo_transparent.png", u"mire_210x297mm_300dpi.bmp", u"lena_512x512.jpg" ]
		self.m_choice_texture = wx.Choice( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_textureChoices, 0 )
		self.m_choice_texture.SetSelection( 0 )
		bSizer20.Add( self.m_choice_texture, 1, wx.ALL, 5 )
		
		bSizer21 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_slider_texture = wx.Slider( self.m_panel10, wx.ID_ANY, 200, 10, 1000, wx.DefaultPosition, wx.DefaultSize, wx.SL_BOTH|wx.SL_HORIZONTAL|wx.SL_TOP )
		bSizer21.Add( self.m_slider_texture, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer20.Add( bSizer21, 0, wx.EXPAND, 5 )
		
		bSizer3.Add( bSizer20, 0, wx.EXPAND, 5 )
		
		self.m_panel10.SetSizer( bSizer3 )
		self.m_panel10.Layout()
		bSizer3.Fit( self.m_panel10 )
		self.m_panel_OpenGL = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.oVueOpenGL=ogl.cMainVueOpenGL(self.m_panel_OpenGL)
		self.oVueOpenGL.SetMinSize( wx.Size( 10,10 ) )
		
		bSizer5.Add( self.oVueOpenGL, 10, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText4 = wx.StaticText( self.m_panel_OpenGL, wx.ID_ANY, u"Saturation", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText4.Wrap( -1 )
		bSizer6.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_slider_vtk = wx.Slider( self.m_panel_OpenGL, wx.ID_ANY, 75, 50, 100, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_slider_vtk, 3, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticline4 = wx.StaticLine( self.m_panel_OpenGL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer6.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText42 = wx.StaticText( self.m_panel_OpenGL, wx.ID_ANY, u"Couleur", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText42.Wrap( -1 )
		bSizer6.Add( self.m_staticText42, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_slider_vtk_color = wx.Slider( self.m_panel_OpenGL, wx.ID_ANY, 512, 1, 512, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer6.Add( self.m_slider_vtk_color, 3, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticline41 = wx.StaticLine( self.m_panel_OpenGL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer6.Add( self.m_staticline41, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText41 = wx.StaticText( self.m_panel_OpenGL, wx.ID_ANY, u"Table Couleur", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText41.Wrap( -1 )
		bSizer6.Add( self.m_staticText41, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_choice_vtk_colorChoices = [ u"Z-Hauteur", u"VonMisesStress", u"MeanStress", u"FinalThicknessDistribution", u"CarteThermique" ]
		self.m_choice_vtk_color = wx.Choice( self.m_panel_OpenGL, wx.ID_ANY, wx.Point( -1,-1 ), wx.DefaultSize, m_choice_vtk_colorChoices, 0 )
		self.m_choice_vtk_color.SetSelection( 0 )
		self.m_choice_vtk_color.SetFont( wx.Font( 8, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.m_choice_vtk_color, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticline411 = wx.StaticLine( self.m_panel_OpenGL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		bSizer6.Add( self.m_staticline411, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_button_vtk = wx.Button( self.m_panel_OpenGL, wx.ID_ANY, u"Reset View", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button_vtk, 0, wx.ALL, 5 )
		
		bSizer5.Add( bSizer6, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_panel_OpenGL.SetSizer( bSizer5 )
		self.m_panel_OpenGL.Layout()
		bSizer5.Fit( self.m_panel_OpenGL )
		self.m_splitter2.SplitVertically( self.m_panel10, self.m_panel_OpenGL, 100 )
		bSizerContentPLAST3D_visu.Add( self.m_splitter2, 1, wx.EXPAND, 5 )
		
		self.VISUALISATION_VTK.SetSizer( bSizerContentPLAST3D_visu )
		self.VISUALISATION_VTK.Layout()
		bSizerContentPLAST3D_visu.Fit( self.VISUALISATION_VTK )
		self.m_notebook_Projet.AddPage( self.VISUALISATION_VTK, u"Sorties Fichiers *.vtk", False )
		
		bSizer4.Add( self.m_notebook_Projet, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.Plast3D_IN.SetSizer( bSizer4 )
		self.Plast3D_IN.Layout()
		bSizer4.Fit( self.Plast3D_IN )
		self.m_notebook.AddPage( self.Plast3D_IN, u"PLAST3D - process plast3d.exe", True )
		self.ANNA_IN = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.ANNA_IN.SetBackgroundColour( wx.Colour( 170, 255, 255 ) )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText31 = wx.StaticText( self.ANNA_IN, wx.ID_ANY, u"Répertoire de l'exécutable ANNA (view.exe) (nécessaire)", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText31.Wrap( -1 )
		self.m_staticText31.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer8.Add( self.m_staticText31, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_dirPicker_ANNA = wx.DirPickerCtrl( self.ANNA_IN, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer8.Add( self.m_dirPicker_ANNA, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.ANNA_IN, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer8.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer8.AddSpacer( ( 0, 10), 1, wx.EXPAND, 5 )
		
		self.ANNA_IN.SetSizer( bSizer8 )
		self.ANNA_IN.Layout()
		bSizer8.Fit( self.ANNA_IN )
		self.m_notebook.AddPage( self.ANNA_IN, u"ANNA - process viewer.exe", False )
		self.MATERIAUX = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.MATERIAUX.SetBackgroundColour( wx.Colour( 255, 223, 223 ) )
		
		bSizer71 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText32 = wx.StaticText( self.MATERIAUX, wx.ID_ANY, u"Répertoire des Fichiers Matériaux", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText32.Wrap( -1 )
		self.m_staticText32.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer71.Add( self.m_staticText32, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_dirPicker_MATERIAU = wx.DirPickerCtrl( self.MATERIAUX, wx.ID_ANY, u".", u"Choisissez le directory de PLAST3D", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_USE_TEXTCTRL )
		bSizer71.Add( self.m_dirPicker_MATERIAU, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline21 = wx.StaticLine( self.MATERIAUX, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer71.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer71.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.MATERIAUX.SetSizer( bSizer71 )
		self.MATERIAUX.Layout()
		bSizer71.Fit( self.MATERIAUX )
		self.m_notebook.AddPage( self.MATERIAUX, u"Gestion de la base de données Matériaux/Films", False )
		
		bSizer10.Add( self.m_notebook, 5, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panel7.SetSizer( bSizer10 )
		self.m_panel7.Layout()
		bSizer10.Fit( self.m_panel7 )
		self.m_panel8 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel8.SetMinSize( wx.Size( 10,50 ) )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_textCtrl_console = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_NOHIDESEL|wx.TE_READONLY|wx.TE_RICH2 )
		self.m_textCtrl_console.SetFont( wx.Font( 14, 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer11.Add( self.m_textCtrl_console, 1, wx.ALL|wx.BOTTOM|wx.EXPAND, 5 )
		
		self.m_panel8.SetSizer( bSizer11 )
		self.m_panel8.Layout()
		bSizer11.Fit( self.m_panel8 )
		self.m_splitter1.SplitHorizontally( self.m_panel7, self.m_panel8, 800 )
		bSizerAllPanel.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizerAllPanel )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 2, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.m_menubar = wx.MenuBar( 0 )
		self.m_menubar.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		self.m_menu_projet = wx.Menu()
		self.m_menuItem_Projet_New = wx.MenuItem( self.m_menu_projet, wx.ID_ANY, u"Nouveau", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_projet.AppendItem( self.m_menuItem_Projet_New )
		
		self.m_menuItem_Projet_Open = wx.MenuItem( self.m_menu_projet, wx.ID_ANY, u"Ouvrir...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_projet.AppendItem( self.m_menuItem_Projet_Open )
		
		self.m_menuItem_Projet_Save = wx.MenuItem( self.m_menu_projet, wx.ID_ANY, u"Enregistrer", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_projet.AppendItem( self.m_menuItem_Projet_Save )
		
		self.m_menuItem_Projet_SaveAs = wx.MenuItem( self.m_menu_projet, wx.ID_ANY, u"Enregistrer sous...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_projet.AppendItem( self.m_menuItem_Projet_SaveAs )
		
		self.m_menubar.Append( self.m_menu_projet, u"Projets IMD" ) 
		
		self.m_menu_materiau = wx.Menu()
		self.m_menuItem_Materiau_New = wx.MenuItem( self.m_menu_materiau, wx.ID_ANY, u"Nouveau", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_materiau.AppendItem( self.m_menuItem_Materiau_New )
		
		self.m_menuItem_Materiau_Open = wx.MenuItem( self.m_menu_materiau, wx.ID_ANY, u"Ouvrir...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_materiau.AppendItem( self.m_menuItem_Materiau_Open )
		
		self.m_menuItem_Materiau_Save = wx.MenuItem( self.m_menu_materiau, wx.ID_ANY, u"Enregistrer", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_materiau.AppendItem( self.m_menuItem_Materiau_Save )
		
		self.m_menuItem_Materiau_SaveAs = wx.MenuItem( self.m_menu_materiau, wx.ID_ANY, u"Enregistrer sous...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu_materiau.AppendItem( self.m_menuItem_Materiau_SaveAs )
		
		self.m_menubar.Append( self.m_menu_materiau, u"Fichiers Matériaux" ) 
		
		self.m_menu3 = wx.Menu()
		self.m_menubar.Append( self.m_menu3, u"?" ) 
		
		self.SetMenuBar( self.m_menubar )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose_Frame )
		self.Bind( wx.EVT_MIDDLE_DOWN, self.OnMiddleDown_wxMainFrame )
		self.m_splitter1.Bind( wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSplitterChanging )
		self.m_notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged )
		self.m_dirPicker_PLAST3D.Bind( wx.EVT_DIRPICKER_CHANGED, self.OnDirChanged_PLAST3D )
		self.m_LaunchPlast.Bind( wx.EVT_BUTTON, self.OnButtonClick_LaunchPlast )
		self.m_checkBox_FichierDAT.Bind( wx.EVT_CHECKBOX, self.OnCheckBox_FichierDAT )
		self.m_filePicker_FichierDAT.Bind( wx.EVT_FILEPICKER_CHANGED, self.OnFileChanges_FichierDAT )
		self.m_splitter3.Bind( wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSplitterChanging )
		self.m_filePicker_Moule.Bind( wx.EVT_FILEPICKER_CHANGED, self.OnFileChanges_STLMoule )
		self.m_button_generer_film.Bind( wx.EVT_BUTTON, self.OnButtonClick_m_button_generer_film )
		self.m_filePicker_Film.Bind( wx.EVT_FILEPICKER_CHANGED, self.OnFileChanges_STLFilm )
		self.m_int_distance_moule_film.Bind( wx.EVT_KILL_FOCUS, self.OnKillFocus_m_int_distance_moule_film )
		self.m_filePicker_thermique_dat.Bind( wx.EVT_FILEPICKER_CHANGED, self.OnFileChanges_STLFilm )
		self.m_splitter2.Bind( wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSplitterChanging )
		self.m_listBox_vtk.Bind( wx.EVT_LISTBOX, self.OnListBox_vtk )
		self.m_checkBox_texture.Bind( wx.EVT_CHECKBOX, self.OnCheckBox_texture )
		self.m_checkBox_lines.Bind( wx.EVT_CHECKBOX, self.OnCheckBox_lines )
		self.m_choice_texture.Bind( wx.EVT_CHOICE, self.OnChoice_texture )
		self.m_slider_texture.Bind( wx.EVT_SCROLL, self.OnScroll_slider_texture )
		self.m_slider_vtk.Bind( wx.EVT_SCROLL, self.OnScroll_slider_vtk )
		self.m_slider_vtk_color.Bind( wx.EVT_SCROLL, self.OnScroll_slider_vtk_color )
		self.m_choice_vtk_color.Bind( wx.EVT_CHOICE, self.OnChoice_vtk_color )
		self.m_button_vtk.Bind( wx.EVT_BUTTON, self.OnButtonClick_vtk )
		self.m_dirPicker_MATERIAU.Bind( wx.EVT_DIRPICKER_CHANGED, self.OnDirChanged_PLAST3D )
		self.Bind( wx.EVT_MENU, self.OnMenuSelection_Projet_New, id = self.m_menuItem_Projet_New.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuSelection_Projet_Save, id = self.m_menuItem_Projet_Save.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuSelection_Projet_SaveAs, id = self.m_menuItem_Projet_SaveAs.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose_Frame( self, event ):
		event.Skip()
	
	def OnMiddleDown_wxMainFrame( self, event ):
		event.Skip()
	
	def OnSplitterChanging( self, event ):
		event.Skip()
	
	def OnNotebookPageChanged( self, event ):
		event.Skip()
	
	def OnDirChanged_PLAST3D( self, event ):
		event.Skip()
	
	def OnButtonClick_LaunchPlast( self, event ):
		event.Skip()
	
	def OnCheckBox_FichierDAT( self, event ):
		event.Skip()
	
	def OnFileChanges_FichierDAT( self, event ):
		event.Skip()
	
	
	def OnFileChanges_STLMoule( self, event ):
		event.Skip()
	
	def OnButtonClick_m_button_generer_film( self, event ):
		event.Skip()
	
	def OnFileChanges_STLFilm( self, event ):
		event.Skip()
	
	def OnKillFocus_m_int_distance_moule_film( self, event ):
		event.Skip()
	
	
	
	def OnListBox_vtk( self, event ):
		event.Skip()
	
	def OnCheckBox_texture( self, event ):
		event.Skip()
	
	def OnCheckBox_lines( self, event ):
		event.Skip()
	
	def OnChoice_texture( self, event ):
		event.Skip()
	
	def OnScroll_slider_texture( self, event ):
		event.Skip()
	
	def OnScroll_slider_vtk( self, event ):
		event.Skip()
	
	def OnScroll_slider_vtk_color( self, event ):
		event.Skip()
	
	def OnChoice_vtk_color( self, event ):
		event.Skip()
	
	def OnButtonClick_vtk( self, event ):
		event.Skip()
	
	
	def OnMenuSelection_Projet_New( self, event ):
		event.Skip()
	
	def OnMenuSelection_Projet_Save( self, event ):
		event.Skip()
	
	def OnMenuSelection_Projet_SaveAs( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 800 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	
	def m_splitter3OnIdle( self, event ):
		self.m_splitter3.SetSashPosition( 1000 )
		self.m_splitter3.Unbind( wx.EVT_IDLE )
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 100 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	

