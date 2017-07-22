# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta 4
# Copyright 2015 tvalacarta@gmail.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
# This file is part of pelisalacarta 4.
#
# pelisalacarta 4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelisalacarta 4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pelisalacarta 4.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------
# platformtools
# ------------------------------------------------------------
# Herramientas responsables de adaptar los diferentes 
# cuadros de dialogo a una plataforma en concreto,
# en este caso Mediserver.
# version 1.3
# ------------------------------------------------------------
import os
import sys
from core import config
from core import logger
import threading
controllers = {}


def dialog_ok(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].dialog_ok(*args, **kwargs)
    
def dialog_notification(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].dialog_notification(*args, **kwargs)

def dialog_yesno(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].dialog_yesno(*args, **kwargs)
    
def dialog_select(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].dialog_select(*args, **kwargs)

def dialog_progress(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].dialog_progress(*args, **kwargs)
 
def dialog_progress_bg(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].dialog_progress_bg(*args, **kwargs)

def dialog_input(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].dialog_input(*args, **kwargs)
    
def dialog_numeric(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].dialog_numeric(*args, **kwargs)

def itemlist_refresh(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].itemlist_refresh(*args, **kwargs)

def itemlist_update(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].itemlist_update(*args, **kwargs)

def render_items(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].render_items(*args,**kwargs)

def is_playing(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].is_playing(*args, **kwargs)

def play_video(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].play_video(*args, **kwargs)

def stop_video(*args, **kwargs):
    # id = threading.current_thread().name
    # return controllers[id].play_video(*args, **kwargs)
    return False

def open_settings(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].open_settings(*args, **kwargs)

def show_channel_settings(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].show_channel_settings(*args, **kwargs)

def show_video_info(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].show_video_info(*args, **kwargs)

def show_recaptcha(*args, **kwargs):
    id = threading.current_thread().name
    return controllers[id].show_recaptcha(*args, **kwargs)