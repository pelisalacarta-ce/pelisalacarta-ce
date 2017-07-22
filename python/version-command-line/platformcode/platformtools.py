# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# platformtools
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/

from core import config


def dialog_ok(heading, line1, line2="", line3=""):
    return True
    
def dialog_notification(heading, message, icon=0, time=5000, sound=True):
    pass

def dialog_yesno(heading, line1, line2="", line3="", nolabel="No", yeslabel="Si", autoclose=""):
    return True
  
def dialog_select(heading, list): 
    return -1
    
def dialog_progress(heading, line1, line2="", line3=""):
    return None

def dialog_progress_bg(heading, message=""):
    return None

def dialog_input(default="", heading="", hidden=False):
    return None

def dialog_numeric(type, heading, default=""):
    return None
        
def itemlist_refresh():
    pass

def itemlist_update(item):
    pass

def render_items(itemlist, parentitem):
    pass
    
def is_playing():
    return None

def play_video(item):
    pass

def stop_video():
    pass

def show_channel_settings(list_controls=None, dict_values=None, caption="", callback=None, item=None):
    return None

def show_recaptcha(key, referer):
    return None