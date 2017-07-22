# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Módulo para acciones en el cliente HTML
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os,importlib,re
from inspect import isclass
import sys
from controller import Controller
from core import logger

def load_controllers():
    controllers=[]
    path=os.path.split(__file__)[0]
    for fname in os.listdir(path):
        mod,ext=os.path.splitext(fname)
        fname=os.path.join(path,fname)
        if os.path.isfile(fname) and ext=='.py' and not mod.startswith('_'):
            try:
              exec "import "+ mod + " as controller"
            except:
              import traceback
              logger.error(traceback.format_exc())
              
            for c in dir(controller):
                cls=getattr(controller, c);

                if not c.startswith('_') and isclass(cls) and issubclass(cls, Controller) and Controller != cls:
                    controllers.append(cls)
    return controllers 

controllers= load_controllers() 

def find_controller(url):
  result = []
  for c in controllers:
    if c().match(url):
      return c