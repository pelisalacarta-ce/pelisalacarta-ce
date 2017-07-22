# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Controlador para acceso indirecto a ficheros remotos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from controller import Controller
from core import config
import os
import re
from core import logger
import time 
import urllib2, urllib
import base64

class proxy(Controller):
    pattern = re.compile("^/proxy/")
    
    def run(self, path):
        url= path.replace("/proxy/","").split("/")[0]
        url = base64.b64decode(urllib.unquote_plus(url))
        
        request_headers = self.handler.headers.dict
        
        if "host" in request_headers: request_headers.pop("host")
        if "referer" in request_headers: request_headers.pop("referer")
        if "cookie" in request_headers: request_headers.pop("cookie")
        
        if "|" in url:
          url_headers = dict([[header.split("=")[0].lower(),urllib.unquote_plus("=".join(header.split("=")[1:]))] for header in url.split("|")[1].split("&")])
          url = url.split("|")[0]
          request_headers.update(url_headers)

        req = urllib2.Request(url, headers=request_headers)
        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=0))
          
        try:
          h = opener.open(req)
        except urllib2.HTTPError, e:
          h = e
        except:
          self.handler.send_response("503")
          self.handler.wfile.close()
          h.close()
          
        self.handler.send_response(h.getcode())
        for header in h.info():
            self.handler.send_header(header, h.info()[header])

        self.handler.end_headers()
        
        blocksize = 1024
        bloqueleido = h.read(blocksize)
        while len(bloqueleido)>0:
          self.handler.wfile.write(bloqueleido)
          bloqueleido = h.read(blocksize)

        self.handler.wfile.close()
        h.close()