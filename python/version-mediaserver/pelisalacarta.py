#! /usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import sys
import os
import time
import threading
from functools import wraps
sys.dont_write_bytecode = True
from core import config
sys.path.append(os.path.join(config.get_runtime_path(), 'lib'))
from core import logger
from platformcode import platformtools
import HTTPServer
import WebSocket

http_port = config.get_setting("server.port")
websocket_port = config.get_setting("websocket.port")
myip = config.get_local_ip()

def ThreadNameWrap(func):
    @wraps(func)
    def bar(*args, **kw):
        if not "name" in kw:
            kw['name'] = threading.current_thread().name
        return func(*args, **kw)

    return bar

threading.Thread.__init__ = ThreadNameWrap(threading.Thread.__init__)

if sys.version_info < (2,7,11):
  import ssl
  ssl._create_default_https_context = ssl._create_unverified_context

def MostrarInfo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print ("--------------------------------------------------------------------")
    print ("Pelisalacarta Iniciado")
    print ("La URL para acceder es http://%s:%s" % (myip, http_port))
    print ("WebSocket Server iniciado en ws://%s:%s" % (myip, websocket_port))
    print ("--------------------------------------------------------------------")
    print ("Runtime Path      : " + config.get_runtime_path())
    print ("Data Path         : " + config.get_data_path())
    print ("Download Path     : " + config.get_setting("downloadpath"))
    print ("DownloadList Path : " + config.get_setting("downloadlistpath"))
    print ("Bookmark Path     : " + config.get_setting("bookmarkpath"))
    print ("Library Path      : " + config.get_setting("librarypath"))
    print ("--------------------------------------------------------------------")
    conexiones = []
    controllers = platformtools.controllers
    for a in controllers:
        try:
          print platformtools.controllers[a].controller.client_ip + " - (" + platformtools.controllers[a].controller.name + ")"
        except:
          pass



def start():
    logger.info("pelisalacarta server init...")
    config.verify_directories_created()
    try:
        HTTPServer.start(MostrarInfo)
        WebSocket.start(MostrarInfo)

        # Da por levantado el servicio
        logger.info("--------------------------------------------------------------------")
        logger.info("Pelisalacarta Iniciado")
        logger.info("La URL para acceder es http://%s:%s" % (myip, http_port))
        logger.info("WebSocket Server iniciado en ws://%s:%s" % (myip, websocket_port))
        logger.info("--------------------------------------------------------------------")
        logger.info("Runtime Path      : " + config.get_runtime_path())
        logger.info("Data Path         : " + config.get_data_path())
        logger.info("Download Path     : " + config.get_setting("downloadpath"))
        logger.info("DownloadList Path : " + config.get_setting("downloadlistpath"))
        logger.info("Bookmark Path     : " + config.get_setting("bookmarkpath"))
        logger.info("Library Path      : " + config.get_setting("librarypath"))
        logger.info("--------------------------------------------------------------------")
        MostrarInfo()

        start = True
        while start:
            time.sleep(1)

    except KeyboardInterrupt:
        print 'Deteniendo el servidor HTTP...'
        HTTPServer.stop()
        print 'Deteniendo el servidor WebSocket...'
        WebSocket.stop()
        print 'Pelisalacarta Detenido'
        start = False


# Inicia pelisalacarta
start()
