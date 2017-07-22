# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Controlador para RSS
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import sys, os
from core import config
from core import logger
from controller import Controller
from controller import Platformtools
import random
import re
from core.item import Item
import threading
import json
import time

class jsonserver(Controller):
  pattern = re.compile("^/json")
  data = {}
  def __init__(self, handler=None):
    super(jsonserver,self).__init__(handler)
    self.platformtools = platformtools(self)

    
  def extract_item(self,path):
    if path=="/json" or path =="/json/":
      item = Item(channel="channelselector", action="mainlist")
    else:
      item=Item().fromurl(path.replace("/json/",""))
    return item
    
  def run(self, path):    
      item = self.extract_item(path)
      from platformcode import launcher
      launcher.run(item)
      
  def set_data(self, data):
    self.data = data
    
  def get_data(self, id):
    if "id" in self.data and self.data["id"] == id:
      data = self.data["result"]
    else:
      data = None
    return data
  def send_data(self, data, headers = {}, response = 200):
      headers.setdefault("content-type","application/json")
      headers.setdefault("connection","close")
      self.handler.send_response(response)
      for header in headers:
        self.handler.send_header(header, headers[header])
      self.handler.end_headers()
      self.handler.wfile.write(data)
 
 
class platformtools(Platformtools):
  def __init__(self, controller):
    self.controller = controller
    self.handler = controller.handler

      
  def render_items(self, itemlist, parentitem):      
      JSONResponse = {}
      JSONResponse["title"] = parentitem.title
      JSONResponse["date"] =  time.strftime("%x")
      JSONResponse["time"] = time.strftime("%X")
      JSONResponse["count"]=len(itemlist)
      JSONResponse["list"]= []
      for item in itemlist:
        JSONItem = {}
        JSONItem["title"] = item.title
        JSONItem["url"] = "http://" + self.controller.host+"/json/" + item.tourl()
        if item.thumbnail: JSONItem["thumbnail"] = item.thumbnail
        if item.plot: JSONItem["plot"] = item.plot
        JSONResponse["list"].append(JSONItem)
        
      
      self.controller.send_data(json.dumps(JSONResponse, indent=4, sort_keys=True))
      
  def dialog_select(self, heading, list): 
      ID = "%032x" %(random.getrandbits(128))
      response = '<?xml version="1.0" encoding="UTF-8" ?>\n'
      response +='<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
      response +='<channel>\n'
      response +='<link>/rss</link>\n'
      response +='<title>'+heading+'</title>\n'
      for option in list:
        response += '<item>\n'
        response += '<title>'+option +'</title>\n'
        response += '<image>%s</image>\n'
        response += '<link>http://'+self.controller.host+'/data/'+threading.current_thread().name +'/'+ID+'/'+str(list.index(option))+'</link>\n'
        response += '</item>\n\n'

      response += '</channel>\n'
      response += '</rss>\n'
      self.controller.send_data(response)

      self.handler.server.shutdown_request(self.handler.request)
      while not self.controller.get_data(ID):
        continue
      
      return  int(self.controller.get_data(ID))
      
  def dialog_ok(self, heading, line1, line2="", line3=""):
      text = line1
      if line2: text += "\n" + line2
      if line3: text += "\n" + line3
      ID = "%032x" %(random.getrandbits(128))
      response = '<?xml version="1.0" encoding="UTF-8" ?>\n'
      response +='<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
      response +='<channel>\n'
      response +='<link>/rss</link>\n'
      response +='<title>'+heading+'</title>\n'
      response += '<item>\n'
      response += '<title>'+text +'</title>\n'
      response += '<image>%s</image>\n'
      response += '<link></link>\n'
      response += '</item>\n\n'
      response += '<item>\n'
      response += '<title>Si</title>\n'
      response += '<image>%s</image>\n'
      response += '<link>http://'+self.controller.host+'/data/'+threading.current_thread().name +'/'+ID+'/1</link>\n'
      response += '</item>\n\n'
      response += '<item>\n'

      response += '</channel>\n'
      response += '</rss>\n'
      self.controller.send_data(response)

      self.handler.server.shutdown_request(self.handler.request)
      while not self.controller.get_data(ID):
        continue
          
  def dialog_yesno(self, heading, line1, line2="", line3=""):
      text = line1
      if line2: text += "\n" + line2
      if line3: text += "\n" + line3
      ID = "%032x" %(random.getrandbits(128))
      response = '<?xml version="1.0" encoding="UTF-8" ?>\n'
      response +='<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
      response +='<channel>\n'
      response +='<link>/rss</link>\n'
      response +='<title>'+heading+'</title>\n'
      response += '<item>\n'
      response += '<title>'+text +'</title>\n'
      response += '<image>%s</image>\n'
      response += '<link></link>\n'
      response += '</item>\n\n'
      response += '<item>\n'
      response += '<title>Si</title>\n'
      response += '<image>%s</image>\n'
      response += '<link>http://'+self.controller.host+'/data/'+threading.current_thread().name +'/'+ID+'/1</link>\n'
      response += '</item>\n\n'
      response += '<item>\n'
      response += '<title>No</title>\n'
      response += '<image>%s</image>\n'
      response += '<link>http://'+self.controller.host+'/data/'+threading.current_thread().name +'/'+ID+'/0</link>\n'
      response += '</item>\n\n'

      response += '</channel>\n'
      response += '</rss>\n'
      self.controller.send_data(response)

      self.handler.server.shutdown_request(self.handler.request)
      while not self.controller.get_data(ID):
        continue
      
      return  bool(int(self.controller.get_data(ID)))
      
  def dialog_notification(self, heading, message, icon=0, time=5000, sound=True):
      #No disponible por ahora, muestra un dialog_ok
      self.dialog_ok(heading,message)

        
  def play_video(self, item):
      response = '<?xml version="1.0" encoding="UTF-8" ?>\n'
      response +='<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
      response +='<channel>\n'
      response +='<link>/rss</link>\n'
      response +='<title>'+item.title+'</title>\n'
      response += '<item>\n'
      response += '<title>'+item.title +'</title>\n'
      response += '<image>%s</image>\n'
      response += '<link>'+item.video_url+'</link>\n'
      response += '</item>\n\n'

      response += '</channel>\n'
      response += '</rss>\n'

      self.controller.send_data(response)
