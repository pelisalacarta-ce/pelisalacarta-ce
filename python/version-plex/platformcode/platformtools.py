# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# platformtools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Herramientas responsables de adaptar los diferentes 
# cuadros de dialogo a una plataforma en concreto,
# en este caso plex
# ------------------------------------------------------------

import os
from core import config

def dialog_ok(heading, line1, line2="", line3=""):
    return True
    
def dialog_notification(heading, message, icon=0, time=5000, sound=True):
    return True

def dialog_yesno(heading, line1, line2="", line3="", nolabel="No", yeslabel="Si", autoclose=""):
    return True
  
def dialog_select(heading, list): 
    return 1
    
def dialog_progress(heading, line1, line2="", line3=""):
  class Dialog(object):
    def __init__(self,heading, line1, line2="", line3=""):
      self.canceled = False
      pass
      
    def iscanceled(self):
      return self.canceled
      
    def update(self,percent, text):
      return True
      
    def close(self):
      self.canceled = True
      return True
  return Dialog(heading, line1, line2, line3)

def dialog_progress_bg(heading, message=""):
    pass

def dialog_input(default="", heading="", hidden=False):
    return default

def dialog_numeric(type, heading, default=""):
    pass
        
def itemlist_refresh():
    pass

def itemlist_update(item):
    pass

def render_items(itemlist, parentitem):
    pass
    
def is_playing():
    return False

def play_video(item):
    pass

def stop_video():
    pass

def show_channel_settings(list_controls=None, dict_values=None, caption="", channel="", callback=None, item=None, custom_button = None, channelpath=None):
    '''
    Muestra un cuadro de configuracion personalizado para cada canal y guarda los datos al cerrarlo.
    
    Parametros: ver descripcion en plex_config_menu.SettingsWindow
    '''
    from platformcode import plex_config_menu
    return plex_config_menu.show_channel_settings(list_controls=list_controls, dict_values=dict_values, caption=caption, callback=callback, item=item, custom_button=custom_button, channelpath=channelpath)
 
def show_recaptcha(key, referer):
    return None