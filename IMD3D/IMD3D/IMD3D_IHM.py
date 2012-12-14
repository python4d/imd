# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import VueOpenGL as ogl

###########################################################################
## Class wxMainFrame
###########################################################################

class wxMainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Interface IMD3D", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.CAPTION|wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( 400,300 ), wx.DefaultSize )
		
		bSizerAllPanel = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.SP_3D )
		self.m_splitter1.SetSashGravity( 0.9 )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		self.m_splitter1.SetMinimumPaneSize( 100 )
		
		self.m_panel7 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel7.SetMinSize( wx.Size( 500,100 ) )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook = wx.Notebook( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, u"m_notebook" )
		self.m_notebook.SetBackgroundColour( wx.Colour( 179, 255, 179 ) )
		
		self.Plast3D_IN = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, u"m_panel_Plast3D_IN" )
		self.Plast3D_IN.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		self.Plast3D_IN.SetMinSize( wx.Size( -1,5000 ) )
		self.Plast3D_IN.SetMaxSize( wx.Size( -1,5000 ) )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook_Projet = wx.Notebook( self.Plast3D_IN, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_BOTTOM )
		self.m_notebook_Projet.SetBackgroundColour( wx.Colour( 215, 255, 215 ) )
		
		self.m_panel4 = wx.Panel( self.m_notebook_Projet, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.SetBackgroundColour( wx.Colour( 210, 255, 210 ) )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Répertoire de l'exécutable PLAST3D (plast3d.exe) et sorties fichiers VTK", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText3.Wrap( -1 )
		self.m_staticText3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_staticText3, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_dirPicker_PLAST3D = wx.DirPickerCtrl( self.m_panel4, wx.ID_ANY, u".", u"Choisissez le directory de PLAST3D", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_USE_TEXTCTRL )
		bSizer7.Add( self.m_dirPicker_PLAST3D, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline2 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer7.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer7.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_panel4.SetSizer( bSizer7 )
		self.m_panel4.Layout()
		bSizer7.Fit( self.m_panel4 )
		self.m_notebook_Projet.AddPage( self.m_panel4, u"PLAST3D Launcher", True )
		self.m_panel5 = wx.Panel( self.m_notebook_Projet, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook_Projet.AddPage( self.m_panel5, u"Paramêtres Procédés", False )
		
		bSizer4.Add( self.m_notebook_Projet, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.Plast3D_IN.SetSizer( bSizer4 )
		self.Plast3D_IN.Layout()
		bSizer4.Fit( self.Plast3D_IN )
		self.m_notebook.AddPage( self.Plast3D_IN, u"PLAST3D - Données Projet (entrées)", True )
		self.VISUALISATION_VTK = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"plast3d_visualisation" )
		self.VISUALISATION_VTK.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.VISUALISATION_VTK.SetBackgroundColour( wx.Colour( 187, 255, 187 ) )
		
		bSizerContentPLAST3D_visu = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_splitter2 = wx.SplitterWindow( self.VISUALISATION_VTK, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter2.SetSashGravity( 0.1 )
		self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
		self.m_splitter2.SetMinimumPaneSize( 100 )
		
		self.m_panel10 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self.m_panel10, wx.ID_ANY, u"Fichiers VTK", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.m_staticText2.Wrap( -1 )
		bSizer3.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		m_listBox_vtkChoices = [ u"test", u"de", u"la liste" ]
		self.m_listBox_vtk = wx.ListBox( self.m_panel10, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), m_listBox_vtkChoices, wx.LB_HSCROLL|wx.VSCROLL )
		self.m_listBox_vtk.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		bSizer3.Add( self.m_listBox_vtk, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		self.m_gauge_vtk = wx.Gauge( self.m_panel10, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,-1 ), wx.GA_HORIZONTAL )
		bSizer3.Add( self.m_gauge_vtk, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
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
		
		self.m_slider_vtk_color = wx.Slider( self.m_panel_OpenGL, wx.ID_ANY, 512, 0, 512, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
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
		self.m_notebook.AddPage( self.VISUALISATION_VTK, u"PLAST3D - *.vtk (sorties)", False )
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
		self.m_notebook.AddPage( self.ANNA_IN, u"ANNA - Viewer", False )
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
		
		self.m_textCtrl_console = wx.TextCtrl( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH )
		bSizer11.Add( self.m_textCtrl_console, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_panel8.SetSizer( bSizer11 )
		self.m_panel8.Layout()
		bSizer11.Fit( self.m_panel8 )
		self.m_splitter1.SplitHorizontally( self.m_panel7, self.m_panel8, 600 )
		bSizerAllPanel.Add( self.m_splitter1, 1, wx.EXPAND|wx.ALL, 5 )
		
		self.SetSizer( bSizerAllPanel )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
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
		
		self.SetMenuBar( self.m_menubar )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose_Frame )
		self.m_notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged )
		self.m_dirPicker_PLAST3D.Bind( wx.EVT_DIRPICKER_CHANGED, self.OnDirChanged_PLAST3D )
		self.m_listBox_vtk.Bind( wx.EVT_LISTBOX, self.OnListBox_vtk )
		self.m_slider_vtk.Bind( wx.EVT_SCROLL, self.OnScroll_slider_vtk )
		self.m_slider_vtk_color.Bind( wx.EVT_SCROLL, self.OnScroll_slider_vtk_color )
		self.m_choice_vtk_color.Bind( wx.EVT_CHOICE, self.OnChoice_vtk_color )
		self.m_button_vtk.Bind( wx.EVT_BUTTON, self.OnButtonClick_vtk )
		self.m_dirPicker_MATERIAU.Bind( wx.EVT_DIRPICKER_CHANGED, self.OnDirChanged_PLAST3D )
		self.Bind( wx.EVT_MENU, self.OnMenuSelection_Projet_New, id = self.m_menuItem_Projet_New.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose_Frame( self, event ):
		event.Skip()
	
	def OnNotebookPageChanged( self, event ):
		event.Skip()
	
	def OnDirChanged_PLAST3D( self, event ):
		event.Skip()
	
	def OnListBox_vtk( self, event ):
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
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 600 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	
	def m_splitter2OnIdle( self, event ):
		self.m_splitter2.SetSashPosition( 100 )
		self.m_splitter2.Unbind( wx.EVT_IDLE )
	

