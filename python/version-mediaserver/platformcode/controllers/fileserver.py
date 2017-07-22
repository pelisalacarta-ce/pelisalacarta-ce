# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Controlador para acceso a archivos locales
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from controller import Controller
from core import config
import os
import re
from core import logger
import time

class fileserver(Controller):
    pattern = re.compile("^/(?:media/.*?)?(?:local/.*?)?$")
    
    def run(self, path):
      if path=="/":
        f=open( os.path.join ( config.get_runtime_path() , "platformcode" , "template" , "page.html" ), "rb" )
        self.handler.send_response(200)
        self.handler.send_header('Content-type', 'text/html')
        self.handler.end_headers()
        respuesta = f.read()
        respuesta = respuesta.replace("{$WSPORT}", str(config.get_setting("websocket.port")))
        self.handler.wfile.write(respuesta)
        f.close()
        
      elif path.startswith("/local/"):
        import base64
        import urllib
        Path= path.replace("/local/","").split("/")[0]
        Path = base64.b64decode(urllib.unquote_plus(Path))
        Size = int(os.path.getsize(Path.decode("utf8") ))
        f=open(Path.decode("utf8") , "rb" )
        if not self.handler.headers.get("range") ==None:
          if "=" in str(self.handler.headers.get("range")) and "-" in str(self.handler.headers.get("range")):
            Inicio= int(self.handler.headers.get("range").split("=")[1].split("-")[0])
            if self.handler.headers.get("range").split("=")[1].split("-")[1]<>"": 
              Fin= int(self.handler.headers.get("range").split("=")[1].split("-")[1])
            else:
              Fin = Size-1
          
        else:
          Inicio=0
          Fin = Size-1
        
        if not Fin > Inicio: Fin = Size-1
          
        if self.handler.headers.get("range") ==None:
          logger.info("-------------------------------------------------------")
          logger.info("Solicitando archivo local: "+ Path)
          logger.info("-------------------------------------------------------")
          
          self.handler.send_response(200)
          self.handler.send_header("Content-Disposition", "attachment; filename=video.mp4")  
          self.handler.send_header('Accept-Ranges', 'bytes')   
          self.handler.send_header('Content-Length', str(Size))   
          self.handler.send_header("Connection", "close") 
          self.handler.end_headers()
          while True:
            time.sleep(0.2)
            buffer =f.read(1024*250)
            if not buffer:
              break
            self.handler.wfile.write(buffer)
          self.handler.wfile.close()
          f.close()
        else:
          logger.info("-------------------------------------------------------")
          logger.info("Solicitando archivo local: "+ Path)
          logger.info("Rango: "+ str(Inicio) + "-" + str(Fin) + "/" + str(Size))
          logger.info("-------------------------------------------------------")
          f.seek(Inicio)
          
          self.handler.send_response(206)
          self.handler.send_header("Content-Disposition", "attachment; filename=video.mp4")  
          self.handler.send_header('Accept-Ranges', 'bytes')   
          self.handler.send_header('Content-Length', str(Fin-Inicio))   
          self.handler.send_header('Content-Range', str(Inicio) + "-" + str(Fin) + "/" + str(Size))
          self.handler.send_header("Connection", "close") 
          
          self.handler.end_headers()
          while True:
            time.sleep(0.2)
            buffer =f.read(1024*250)
            if not buffer:
              break
            self.handler.wfile.write(buffer)
          self.handler.wfile.close()
          f.close()         
      elif path.startswith("/media/"):
        file = os.path.join ( config.get_runtime_path() , "platformcode" , "template" , path[7:] )
        from mimetypes import MimeTypes
        mime = MimeTypes()
        mime_type = mime.guess_type(file)
        try:
          mim = mime_type[0]
        except:
          mim = ""
        f=open(file, "rb")
        self.handler.send_response(200)
        self.handler.send_header('Content-type', mim)
        self.handler.end_headers()
        self.handler.wfile.write(f.read())
        f.close()
