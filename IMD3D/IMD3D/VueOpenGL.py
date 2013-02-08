#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 3 Déc. 2012

@author: damien
'''

import numpy
import colorsys
from multiprocessing import Queue
from threading import Thread as Process
import Common
try:
    from OpenGL.platform import win32
except AttributeError:
    pass
import math
import logging
logging.basicConfig()
import wx.glcanvas
try:
    import OpenGL.GL as gl
    import OpenGL.GLU as glu
    import OpenGL.GLUT as glut
    import OpenGL.GLE as gle
except ImportError:
    raise ImportError, "Required dependency OpenGL not present"
    
    
class cMainVueOpenGL(wx.glcanvas.GLCanvas):
  def __init__(self, *args, **kwargs):
    wx.glcanvas.GLCanvas.__init__(self, *args, **kwargs)
    
    self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)#ne sert à rien uniquement pour éviter le flash sous MSW et uniquement en Python...
    self.Bind(wx.EVT_PAINT, self.mDessine)
    self.Bind(wx.EVT_SIZE, self.OnSize)
    self.Bind(wx.EVT_KEY_DOWN, self.mAppuiTouche)
    self.Bind(wx.EVT_MOUSE_EVENTS, self.mEvenementSouris)
    
    self.OpenGlVersion=gl.glGetString(gl.GL_VERSION)
    self._frame=self.TopLevelParent
    self.lbd,self.rbd,self.mbd,self.mbdc,self.rdc=(0,0,0,0,0)
    self.flag_reset_view=0
    self.flag_new_set_of_points=0
    self.x,self.y=0,0
    self.init = False
    # Créer une queue de donnée rempli par la fonction get_quad_from_vtk du module vtk2obj (utile si cette fonction est appelé dans un thread)
    # Vérifier qu'il n'y a rien dans la queue avant de dessiner
    self.q=Queue()
    self.points=[[(-1,1,0),(-1,2,0),(2,2,0),(2,1,0)],[(0,1,0),(1,1,0),(1,-1,0),(0,-1,0)],[(-1,-1,0),(-1,-2,0),(2,-2,0),(2,-1,0)]] #la lettre I
    self.mean,self.max,self.min=Common.MeanMaxMin(self.points)  
    # Défini N coleurs différentes matrice de transformation HSV vers RGB
    # La saturation et valeur réglable via le Slider (utilisation d'un flag=>cf NoteBBook module)
    self.flag_color_change=0
    self.N = 512
    HSV_tuples = [(x*0.5/self.N, 0.75, 0.75) for x in range(self.N)]
    self.RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    # Données des couleurs ou data de chaque cell (quads) - Gestion de IHM pour le choix des couleurs
    self.cell_data,self.cd_max,self.cd_min={},{},{}
    self.TableCouleur="Z-Hauteur"
    self.cache_color={}
    
    #flag concernant la texture:
    #  0 pas de changement
    # -1 texture devient inactif
    #  1 texture devient actif
    #  2 changement de texture
    #  3 changement de taille
    #cf Notebook
    self.flag_texture_change=0
    self.rz,self.ry,self.pz=(0.0,0.0,22.0)
    self.CoordTex=[0,0,0,0,0,0]
    self.only_lines=0
       
  def OnSize(self, event):
    size = self.size = self.GetClientSize()
    if self.GetContext() and self.GetParent().IsShown() and not size[0]==0 and not size[1]==0: 
    #vérifie que l'on est bien dans l'onglet visualisation 3D sinon on a un warning wx canvas
        self.SetCurrent()
        gl.glViewport(0, 0, size.width, size.height)
    event.Skip()
    
  def mInitOpenGL(self,ClearColor=[0.0,0.0,0.0,1.0]):

    #Active la gestion de la profondeur
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glShadeModel (gl.GL_FLAT)
    # Fixe la perspective
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(65.0, 4./3., 1.0, 10000.0)
    
    self.flag_opengl_light=True
    # Travail sur les lumières
    if self.flag_opengl_light:   
      gl.glEnable(gl.GL_COLOR_MATERIAL)   
       
      gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT, (0.8,1,1, 1))
      gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, (0,0,0, 1))
      gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE, (0.8,1,1, 1))
      gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, (0,0,0, 1))
      gl.glMaterialfv(gl.GL_FRONT, gl.GL_SHININESS, 128)
      gl.glLight(gl.GL_LIGHT0,gl.GL_AMBIENT,(0,0,0,1))
      gl.glLight(gl.GL_LIGHT0,gl.GL_DIFFUSE,(1,1,1,1))
      gl.glLight(gl.GL_LIGHT0,gl.GL_SPECULAR,(1,1,1,1))   
      gl.glLight(gl.GL_LIGHT0, gl.GL_POSITION, (100,100,10000,1))
      gl.glLight(gl.GL_LIGHT1,gl.GL_AMBIENT,(0,0,0,1))
      gl.glLight(gl.GL_LIGHT1,gl.GL_DIFFUSE,(1,1,1,1))
      gl.glLight(gl.GL_LIGHT1,gl.GL_SPECULAR,(1,1,1,1))    
      gl.glLight(gl.GL_LIGHT1, gl.GL_POSITION, (-100,-100,-10000,1))
      gl.glLight(gl.GL_LIGHT2,gl.GL_AMBIENT,(0,0,0,1))
      gl.glLight(gl.GL_LIGHT2,gl.GL_DIFFUSE,(1,1,1,1))
      gl.glLight(gl.GL_LIGHT2,gl.GL_SPECULAR,(1,1,1,1))    
      gl.glLight(gl.GL_LIGHT2, gl.GL_POSITION, (1000,1000,100,1))
      gl.glLight(gl.GL_LIGHT3,gl.GL_AMBIENT,(0,0,0,1))
      gl.glLight(gl.GL_LIGHT3,gl.GL_DIFFUSE,(1,1,1,1))
      gl.glLight(gl.GL_LIGHT3,gl.GL_SPECULAR,(1,1,1,1))    
      gl.glLight(gl.GL_LIGHT3, gl.GL_POSITION, (-1000,-1000,-100,1))      
      gl.glEnable(gl.GL_LIGHT3)      
      gl.glEnable(gl.GL_LIGHT2)
      gl.glEnable(gl.GL_LIGHT1)
      gl.glEnable(gl.GL_LIGHT0)
      gl.glEnable(gl.GL_LIGHTING)
        

    
    #Initialiser la Texture sans l'activer...
    self.TextureBitmap(image=r"./images/"+self._frame.m_choice_texture.LabelText,size=(10.0/float(self._frame.m_slider_texture.GetValue())))

    
    # fixe le fond d'écran à noir
    gl.glClearColor(*ClearColor)
    # prépare à travailler sur le modèle
    # (données de l'application)
    gl.glMatrixMode(gl.GL_MODELVIEW)



    
  def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.
   
  def mCacheColor(self):
    #Gestion de la couleur à l'avance,  appelé entre autre par NoteBook.OnChoice_vtk_color
    j=0
    self.cache_color[self.TableCouleur]=[]
    for i in self.points:
      if  not self.TableCouleur=="Z-Hauteur":
        self.cache_color[self.TableCouleur].append(self.RGB_tuples[int(self.N*abs((self.cell_data[self.TableCouleur][j]-self.cd_min[self.TableCouleur])/(self.cd_max[self.TableCouleur]-self.cd_min[self.TableCouleur]+1e-99)))-1])
      else:
        self.cache_color[self.TableCouleur].append(self.RGB_tuples[int(self.N*abs((i[0][2]-self.min[2])/(self.max[2]-self.min[2]+1e-99)))-1])  
      j+=1 
   
  def mDrawFloor(self):
    #dessine le plancher
    gl.glPushMatrix ()  
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA) 
    gl.glColor4f(0.5, 0.5, 0.5, 0.5)
    gl.glBegin(gl.GL_QUADS)
    _facteur=5
    gl.glVertex3f(self.min[0]-_facteur*(self.max[0]-self.min[0]), self.min[1]-_facteur*(self.max[1]-self.min[1]), -22.0 + self.min[2])
    gl.glVertex3f(self.max[0]+_facteur*(self.max[0]-self.min[0]), self.min[1]-_facteur*(self.max[1]-self.min[1]), -22.0 + self.min[2])
    gl.glVertex3f(self.max[0]+_facteur*(self.max[0]-self.min[0]), self.max[1]+_facteur*(self.max[1]-self.min[1]), -22.0 + self.min[2])
    gl.glVertex3f(self.min[0]-_facteur*(self.max[0]-self.min[0]), self.max[1]+_facteur*(self.max[1]-self.min[1]), -22.0 + self.min[2])
    gl.glEnd()
    gl.glPopMatrix()   
    
  def mDrawAxes(self):
    _anti_zoom=self.pz*0.1
    _flag_texture=gl.glIsEnabled(gl.GL_TEXTURE_2D)
    _flag_color_mat=gl.glIsEnabled(gl.GL_COLOR_MATERIAL)
    _flag_lighting=gl.glIsEnabled(gl.GL_LIGHTING)
    gl.glDisable(gl.GL_TEXTURE_2D)  
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_COLOR_MATERIAL)
    gl.glDisable(gl.GL_LIGHTING)
    
    gl.glPushMatrix ()    
    gl.glTranslate(0,0,0)
    gl.glScalef(_anti_zoom,_anti_zoom,_anti_zoom)

    gl.glLineWidth (2.0)

    gl.glBegin (gl.GL_LINES)
    gl.glColor3d(1,0,0) # X axis is red.
    gl.glVertex3d(0,0,0)
    gl.glVertex3d(1,0,0 )
    gl.glEnd()
    gl.glRasterPos3f(1.2, 0.0, 0.0)
    glut.glutBitmapCharacter(glut.GLUT_BITMAP_9_BY_15, ord('x'))
    gl.glBegin (gl.GL_LINES)
    gl.glColor3d(0,1,0) # Y axis is green.
    gl.glVertex3d(0,0,0)
    gl.glVertex3d(0,1,0)
    gl.glEnd()    
    gl.glRasterPos3f(0.0, 1.2, 0.0)
    glut.glutBitmapCharacter(glut.GLUT_BITMAP_9_BY_15, ord('y'))
    gl.glBegin (gl.GL_LINES)    
    gl.glColor3d(0,0,1); # z axis is blue.
    gl.glVertex3d(0,0,0)
    gl.glVertex3d(0,0,1)
    gl.glEnd()    
    gl.glRasterPos3f(0.0, 0.0, 1.2)
    glut.glutBitmapCharacter(glut.GLUT_BITMAP_9_BY_15, ord('z'))
    gl.glPopMatrix()   

    if _flag_texture==True: gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glEnable(gl.GL_DEPTH_TEST)
    if _flag_color_mat==True:gl.glEnable(gl.GL_COLOR_MATERIAL)
    if _flag_lighting==True:gl.glEnable(gl.GL_LIGHTING)
    
  def mCreerDisplayList(self):
    """
    Utilisation des DisplayList d'OpenGL pour mettre en cache une scéne statique ou un objet
    Cette Fonction est appelé à l'init OpenGL puis à chaque fois que les vertex (points) ou la couleur change
    cf http://www.siteduzero.com/tutoriel-3-3841-afficher-une-display-list.html
    """
    #TODO: utilisez des drawarray plutot que une boucle et créer les normals au face pour la couleur
    #TODO: cf http://www.blitzbasic.com/Community/posts.php?topic=66184 and http://www.songho.ca/opengl/gl_vertexarray.html
    #TODO: cf https://sites.google.com/site/dlampetest/python/calculating-normals-of-a-triangle-mesh-using-numpy
    self.mean,self.max,self.min=Common.MeanMaxMin(self.points) 
    self.mCacheColor()
    dl=gl.glGenLists(1)
    gl.glNewList(dl,gl.GL_COMPILE)

    if not self.only_lines==1:
      if len(self.points[0])==4:
        gl.glBegin(gl.GL_QUADS)
      else:
        gl.glBegin(gl.GL_TRIANGLES)  
    else:
        gl.glLineWidth (1.0)
    ################################ Création de l'objet
    j=0
    #_c1,_c2,_c3,_c4=Common.FindCorners(self.points)
    #flag1,flag2,flag3,flag4=0,0,0,0
    for i in self.points:
      gl.glColor3d(*self.cache_color[self.TableCouleur][j])
      # Boucle sur les différents sommet de l'élément (QUAD ou TRI à afficher)
      pair=0
      for k in i:
        if self.only_lines==1:      
          #gl.glColor3d(1,1,1)            
          if pair%(len(self.points[0]))==0: 
            gl.glBegin(gl.GL_LINE_LOOP)  
          gl.glVertex3d(k[0],k[1],k[2])
          if (pair+1)%(len(self.points[0]))==0:     
            gl.glEnd()
          pair+=1
        else:
          #gl.glNormal3d(0, 0, 1)    
          gl.glVertex3d(k[0],k[1],k[2])          
          
      j+=1
    ################################ Création de l'objet (fin)
    if not self.only_lines==1:
      gl.glEnd()
    gl.glEndList()
    return dl,self.mean,self.max,self.min
  
  def mSetVue(self):
    """
    Préparer la vue pour l'affichage des objets.
    @note: on n'utilise pas glu.gluLookAt mais directement des translations et rotations adéquates
    """
    #on s'éloigne de de l'axe des z (eyeview est à l'origine et dirigé vers -z)
    gl.glTranslate(0,0,-self.pz)
    #rotation autour de x (permet de basculer l'objet => cf événement souris sur l'axe Y)
    gl.glRotated(self.ry*180/math.pi, 1.0, 0.0,0.0)
    #rotation autour de z (permet de faire tourner l'objet => cf événement souris sur le plan XY)
    gl.glRotated(self.rz*180/math.pi, 0.0,0.0,1.0)

    #on se décale en fonction de la moyenne des coordonnées de l'objet (cette moyenne sera modifiée pour pouvoir bouger dans le plan XY)
    gl.glTranslate(-self.mean[0],-self.mean[1],-self.mean[2])
    
  def mDessine(self,event):
    """
    Fonction Principale pour dessiner la scéne "OpenGL"
    Cette fonction est la fonction callback de l'événement PAINT [self.Bind(wx.EVT_PAINT, self.mDessine)]
    Fortement utiliser dans toutes l'Application elle est appelé indirectement via la fonction Refresh(True) de l'objet oVisuOpenGL
    ATTENTION!! Chaque Ajout dans cette fonction peut ralentir l'animation OpenGL!!!
    """
    #Vérifie qu'il n'y a rien dans la queue
    if not self.q.empty()==True:
      [self.points,self.cell_data],_flag_cache,_filein=self.q.get() #on récupère les points, on récupère le flag pour savoir si les points viennent du cache ou pas
      if _flag_cache==0:# si les données ne viennent pas du cache il faut les mettre
        self._frame.cache_liste_points[_filein]=[self.points,self.cell_data]
      self.flag_new_set_of_points-=1
      self._frame.m_textCtrl_console.AppendText(".")
      #Récupération des Map de couleur dans les cell_data, mis à jour de la liste de choix couleur
      self._frame.m_choice_vtk_color.Clear()
      self._frame.m_choice_vtk_color.Append("Z-Hauteur")
      for _i in self.cell_data:
        self.cd_max[_i],self.cd_min[_i]=min(self.cell_data[_i]),max(self.cell_data[_i])
        self._frame.m_choice_vtk_color.Append(_i)
      self._frame.m_choice_vtk_color.SetSelection(0)
      self.TableCouleur="Z-Hauteur"
      self.dl_surf,_,_,_=self.mCreerDisplayList()
    #Création de tuple de couleur HSV
    if not self.flag_color_change==0:
      #cas de changement de saturation/couleur (cf NoteBook.OnScroll_slider_vtk) ou
      HSV_tuples = [(x*0.5/self.N, float(self._frame.m_slider_vtk.GetValue())/100.0, float(self._frame.m_slider_vtk.GetValue())/100.0) for x in range(self.N)]
      HSV_tuples = Common.RotateList(HSV_tuples, self._frame.m_slider_vtk_color.GetValue())
      self.RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
      self.flag_color_change=0
      self.dl_surf,_,_,_=self.mCreerDisplayList()
    if not self.flag_texture_change==0:
      #Cas d'un changement dans les paramêtres GUI de la texture
      #  0 pas de changement
      # -1 texture devient inactif
      #  1 texture devient actif
      #  2 changement de texture
      #  3 changement de taille
      #cf Notebook
      if self.flag_texture_change==1:
        gl.glEnable(gl.GL_TEXTURE_2D)
      if self.flag_texture_change==-1:
        gl.glDisable(gl.GL_TEXTURE_2D)   
      if self.flag_texture_change==2:    
        self.TextureBitmap(image=r"./images/"+self._frame.m_choice_texture.LabelText,size=(10.0/float(self._frame.m_slider_texture.GetValue())))
      if self.flag_texture_change==3:
        self.CoordTex[0]=self.CoordTex[0]/self.TexSize
        self.CoordTex[1]=self.CoordTex[1]/self.TexSize
        self.TexSize=10.0/float(self._frame.m_slider_texture.GetValue())
        gl.glTexGendv(gl.GL_S,gl.GL_OBJECT_PLANE,(self.TexSize,0,0,0))
        gl.glTexGendv(gl.GL_T,gl.GL_OBJECT_PLANE,(0,self.TexSize,0,0))
        self.CoordTex[0]=self.CoordTex[0]*self.TexSize
        self.CoordTex[1]=self.CoordTex[1]*self.TexSize        
      self.flag_texture_change=0
      
    #Indique que les instructions OpenGL s'adressent au contexte OpenGL courant
    self.SetCurrent()
    if not self.init:
      self.mInitOpenGL()
      #On crée les couleurs et la display list 
      self.dl_surf,_,_,_=self.mCreerDisplayList()
      self.init = True

    #initialise les données liées à la gestion de la profondeur
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    # initialise GL_MODELVIEW
    # place le repère en (0,0,0)
    gl.glLoadIdentity()

    #On positionne la caméra
    if self.flag_reset_view==1:
      #cas ou l'on remet la caméra en position "moyenne" lorsque l'on clique sur le bouton Reset View (cf NoteBook)
      self.rz,self.ry,self.pz=(0.0,0.0,22.0)    
      self.flag_reset_view=0
      self.CoordTex=[0,0,0,0,0,0]
      self.mean,self.max,self.min=Common.MeanMaxMin(self.points) 
      
    self.mSetVue()    
    

    gl.glMatrixMode(gl.GL_TEXTURE)
    gl.glLoadIdentity()
    gl.glRotate(self.CoordTex[3],0.0,0.0,1.0)
    gl.glRotate(self.CoordTex[4],1.0,0.0,0.0)
    gl.glTranslate(self.CoordTex[0],self.CoordTex[1],0)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    
    gl.glCallList(self.dl_surf)
    self.mDrawFloor()
    self.mDrawAxes()
    
    #Finalement, envoi du dessin à l écran
    gl.glFlush()
    self.SwapBuffers()
    event.Skip()
    
  def mAppuiTouche(self,event):
    """
    Récupération des événements claviers:
    - F1 => Affichage d'un splash windows 30 secondes sur les possibilités des actions de la souris
    """
    e=event.GetKeyCode()
    if e==wx.WXK_F1:
      wx.SplashScreen(wx.Bitmap("./images/AideSourisIMD3D.png"), wx.SPLASH_TIMEOUT | wx.SPLASH_CENTRE_ON_PARENT,30000, self, -1,(100,100),style=wx.BORDER_DEFAULT).Show()
      return(0)
    self.Refresh(True)
    event.Skip()
  
  def Screen2World(self,x=None,y=None):
    """
    @note:http://nehe.gamedev.net/article/using_gluunproject/16013/
    """
    if x==None or y==None:
      x=self.x
      y=self.y
    viewport=gl.glGetIntegerv(gl.GL_VIEWPORT)
    modelview=gl.glGetDoublev(gl.GL_MODELVIEW_MATRIX)
    projection=gl.glGetDoublev(gl.GL_PROJECTION_MATRIX) #matrice pour clip coordinates
    y = viewport[3] - y
    z=gl.glReadPixels(x,y, 1, 1,gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT)
    pos=glu.gluUnProject(x,y,z, modelview, projection, viewport)
    return pos
  
  def AffNoeudsfromPos(self,_pos):
    """
    @param pos: position (tuple) dans l'espace (issu par exemple de Screen2World)
    """
    
    self._frame.m_statusBar.SetStatusText("Recherche du NOEUD cliqué...",1)
    logging.warning("pos="+str(_pos))
    _dist=[]
    _noeuds=[]
    for face in self.points:
      for j in face:          
        _dist.append(numpy.linalg.norm(numpy.array(j)-numpy.array(_pos)))
        _noeuds.append(j)
    _dist_mini=min(_dist)
    self._frame.m_statusBar.SetStatusText("Position du noeud le plus proche:(x={1:.2f},y={2:.2f},z={3:.2f}) - Distance:{0:.2f} mm".format(_dist_mini,*_noeuds[_dist.index(_dist_mini)]),1)
    
  def mEvenementSouris(self,event):
    """
    Liste des évenements souris gérés:
    Bouton Droit Enfoncé= Faire bouger l'objet sur le Plan XY
    Double Click Droit Enfoncé = Translater l'objet sur l' axe Z en utilisant l'axe Y de la souris
    Bouton Gauche Enfoncé = Rotation Autour de l'objet
    Molette = Zoom
    Bouton Milieu Enfoncé = Déplacé de la texture (si activé) suivant l'axe XY
    Double Click Bouton Gauche ou Milieu = Rotation et Placage de la texture suivant la vue courante
    """
    
    amt = event.GetWheelRotation() 
    if abs(amt)>0:
      #Roulette de la molette =+/-ZOOM
      units = amt/(-(event.GetWheelDelta())) 
      self.pz+=units*(self.pz/22.0)
      if self.pz<2:self.pz=2
      self.Refresh(True)  
      
    if event.LeftDown():
      #rotation autour du plan XY
      self.lbd=1
      self.ry0=self.ry
      self.rz0=self.rz
      
    if event.RightDown():
      #Translation dans le plan XY
      self.rbd=1
      self.xx0=self.mean[0]*math.cos(self.rz)-self.mean[1]*math.sin(self.rz)
      self.yy0=self.mean[1]*math.cos(self.rz)+self.mean[0]*math.sin(self.rz)
    elif event.RightDClick():
      #Translation sur l'axe Z en utilisant l'axe Y de la souris
      self.rdc=1
      self.rbd=0
      self.z0=self.mean[2]
          
    if event.MiddleDown():
      #Translation Texture dans le plan XY et Affichage Status Barre du point le plus proche du click souris
      if self.mbd==0:
        Process(target= self.AffNoeudsfromPos, args=(self.Screen2World(),)).start()   
      
      self.mbd=1
      self.xx0=self.CoordTex[0]*math.cos(self.rz)-self.CoordTex[1]*math.sin(self.rz)
      self.yy0=self.CoordTex[1]*math.cos(self.rz)+self.CoordTex[0]*math.sin(self.rz)

         
      
    if event.MiddleDClick():
      #Placement de la texture sur le premier plan eyeview suivant le "rayon Z"
      pos=self.Screen2World()
      self.mbdc=1
      self.CoordTex[0]=-pos[0]*self.TexSize
      self.CoordTex[1]=-pos[1]*self.TexSize
      self.CoordTex[3]=(self.rz)*180.0/math.pi
      self.CoordTex[4]=(self.ry)*180.0/math.pi
      logging.warning("pos="+str(pos))
      logging.warning("cam(rx,ry,px)="+str((self.rz,self.ry,self.pz)))      
      logging.warning("CoordTex="+str(self.CoordTex))
      logging.warning("Mean="+str((-self.mean[0],-self.mean[1],-self.mean[2])))
      logging.warning("SizeTex="+str(self.TexSize))
      self.Refresh(True)
      
    if self.lbd>=1:
      (self.x0,self.y0)=event.GetPosition()
      self.rz=(self.rz0+(self.x0-self.x)/100.0)
      self.ry=(self.ry0+(self.y0-self.y)/100.0)   
      self.Refresh(True)          
         
    elif self.rbd>=1:
      (self.x0,self.y0)=event.GetPosition()
      _x=self.xx0-(self.x0-self.x)/10.0
      _y=self.yy0+(self.y0-self.y)/10.0
      self.mean[0]=_x*math.cos(self.rz)+_y*math.sin(self.rz)
      self.mean[1]=_y*math.cos(self.rz)-_x*math.sin(self.rz)    
      self.Refresh(True)         

    elif self.rdc>=1:
      (self.x0,self.y0)=event.GetPosition()
      _y=self.z0+(self.y0-self.y)/10.0
      self.mean[2]=_y
      self.Refresh(True)    
      
    elif self.mbd>=1:
      (self.x0,self.y0)=event.GetPosition()
      _x=self.xx0-(self.x0-self.x)/100.0
      _y=self.yy0+(self.y0-self.y)/100.0
      self.CoordTex[0]=_x*math.cos(self.rz)+_y*math.sin(self.rz)
      self.CoordTex[1]=_y*math.cos(self.rz)-_x*math.sin(self.rz)
      self.Refresh(True)        
    else:
      (self.x,self.y)=event.GetPosition() 
      
    if event.ButtonUp():
      self.lbd,self.rbd,self.mbd,self.mbdc,self.rdc=(0,0,0,0,0)
      (self.x,self.y)=event.GetPosition() 
    event.Skip()   

  def TextureBitmap(self,image=r".\images\Mire_R.bmp",size=0.1):
    #On charge l'image texture à plaquer
    #@note: http://www.fil.univ-lille1.fr/~aubert/p3d/Cours04.pdf
    self.TexSize=size
    image_bmp=wx.Image(image)
    #Remise des coordonnées y dans le sens OpenGL différent de l'écran
    image_bmp=image_bmp.Mirror(horizontally=False)
    image_bmp=image_bmp.ConvertToBitmap()
    ix=image_bmp.Width
    iy=image_bmp.Height
    import numpy
    image_buffer = numpy.ones((ix,iy,3), numpy.uint8)
    image_bmp.CopyToBuffer(image_buffer)
    image=image_buffer.data
    ID=gl.glGenTextures(1)#récupère un ID d'objet-texture unique et libre 
    gl.glBindTexture(gl.GL_TEXTURE_2D, ID)# annonce l'utilisation d'une texture 2D pour objet-texture ID 
                                          #(toutes les fonctions de texture s'applique désormais à cet onjet-texture ID)
    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT,1) #préviens que les données de la texture sont brut
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, ix, iy, 0,gl.GL_RGB, gl.GL_UNSIGNED_BYTE, image_buffer) #charge la texture 2D
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameterf(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_S,gl.GL_CLAMP_TO_BORDER_ARB )
    gl.glTexParameterf(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_T,gl.GL_CLAMP_TO_BORDER_ARB )
    gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
    gl.glTexGeni(gl.GL_S,gl.GL_TEXTURE_GEN_MODE,gl.GL_OBJECT_LINEAR)
    gl.glEnable(gl.GL_TEXTURE_GEN_S)
    gl.glTexGeni(gl.GL_T,gl.GL_TEXTURE_GEN_MODE,gl.GL_OBJECT_LINEAR)  
    gl.glEnable(gl.GL_TEXTURE_GEN_T)
    gl.glTexGendv(gl.GL_S,gl.GL_OBJECT_PLANE,(size,0,0,0))
    gl.glTexGendv(gl.GL_T,gl.GL_OBJECT_PLANE,(0,size,0,0))
  
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA) 
    gl.glTexParameterfv(gl.GL_TEXTURE_2D,gl. GL_TEXTURE_BORDER_COLOR,(1,1,1,1))
    

"""
Class dérivée pour Gestion des vue STL et DAT
"""
class cSimpleVueOpenGL(cMainVueOpenGL):
  def __init__(self, *args, **kwargs):
    cMainVueOpenGL.__init__(self, *args, **kwargs)
    self.flag_DAT=False
    self.flag_STL=False
    self.flag_new_STL=False
    self.flag_new_DAT=False
    self.RESET_VIEW=(0.0,0.0,50.0)
    self._VueSTL=self.RESET_VIEW
    self._VueDAT=self.RESET_VIEW

  def mEvenementSouris(self,event):

    super(cSimpleVueOpenGL,self).mEvenementSouris(event)  
    if event.LeftDClick():
      if self.only_lines==1:  
        self.only_lines=0
      else: 
        self.only_lines=1
      if self._frame.m_checkBox_FichierDAT.GetValue()==False:
        self.meanSTL=self.mean 
        self.dl,_,_,_=self.mCreerDisplayList()
        self.mean=self.meanSTL    
      else:
        self.meanDAT=self.mean 
        self.dl,_,_,_=self.mCreerDisplayList()
        self.mean=self.meanDAT   
      self.Refresh(True)
      
    

  def mDessine(self,event):
    """
    Fonction Principale pour dessiner la scéne simple "OpenGL" (redéfinition de la fonction mDessine de la class parente)
    Cette fonction est la fonction callback de l'événement PAINT [self.Bind(wx.EVT_PAINT, self.mDessine)]
    Fortement utiliser dans toutes l'Application elle est appelé indirectement via la fonction Refresh(True) de l'objet oVisuOpenGL
    ATTENTION!! Chaque Ajout dans cette fonction peut ralentir l'animation OpenGL!!!
    """    


    #Indique que les instructions OpenGL s'adressent au contexte OpenGL courant
    self.SetCurrent()
    if not self.init:
      self._mInitOpenGL()
      #On crée les couleurs et la display list 
      self.dl,self.mean,_,_=self.mCreerDisplayList()
      self.pointsSTL=self.points
      self.meanSTL=self.mean
      self.init = True
    
    #initialise les données liées à la gestion de la profondeur
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    # initialise GL_MODELVIEW
    # place le repère en (0,0,0)
    gl.glLoadIdentity()

  
    if self.flag_STL and not self.flag_new_STL: #on bascule en mode STL sans changer de données
      self.flag_STL=False
      self.points=self.pointsSTL    
      self._VueDAT= (self.rz,self.ry,self.pz)      
      self.meanDAT=self.mean
      self.dl,_,_,_=self.mCreerDisplayList() 
      self.mean=self.meanSTL
      self.rz,self.ry,self.pz=self._VueSTL    
        
    if self.flag_new_STL : #on change de données
      self.flag_new_STL=False
      self.points=self.pointsSTL         
      self.dl,self.mean,self.max,self.min=self.mCreerDisplayList()   #on écrase mean
      self.rz,self.ry,self.pz=self.RESET_VIEW   
      self.pz=self.max[1]-self.min[1] if self.max[1]-self.min[1]>self.max[2]-self.min[2] else self.max[2]-self.min[2]

      
    if self.flag_DAT and not self.flag_new_DAT: #on bascule en mode DAT sans changer de données
      self.flag_DAT=False
      self.points=self.pointsDAT    
      self._VueSTL= (self.rz,self.ry,self.pz)
      self.meanSTL=self.mean
      self.dl,_,_,_=self.mCreerDisplayList() 
      self.mean= self.meanDAT
      self.rz,self.ry,self.pz=self._VueDAT           
      
    if self.flag_new_DAT: #on change de données
      self.flag_new_DAT=False
      self.points=self.pointsDAT
      if self.flag_DAT : #on a aussi basculer de STL=>DAT
        self.flag_DAT=False
        self._VueSTL= (self.rz,self.ry,self.pz)
        self.meanSTL=self.mean
      self.dl,self.mean,self.max,self.min=self.mCreerDisplayList()   #on écrase mean
      self.rz,self.ry,self.pz=self.RESET_VIEW
      self.pz=self.max[1]-self.min[1] if self.max[1]-self.min[1]>self.max[2]-self.min[2] else self.max[2]-self.min[2]        
      
   
    self.mSetVue()      
    
    gl.glLight(gl.GL_LIGHT0, gl.GL_POSITION, (0,0,10000,1))
    gl.glDisable(gl.GL_LINE_SMOOTH)    
    
    gl.glCallList(self.dl)

    self.mDrawAxes()
    #Finalement, envoi du dessin à l écran
    gl.glFlush()
    self.SwapBuffers()
    
    #test de création de bitmap à partir de la vue OpenGL
    #pixels = gl.glReadPixels( 0,0, self.size[0],self.size[1], gl.GL_RGB, gl.GL_UNSIGNED_BYTE )
    #image_bmp = Common.scale_bitmap(wx.BitmapFromBuffer(self.size[0],self.size[1],pixels),50,50)
    #self.TopLevelParent.m_bitmap_test.SetBitmap(image_bmp)
    #fin du test
    
    event.Skip()
    
  def _mInitOpenGL(self):
    self.mInitOpenGL([215.0/255.0,1.0,215.0/255.0,1.0])
          