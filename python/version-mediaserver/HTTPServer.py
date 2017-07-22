# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# HTTPServer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from core import logger
from core import config
import threading
import random
import re
import time
import traceback

class MyHTTPServer(HTTPServer):
    daemon_threads = True
    def process_request_thread(self, request, client_address):
        try:
          
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        ID = "%032x" %(random.getrandbits(128))
        t = threading.Thread(target = self.process_request_thread,
                             args = (request, client_address), name=ID)
        t.daemon = self.daemon_threads
        t.start()

    def handle_error(self, request, client_address):
      import traceback
      if not "socket.py" in traceback.format_exc():
        logger.error(traceback.format_exc())


class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args): 
      #sys.stderr.write("%s - - [%s] %s\n" %(self.client_address[0], self.log_date_time_string(), format%args))
      pass

    def do_GET(self):     
        from platformcode import platformtools
        from platformcode import controllers
        #Control de accesos
        Usuario = "user"
        Password = "password"
        ControlAcceso = False
        import base64
        #Comprueba la clave
        if ControlAcceso and self.headers.getheader('Authorization') <> "Basic " + base64.b64encode(Usuario + ":"+ Password):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"Introduce el nombre de usuario y clave para acceder a pelisalacarta\"')
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('¡Los datos introducidos no son correctos!')
            return
        

        data = re.compile('/data/([^/]+)/([^/]+)/([^/]+)', re.DOTALL).findall(self.path)
        if data:
          data = data[0]
          if data[0] in platformtools.requests:
            c = platformtools.requests[data[0]]
            response = {"id":data[1],"result": data[2]}
            print response
            c.handler = self
            c.set_data(response)
            while data[0] in platformtools.requests and not self.wfile.closed:
              time.sleep(1)
        else:         
          if self.path =="": self.path="/"

          #Busca el controller para la url
          controller = controllers.find_controller(self.path)
          if controller:
            try:
                c =  controller(self)
                c.run(self.path)
            except:
              if not "socket.py" in traceback.format_exc():
                  logger.error(traceback.format_exc())
            finally:
              c.__del__()
              del c
        return
    
    def address_string(self):
        # Disable reverse name lookups
        return self.client_address[:2][0] 
        
PORT=config.get_setting("server.port")
server = MyHTTPServer(('', int(PORT)), Handler)  

def start(fnc_info):
    server.fnc_info = fnc_info
    threading.Thread(target=server.serve_forever).start()
 
def stop():
    server.socket.close()
    server.shutdown()
    