# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Controlador para HTML
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import sys, os
from core import config
from core import logger
from core import versiontools
from controller import Controller
from controller import Platformtools
from platformcode import platformtools
import json
import re
from core.item import Item
import threading
import random
from platformcode import launcher
from core.tmdb import Tmdb
import time
import channelselector

class html(Controller):
    pattern = re.compile("##")
    name = "HTML"
  
    def __init__(self, handler=None, ID = None):
        super(html, self).__init__(handler, ID)
        self.platformtools = platform(self)
        self.data = {}
        if self.handler:
            self.client_ip = handler.client.getpeername()[0]
            self.send_message({"action": "connect", "data":{"version": "pelisalacarta %s" % versiontools.get_current_plugin_version_tag(), "date":versiontools.get_current_plugin_date()}})
            t = threading.Thread(target=launcher.start, name=ID)
            t.setDaemon(True)
            t.start()


    def run(self, path):
        if path:
          item = Item().fromurl(path)
        else:
          item = Item(channel="channelselector", action="mainlist", viewmode="banner")

        launcher.run(item)


    def get_data(self, id):
        while not "id" in self.data or not self.data["id"] == id:
          time.sleep(0.1)
        data = self.data["result"]
        self.data = {}
        return data


    def send_message(self, data):
        import random
        
        ID = "%032x" %(random.getrandbits(128))
        data["id"] = ID
        
        self.handler.sendMessage(json.dumps(data))
        return ID
   
 
 
class platform(Platformtools):
    def __init__(self, controller):
        self.controller = controller
        self.handler = controller.handler
        self.get_data = controller.get_data
        self.send_message = controller.send_message


    def render_items(self, itemlist, parent_item):
        """
        Función encargada de mostrar el itemlist, se pasa como parametros el itemlist y el item del que procede
        @type itemlist: list
        @param itemlist: lista de elementos a mostrar

        @type parent_item: item
        @param parent_item: elemento padre
        """

        # Si el itemlist no es un list salimos
        if not type(itemlist) == list:
            JsonData = {}
            JsonData["action"]="HideLoading"
            JsonData["data"] = {}
            self.send_message(JsonData)
            return

        # Si no hay ningun item, mostramos un aviso
        if not len(itemlist):
            itemlist.append(Item(title="No hay elementos que mostrar"))
        
        if parent_item.channel == "channelselector" and not parent_item.action == "filterchannels":
          parent_item.viewmode = "banner"
        elif parent_item.channel == "channelselector" and  parent_item.action == "filterchannels":
          parent_item.viewmode = "channel"
        if not parent_item.viewmode:
          parent_item.viewmode = "list"
        
        #Item Atrás
        if not (parent_item.channel=="channelselector" and parent_item.action=="mainlist") and not itemlist[0].action=="go_back":
          if parent_item.viewmode in ["banner", "channel"]:
            itemlist.insert(0,Item(title="Atrás", action="go_back",thumbnail=os.path.join(config.get_runtime_path(),"resources","images","bannermenu","thumb_atras.png")))
          else:
            itemlist.insert(0,Item(title="Atrás", action="go_back",thumbnail=os.path.join(config.get_runtime_path(),"resources","images","squares","thumb_atras.png")))
               
        JsonData = {}
        JsonData["action"] = "EndItems"
        JsonData["data"] = {}
        JsonData["data"]["itemlist"] = []
        JsonData["data"]["viewmode"] = parent_item.viewmode   
        JsonData["data"]["category"] = parent_item.category.capitalize()
        JsonData["data"]["host"] = self.controller.host
        
        # Recorremos el itemlist
        for item in itemlist:
                
            if not item.thumbnail and item.action == "search": item.thumbnail = channelselector.get_thumbnail_path() + "thumb_buscar.png"
            if not item.thumbnail and item.folder == True: item.thumbnail = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/thumb_folder.png"
            if not item.thumbnail and item.folder == False: item.thumbnail = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/thumb_nofolder.png"
            if "https://raw.githubusercontent.com/pelisalacarta-ce/media/master" in item.thumbnail and not item.thumbnail.startswith("https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/thumb_"):
            
              if parent_item.viewmode in ["banner", "channel"]: 
                item.thumbnail = channelselector.get_thumbnail_path("bannermenu") + os.path.basename(item.thumbnail)
              else:
                item.thumbnail = channelselector.get_thumbnail_path() + os.path.basename(item.thumbnail)
            
            #Estas imagenes no estan en bannermenu, asi que si queremos bannermenu, para que no se vean mal las quitamos    
            elif parent_item.viewmode in ["banner", "channel"] and item.thumbnail.startswith("https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/thumb_"):
              item.thumbnail = ""
              

            # Si el item no contiene categoria,le ponemos la del item padre
            if item.category == "":
                item.category = parent_item.category

            # Si el item no contiene fanart,le ponemos la del item padre
            if item.fanart == "":
                item.fanart = parent_item.fanart
            
            title = item.title.replace(item.title.lstrip(), ""). replace(" ", "&nbsp;") + item.title.lstrip()
            
            # Formatear titulo
            if item.text_color:
                title = '[COLOR %s]%s[/COLOR]' % (item.text_color, title)
            if item.text_blod:
                title = '[B]%s[/B]' % title
            if item.text_italic:
                title = '[I]%s[/I]' % title
            
            title = self.kodi_labels_to_html(title)
            
            #Añade headers a las imagenes si estan en un servidor con cloudflare    
            from core import httptools
            item.thumbnail = httptools.get_url_headers(item.thumbnail)
            item.fanart = httptools.get_url_headers(item.fanart)
          
            JsonItem = {}
            JsonItem["title"]=title
            JsonItem["thumbnail"]= item.thumbnail
            JsonItem["fanart"]=item.fanart
            JsonItem["plot"]=item.plot
            JsonItem["action"]=item.action
            JsonItem["url"]=item.tourl()
            JsonItem["context"]=[]
            if not item.action == "go_back":
              for Comando in self.set_context_commands(item, parent_item):
                JsonItem["context"].append({"title":Comando[0],"url": Comando[1]})
              
            JsonData["data"]["itemlist"].append(JsonItem)


        ID = self.send_message(JsonData)
        self.get_data(ID)


      
    def set_context_commands(self, item, parent_item):
        """
        Función para generar los menus contextuales.
            1. Partiendo de los datos de item.context
                 a. Metodo antiguo item.context tipo str separando las opciones por "|" (ejemplo: item.context = "1|2|3")
                    (solo predefinidos)
                b. Metodo list: item.context es un list con las diferentes opciones del menu:
                    - Predefinidos: Se cargara una opcion predefinida con un nombre.
                        item.context = ["1","2","3"]

                    - dict(): Se cargara el item actual modificando los campos que se incluyan en el dict() en caso de
                        modificar los campos channel y action estos serán guardados en from_channel y from_action.
                        item.context = [{"title":"Nombre del menu", "action": "action del menu", "channel",
                                        "channel del menu"}, {...}]

            2. Añadiendo opciones segun criterios
                Se pueden añadir opciones al menu contextual a items que cumplan ciertas condiciones

            3. Añadiendo opciones a todos los items
                Se pueden añadir opciones al menu contextual para todos los items

        @param item: elemento que contiene los menu contextuales
        @type item: item
        @param parent_item:
        @type parent_item: item
        """
        context_commands = []


        # Creamos un list con las diferentes opciones incluidas en item.context
        if type(item.context) == str:
            context = item.context.split("|")
        elif type(item.context) == list:
            context = item.context
        else:
            context = []

        # Opciones segun item.context
        for command in context:
            # Predefinidos
            if type(command) == str:
                if command == "buscar_trailer":
                    context_commands.append(("Buscar Trailer", item.clone(channel="trailertools", action="buscartrailer", contextual=True).tourl()))

            # Formato dict
            if type(command) == dict:
                # Los parametros del dict, se sobreescriben al nuevo context_item en caso de sobreescribir "action" y
                # "channel", los datos originales se guardan en "from_action" y "from_channel"
                if "action" in command:
                    command["from_action"] = item.action
                if "channel" in command:
                    command["from_channel"] = item.channel
                context_commands.append(
                    (command["title"], item.clone(**command).tourl()))

        # Opciones segun criterios

        # Ir al Menu Principal (channel.mainlist)
        if parent_item.channel not in ["novedades", "channelselector"] and item.action != "mainlist" and parent_item.action != "mainlist":
            context_commands.append(("Ir al Menu Principal", Item(channel=item.channel, action="mainlist").tourl()))

        # Añadir a Favoritos
        if item.channel not in ["favoritos", "biblioteca", "ayuda","configuracion", ""] and not parent_item.channel == "favoritos":
            context_commands.append((config.get_localized_string(30155), item.clone(channel="favoritos", action="addFavourite", from_channel=item.channel, from_action=item.action).tourl()))

        # Añadimos opción contextual para Añadir la serie completa a la biblioteca
        if item.channel != "biblioteca" and item.action in ["episodios", "get_episodios"] \
                and (item.contentSerieName or item.show):
            context_commands.append(("Añadir Serie a Biblioteca", item.clone(action="add_serie_to_library",from_action=item.action).tourl()))

        # Añadir Pelicula a Biblioteca
        if item.channel != "biblioteca" and item.action in ["detail", "findvideos"] \
                and item.contentType == 'movie':
            context_commands.append(("Añadir Pelicula a Biblioteca", item.clone(action="add_pelicula_to_library", from_action=item.action).tourl()))

        # Descargar pelicula
        if item.contentType == "movie" and not item.channel == "descargas":
            context_commands.append(("Descargar Pelicula", item.clone(channel="descargas", action="save_download",from_channel=item.channel, from_action=item.action).tourl()))

        # Descargar serie
        if item.contentType == "tvshow" and not item.channel == "descargas":
            context_commands.append(("Descargar Serie", item.clone(channel="descargas", action="save_download",from_channel=item.channel, from_action=item.action).tourl()))

        # Descargar episodio
        if item.contentType == "episode" and not item.channel == "descargas":
            context_commands.append(("Descargar Episodio", item.clone(channel="descargas", action="save_download",from_channel=item.channel, from_action=item.action).tourl()))

        # Descargar temporada
        if item.contentType == "season" and not item.channel == "descargas":
            context_commands.append(("Descargar Temporada", item.clone(channel="descargas", action="save_download", from_channel=item.channel, from_action=item.action).tourl()))
            
        # Abrir configuración
        if parent_item.channel not in ["configuracion", "novedades", "buscador"]:
            context_commands.append(("Abrir Configuración", Item(channel="configuracion", action="mainlist").tourl()))


        return sorted(context_commands, key=lambda comand: comand[0])


    def dialog_ok(self, heading, line1, line2="", line3=""):
        text = line1
        if line2: text += "\n" + line2
        if line3: text += "\n" + line3
        text = self.kodi_labels_to_html(text)
        JsonData = {}
        JsonData["action"]="Alert" 
        JsonData["data"]={}
        JsonData["data"]["title"]=heading
        JsonData["data"]["text"]=unicode(text ,"utf8","ignore").encode("utf8")
        ID = self.send_message(JsonData)
        self.get_data(ID)

      
    def dialog_notification(self, heading, message, icon=0, time=5000, sound=True):
        JsonData = {}
        JsonData["action"]="notification" 
        JsonData["data"]={}
        JsonData["data"]["title"]=self.kodi_labels_to_html(heading)
        JsonData["data"]["text"]=self.kodi_labels_to_html(message)
        JsonData["data"]["icon"]=icon
        JsonData["data"]["sound"]=sound
        JsonData["data"]["time"]=time
        self.send_message(JsonData)
        return 

    def dialog_yesno(self, heading, line1, line2="", line3="", nolabel="No", yeslabel="Si", autoclose=""):
        text = line1
        if line2: text += "\n" + line2
        if line3: text += "\n" + line3
        text = self.kodi_labels_to_html(text)
        heading = self.kodi_labels_to_html(heading)
        JsonData = {}
        JsonData["action"]="AlertYesNo" 
        JsonData["data"]={}
        JsonData["data"]["title"]=heading
        JsonData["data"]["text"]=text
        ID = self.send_message(JsonData)
        response = self.get_data(ID)
        return response
      
    def dialog_select(self, heading, list): 
        JsonData = {}
        heading = self.kodi_labels_to_html(heading)
        JsonData["action"]="List"
        JsonData["data"]={}
        JsonData["data"]["title"]=heading
        JsonData["data"]["list"]=[]
        for Elemento in list:
          JsonData["data"]["list"].append(self.kodi_labels_to_html(Elemento))
        ID = self.send_message(JsonData)
        response = self.get_data(ID)

        return response
      
    def dialog_progress(self, heading, line1, line2="", line3=""):
        class Dialog(object):
            def __init__(self, heading, line1, line2, line3, platformtools):
                self.platformtools = platformtools
                self.closed = False
                self.heading  = self.platformtools.kodi_labels_to_html(heading)
                text = line1
                if line2: text += "\n" + line2
                if line3: text += "\n" + line3
                text = self.platformtools.kodi_labels_to_html(text)
                JsonData = {}
                JsonData["action"]="Progress" 
                JsonData["data"]={}
                JsonData["data"]["title"]=heading
                JsonData["data"]["text"]=text
                JsonData["data"]["percent"]=0
                
                ID = self.platformtools.send_message(JsonData)
                self.platformtools.get_data(ID)

            def iscanceled(self):
                JsonData = {}
                JsonData["action"]="ProgressIsCanceled" 
                JsonData["data"]={}
                ID = self.platformtools.send_message(JsonData)
                response = self.platformtools.get_data(ID)
                  
                return response

            def update(self, percent, line1, line2="", line3=""):
                text = line1
                if line2: text += "\n" + line2
                if line3: text += "\n" + line3
                text = self.platformtools.kodi_labels_to_html(text)
                JsonData = {}
                JsonData["action"]="ProgressUpdate" 
                JsonData["data"]={}
                JsonData["data"]["title"]=self.heading
                JsonData["data"]["text"]=text
                JsonData["data"]["percent"]=percent
                self.platformtools.send_message(JsonData)

            def close(self):
                JsonData = {}
                JsonData["action"]="ProgressClose" 
                JsonData["data"]={}
                ID = self.platformtools.send_message(JsonData)
                self.platformtools.get_data(ID)
                self.closed = True

        return Dialog(heading, line1, line2, line3, self)


    def dialog_progress_bg(self, heading, message=""):
        class Dialog(object):
            def __init__(self, heading, message, platformtools):
                self.platformtools = platformtools
                self.closed = False
                self.heading  = self.platformtools.kodi_labels_to_html(heading)
                message = self.platformtools.kodi_labels_to_html(message)
                JsonData = {}
                JsonData["action"]="ProgressBG" 
                JsonData["data"]={}
                JsonData["data"]["title"]=heading
                JsonData["data"]["text"]=message
                JsonData["data"]["percent"]=0
                
                ID = self.platformtools.send_message(JsonData)
                self.platformtools.get_data(ID)


            def isFinished(self):
                return not self.closed

            def update(self, percent=0, heading="", message=""):
                JsonData = {}
                JsonData["action"]="ProgressBGUpdate" 
                JsonData["data"]={}
                JsonData["data"]["title"]=self.platformtools.kodi_labels_to_html(heading)
                JsonData["data"]["text"]=self.platformtools.kodi_labels_to_html(message)
                JsonData["data"]["percent"]=percent
                self.platformtools.send_message(JsonData)

            def close(self):
                JsonData = {}
                JsonData["action"]="ProgressBGClose" 
                JsonData["data"]={}
                ID = self.platformtools.send_message(JsonData)
                self.platformtools.get_data(ID)
                self.closed = True
                
        return Dialog(heading, message, self)

    def dialog_input(self, default="", heading="", hidden=False):
        JsonData = {}
        JsonData["action"]="Keyboard" 
        JsonData["data"]={}
        JsonData["data"]["title"] = self.kodi_labels_to_html(heading)
        JsonData["data"]["text"]=default
        JsonData["data"]["password"]=hidden
        ID = self.send_message(JsonData)
        response = self.get_data(ID)

        return response

    def dialog_numeric(self, type, heading, default=""):
        return self.dialog_input("", heading, False) 

    def itemlist_refresh(self):
        JsonData = {}
        JsonData["action"]="Refresh" 
        JsonData["data"]={}
        ID = self.send_message(JsonData)
        self.get_data(ID)

    def itemlist_update(self, item):
        JsonData = {}
        JsonData["action"]="Update" 
        JsonData["data"]={}
        JsonData["data"]["url"]=item.tourl()
        ID = self.send_message(JsonData)

        self.get_data(ID)

    def is_playing(self):
      JsonData = {}
      JsonData["action"]="isPlaying" 
      JsonData["data"]={}
      ID = self.send_message(JsonData)
      response = self.get_data(ID)
      return response

    def play_video(self, item):
        if item.contentTitle:
          title = item.contentTitle
        elif item.fulltitle:
          title = item.fulltitle
        else:
          title = item.title
        
        if item.contentPlot:
          plot = item.contentPlot
        else:
          plot = item.plot  
        

        if item.server=="torrent":
          self.play_torrent(item)
        else:
          JsonData = {}
          JsonData["action"]="Play" 
          JsonData["data"]={}
          JsonData["data"]["title"]= title
          JsonData["data"]["plot"]= plot
          JsonData["data"]["video_url"] =  item.video_url
          JsonData["data"]["url"] =  item.url
          JsonData["data"]["host"] =  self.controller.host
          ID = self.send_message(JsonData)
          self.get_data(ID)
            
    def play_torrent(self,item):
        import time
        import os
        played = False
        
        #Importamos el cliente
        from btserver import Client
        
        #Iniciamos el cliente:
        c = Client(url=item.url, is_playing_fnc=self.is_playing ,wait_time=None, timeout=5, temp_path =os.path.join(config.get_data_path(),"torrent") )

        #Mostramos el progreso
        progreso = self.dialog_progress( "Pelisalacarta - Torrent" , "Iniciando...")
        
        
        #Mientras el progreso no sea cancelado ni el cliente cerrado
        while not progreso.iscanceled() and not c.closed:
          try:
            #Obtenemos el estado del torrent
            s = c.status
            
            #Montamos las tres lineas con la info del torrent
            txt = '%.2f%% de %.1fMB %s | %.1f kB/s' % \
            (s.progress_file, s.file_size, s.str_state, s._download_rate)
            txt2 =  'S: %d(%d) P: %d(%d) | DHT:%s (%d) | Trakers: %d' % \
            (s.num_seeds, s.num_complete, s.num_peers, s.num_incomplete, s.dht_state, s.dht_nodes, s.trackers)
            txt3 = 'Origen Peers TRK: %d DHT: %d PEX: %d LSD %d ' % \
            (s.trk_peers,s.dht_peers, s.pex_peers, s.lsd_peers)
            
            progreso.update(s.buffer,txt, txt2, txt3)
            
            
            time.sleep(1)
            
            #Si el buffer se ha llenado y la reproduccion no ha sido iniciada, se inicia
            if s.buffer == 100 and not played:
              
              #Cerramos el progreso
              progreso.close()
              
              #Obtenemos el playlist del torrent
              item.video_url = c.get_play_list()
              item.server = "directo"
              
              self.play_video(item)
              
              #Marcamos como reproducido para que no se vuelva a iniciar
              played = True
              
              #Y esperamos a que el reproductor se cierre
              while self.is_playing():
                time.sleep(1)
              
              #Cuando este cerrado,  Volvemos a mostrar el dialogo
              progreso = self.dialog_progress( "Pelisalacarta - Torrent" , "Iniciando...")

          except:
            import traceback
            logger.info(traceback.format_exc())
            break
            
        progreso.update(100,"Terminando y eliminando datos"," "," ")
        
        #Detenemos el cliente
        if not c.closed:
          c.stop()
         
        #Y cerramos el progreso
        progreso.close()
          
        return 
        
    def open_settings(self,items):
      from core import config
      JsonData = {}
      JsonData["action"]="OpenConfig"   
      JsonData["data"]={}
      JsonData["data"]["title"]= "Opciones"
      JsonData["data"]["items"]=[]
      
      for item in items:
        if item.get('option') == 'hidden':
           item['hidden'] = True

        for key in item:
          if key in ["lvalues", "label", "category"]:
            try:
              ops = item[key].split("|")
              for x, op in enumerate(ops):
                ops[x] = config.get_localized_string(int(ops[x])) 
              item[key] = "|".join(ops)
            except:
              pass

        JsonData["data"]["items"].append(item)
      ID = self.send_message(JsonData)

      response = self.get_data(ID)
        
      if response:
        from core import config
        config.set_settings(response)
        JsonData = {}
      JsonData["action"]="HideLoading"
      JsonData["data"] = {}
      self.send_message(JsonData)

    def show_channel_settings(self, list_controls=None, dict_values=None, caption="", callback=None, item=None, custom_button=None, channelpath=None):
      from core import config
      from core import channeltools
      from core import servertools
      import inspect
      if not os.path.isdir(os.path.join(config.get_data_path(), "settings_channels")):
         os.mkdir(os.path.join(config.get_data_path(), "settings_channels"))
         
                
      title = caption

      if type(custom_button) == dict:
        custom_button = {"label"    : custom_button.get("label", ""),
                         "function" : custom_button.get("function", ""),
                         "visible"  : bool(custom_button.get("visible", True)),
                         "close"    : bool(custom_button.get("close", False))} 

      else:
        custom_button = None
            
      #Obtenemos el canal desde donde se ha echo la llamada y cargamos los settings disponibles para ese canal
      if not channelpath:
        channelpath = inspect.currentframe().f_back.f_back.f_code.co_filename
      channelname = os.path.basename(channelpath).replace(".py", "")
      ch_type = os.path.basename(os.path.dirname(channelpath))

      #Si no tenemos list_controls, hay que sacarlos del xml del canal
      if not list_controls:      
      
        #Si la ruta del canal esta en la carpeta "channels", obtenemos los controles y valores mediante chaneltools
        if os.path.join(config.get_runtime_path(), "channels") in channelpath:
        
          # La llamada se hace desde un canal
          list_controls, default_values = channeltools.get_channel_controls_settings(channelname)
          kwargs = {"channel": channelname}
          
        #Si la ruta del canal esta en la carpeta "servers", obtenemos los controles y valores mediante servertools
        elif os.path.join(config.get_runtime_path(), "servers") in channelpath:
          # La llamada se hace desde un server
          list_controls, default_values = servertools.get_server_controls_settings(channelname)
          kwargs = {"server": channelname}

        #En caso contrario salimos
        else:
          return None


      #Si no se pasan dict_values, creamos un dict en blanco
      if  dict_values == None:
        dict_values = {}
      
      #Ponemos el titulo
      if caption =="": 
        caption = str(config.get_localized_string(30100)) + " -- " + channelname.capitalize()
      elif caption.startswith('@') and unicode(caption[1:]).isnumeric():
          caption = config.get_localized_string(int(caption[1:]))
      
      
    
      JsonData = {}
      JsonData["action"]="OpenConfig"   
      JsonData["data"]={}
      JsonData["data"]["title"] = self.kodi_labels_to_html(caption)
      JsonData["data"]["custom_button"]=custom_button
      JsonData["data"]["items"]=[]
      

      # Añadir controles
      for c in list_controls:
          if not "default" in c: c["default"] = ""
          if not "color" in c: c["color"] = "auto"
          if not "label" in c: continue
          
          #Obtenemos el valor
          if not c["id"] in dict_values:
            if not callback:
              c["value"]= config.get_setting(c["id"], **kwargs)
            else:
              c["value"] = c["default"]

            dict_values[c["id"]] = c["value"]

          else:
            c["value"] = dict_values[c["id"]]
            
          # Translation
          if c['label'].startswith('@') and unicode(c['label'][1:]).isnumeric():
              c['label'] = str(config.get_localized_string(c['label'][1:]))
          if c["label"].endswith (":"): c["label"] = c["label"][:-1]
          
          if c['type'] == 'list':
              lvalues=[]
              for li in c['lvalues']:
                  if li.startswith('@') and unicode(li[1:]).isnumeric():
                      lvalues.append(str(config.get_localized_string(li[1:])))
                  else:
                      lvalues.append(li)
              c['lvalues'] = lvalues
              
          c["label"] = self.kodi_labels_to_html(c["label"])
          
          JsonData["data"]["items"].append(c)
        
      ID = self.send_message(JsonData)
      close = False
      
      while True:
        data = self.get_data(ID)
        if type(data) == dict:
          JsonData["action"]="HideLoading"
          JsonData["data"] = {}
          self.send_message(JsonData)
        
          for v in data:
              if data[v] == "true": data[v] = True
              if data[v] == "false": data[v] = False
              if unicode(data[v]).isnumeric():  data[v] =  int(data[v])
              
          if callback and '.' in callback:
              package, callback = callback.rsplit('.', 1)
          else:
              package = '%s.%s' % (ch_type, channelname)  
                
          cb_channel = None
          try:
              cb_channel = __import__(package, None, None, [package])
          except ImportError:
              logger.error('Imposible importar %s' % package)

          if callback:
              # Si existe una funcion callback la invocamos ...
              return getattr(cb_channel, callback)(item, data)
          else:
              # si no, probamos si en el canal existe una funcion 'cb_validate_config' ...
              try:
                  return getattr(cb_channel, 'cb_validate_config')(item, data)
              except AttributeError:
                  # ... si tampoco existe 'cb_validate_config'...
                  for v in data:
                      config.set_setting(v,data[v], **kwargs)
          
        elif data == "custom_button":
            if '.' in callback:
                package, callback = callback.rsplit('.', 1)
            else:
                package = '%s.%s' % (ch_type, channelname)
            try:
                cb_channel = __import__(package, None, None, [package])
            except ImportError:
                logger.error('Imposible importar %s' % package)
            else:
                return_value = getattr(cb_channel, custom_button['function'])(item, dict_values)          
                if custom_button["close"] == True:
                    return return_value
                else:
                    JsonData["action"]="custom_button"
                    JsonData["data"] = {}
                    JsonData["data"]["values"] = dict_values
                    JsonData["data"]["return_value"] = return_value
                    ID = self.send_message(JsonData)
                        
        elif data == False:
          return None
         
    def show_video_info(self,data, caption="", item=None, scraper=Tmdb):
        from platformcode import html_info_window
        return html_info_window.InfoWindow().Start(self, data, caption, item, scraper)
    
    def show_recaptcha(self, key, url):
        from platformcode import html_recaptcha
        return html_recaptcha.recaptcha().start(self, key, url)
    
    def kodi_labels_to_html(self, text):
      text = re.sub(r"(?:\[I\])(.*?)(?:\[/I\])", r"<i>\1</i>", text)
      text = re.sub(r"(?:\[B\])(.*?)(?:\[/B\])", r"<b>\1</b>", text)
      text = re.sub(r"(?:\[COLOR (?:0x)?([0-f]{2})([0-f]{2})([0-f]{2})([0-f]{2})\])(.*?)(?:\[/COLOR\])", lambda m: "<span style='color: rgba(%s,%s,%s,%s)'>%s</span>" %(int(m.group(2),16), int(m.group(3),16), int(m.group(4),16), int(m.group(1),16) / 255.0, m.group(5)), text)
      text = re.sub(r"(?:\[COLOR (?:0x)?([0-f]{2})([0-f]{2})([0-f]{2})\])(.*?)(?:\[/COLOR\])", r"<span style='color: #\1\2\3'>\4</span>", text)
      text = re.sub(r"(?:\[COLOR (?:0x)?([a-z|A-Z]+)\])(.*?)(?:\[/COLOR\])", r"<span style='color: \1'>\2</span>", text)
      return text