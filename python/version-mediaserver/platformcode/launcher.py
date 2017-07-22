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
# Mediaserver Launcher
# ------------------------------------------------------------

import os
import sys
from core.item import Item
from core import logger
from core import config
from platformcode import platformtools
from core import channeltools
import channelselector
from core import servertools
from core import library

def start():
    """ Primera funcion que se ejecuta al entrar en el plugin.
    Dentro de esta funcion deberian ir todas las llamadas a las
    funciones que deseamos que se ejecuten nada mas abrir el plugin.
    """
    logger.info()

    # Test if all the required directories are created
    config.verify_directories_created()
    import library_service
    library_service.start()
      

def run(item):
    itemlist = []
    #Muestra el item en el log:
    PrintItems(item)
    
      
    #Control Parental, comprueba si es adulto o no
    if item.action=="mainlist":
      # Parental control
      if channeltools.is_adult(item.channel) and config.get_setting("adult_pin")!="":
        tecleado = platformtools.dialog_input("","Contraseña para canales de adultos",True)
        if tecleado is None or tecleado != config.get_setting("adult_pin"):
            platformtools.render_items(None, item)
            return

    #Importa el canal para el item, todo item debe tener un canal, sino sale de la función
    if item.channel: channelmodule = ImportarCanal(item)
    
    # If item has no action, stops here
    if item.action == "":
        logger.info("Item sin accion")
        itemlist = None
        
    #Action Play, para mostrar el menú con las opciones de reproduccion.
    elif item.action=="play":
      logger.info("play")
      # Si el canal tiene una acción "play" tiene prioridad
      if hasattr(channelmodule, 'play'):
          logger.info("executing channel 'play' method")
          itemlist = channelmodule.play(item)
          b_favourite = item.isFavourite
          if len(itemlist)>0 and isinstance(itemlist[0], Item):
              item = itemlist[0]
              if b_favourite:
                  item.isFavourite = True
              play_menu(item)
          elif len(itemlist)>0 and isinstance(itemlist[0], list):
              item.video_urls = itemlist
              play_menu(item)
          else:
              platformtools.dialog_ok("plugin", "No hay nada para reproducir")
      else:
          logger.info("no channel 'play' method, executing core method")
          play_menu(item)
          
      itemlist = None
    
      
    #Action Search, para mostrar el teclado y lanzar la busqueda con el texto indicado. 
    elif item.action=="search":
      logger.info("search")
      tecleado = platformtools.dialog_input()
      if not tecleado is None:
          itemlist = channelmodule.search(item,tecleado)
      else:
          itemlist = []


    elif item.channel == "channelselector":
      import channelselector
      if item.action =="mainlist":
        itemlist = channelselector.getmainlist("bannermenu")
      if item.action =="getchanneltypes":
        itemlist = channelselector.getchanneltypes("bannermenu")
      if item.action =="filterchannels":
        itemlist = channelselector.filterchannels(item.channel_type, "bannermenu")
                   
    #Todas las demas las intenta ejecturaren el siguiente orden:
    # 1. En el canal
    # 2. En el launcher
    # 3. Si no existe en el canal ni en el launcher guarda un error en el log
    else:
      #Si existe la funcion en el canal la ejecuta
      if hasattr(channelmodule, item.action):
        logger.info("Ejectuando accion: " + item.channel + "." + item.action + "(item)")
        exec "itemlist = channelmodule." + item.action + "(item)"
        
      #Si existe la funcion en el launcher la ejecuta
      elif hasattr(sys.modules[__name__], item.action):
        logger.info("Ejectuando accion: " + item.action + "(item)")
        exec "itemlist =" + item.action + "(item)"
        
      #Si no existe devuelve un error
      else:
          logger.info("No se ha encontrado la accion ["+ item.action + "] en el canal ["+item.channel+"] ni en el launcher")
          
     
          
    #Llegados a este punto ya tenemos que tener el itemlist con los resultados correspondientes
    #Pueden darse 3 escenarios distintos:
    # 1. la función ha generado resultados y estan en el itemlist
    # 2. la función no ha generado resultados y por tanto el itemlist contiene 0 items, itemlist = []
    # 3. la función realiza alguna accion con la cual no se generan nuevos items, en ese caso el resultado deve ser: itemlist = None para que no modifique el listado
    #A partir de aquí ya se ha ejecutado la funcion en el lugar adecuado, si queremos realizar alguna acción sobre los resultados, este es el lugar.
          
    
     
    #Filtrado de Servers      
    if item.action== "findvideos":
        itemlist = servertools.filter_servers(itemlist)
      
    
    #Si la accion no ha devuelto ningún resultado, añade un item con el texto "No hay elementos para mostrar"              
    if type(itemlist)==list:
      if  len(itemlist) ==0:
        itemlist = [Item(title="No hay elementos para mostrar", thumbnail="https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/thumb_error.png")]
    
      #Imprime en el log el resultado
      PrintItems(itemlist)
      
    #Muestra los resultados en pantalla
    platformtools.render_items(itemlist, item)


def ImportarCanal(item):
  channel = item.channel
  channelmodule=""
  if os.path.exists(os.path.join( config.get_runtime_path(), "channels",channel+".py")):
    exec "from channels import "+channel+" as channelmodule"
  elif os.path.exists(os.path.join( config.get_runtime_path(),"core",channel+".py")):
    exec "from core import "+channel+" as channelmodule"
  elif os.path.exists(os.path.join( config.get_runtime_path(),channel+".py")):
    exec "import "+channel+" as channelmodule"
  return channelmodule

def PrintItems(itemlist):
  if type(itemlist)==list:
    if len(itemlist) >0:
      logger.info("Items devueltos")  
      logger.info("-----------------------------------------------------------------------")
      for item in itemlist:
        logger.info(item.tostring())
      logger.info("-----------------------------------------------------------------------")
  else:
    item =  itemlist
    logger.info("-----------------------------------------------------------------------")
    logger.info(item.tostring())    
    logger.info("-----------------------------------------------------------------------")

  
def findvideos(item):
    logger.info()
    itemlist = servertools.find_video_items(item)        
    return itemlist

def add_pelicula_to_library(item):

  library.add_pelicula_to_library(item)
                
def add_serie_to_library(item):
  channel = ImportarCanal(item)
  library.add_serie_to_library(item, channel)

def download_all_episodes(item,first_episode="",preferred_server="vidspot",filter_language=""):
    logger.info("show="+item.show)
    channel = ImportarCanal(item)
    show_title = item.show

    # Obtiene el listado desde el que se llamó
    action = item.extra

    # Esta marca es porque el item tiene algo más aparte en el atributo "extra"
    if "###" in item.extra:
        action = item.extra.split("###")[0]
        item.extra = item.extra.split("###")[1]

    exec "episode_itemlist = channel."+action+"(item)"

    # Ordena los episodios para que funcione el filtro de first_episode
    episode_itemlist = sorted(episode_itemlist, key=lambda Item: Item.title) 

    from core import downloadtools
    from core import scrapertools

    best_server = preferred_server
    worst_server = "moevideos"

    # Para cada episodio
    if first_episode=="":
        empezar = True
    else:
        empezar = False

    for episode_item in episode_itemlist:
        try:
            logger.info("episode="+episode_item.title)
            episode_title = scrapertools.get_match(episode_item.title,"(\d+x\d+)")
            logger.info("episode="+episode_title)
        except:
            import traceback
            logger.error(traceback.format_exc())
            continue

        if first_episode!="" and episode_title==first_episode:
            empezar = True

        if episodio_ya_descargado(show_title,episode_title):
            continue

        if not empezar:
            continue

        # Extrae los mirrors
        try:
            mirrors_itemlist = channel.findvideos(episode_item)
        except:
            mirrors_itemlist = servertools.find_video_items(episode_item)
        print mirrors_itemlist

        descargado = False

        new_mirror_itemlist_1 = []
        new_mirror_itemlist_2 = []
        new_mirror_itemlist_3 = []
        new_mirror_itemlist_4 = []
        new_mirror_itemlist_5 = []
        new_mirror_itemlist_6 = []

        for mirror_item in mirrors_itemlist:
            
            # Si está en español va al principio, si no va al final
            if "(Español)" in mirror_item.title:
                if best_server in mirror_item.title.lower():
                    new_mirror_itemlist_1.append(mirror_item)
                else:
                    new_mirror_itemlist_2.append(mirror_item)
            elif "(Latino)" in mirror_item.title:
                if best_server in mirror_item.title.lower():
                    new_mirror_itemlist_3.append(mirror_item)
                else:
                    new_mirror_itemlist_4.append(mirror_item)
            elif "(VOS)" in mirror_item.title:
                if best_server in mirror_item.title.lower():
                    new_mirror_itemlist_3.append(mirror_item)
                else:
                    new_mirror_itemlist_4.append(mirror_item)
            else:
                if best_server in mirror_item.title.lower():
                    new_mirror_itemlist_5.append(mirror_item)
                else:
                    new_mirror_itemlist_6.append(mirror_item)

        mirrors_itemlist = new_mirror_itemlist_1 + new_mirror_itemlist_2 + new_mirror_itemlist_3 + new_mirror_itemlist_4 + new_mirror_itemlist_5 + new_mirror_itemlist_6

        for mirror_item in mirrors_itemlist:
            logger.info("mirror="+mirror_item.title)

            if "(Español)" in mirror_item.title:
                idioma="(Español)"
                codigo_idioma="es"
            elif "(Latino)" in mirror_item.title:
                idioma="(Latino)"
                codigo_idioma="lat"
            elif "(VOS)" in mirror_item.title:
                idioma="(VOS)"
                codigo_idioma="vos"
            elif "(VO)" in mirror_item.title:
                idioma="(VO)"
                codigo_idioma="vo"
            else:
                idioma="(Desconocido)"
                codigo_idioma="desconocido"

            logger.info("filter_language=#"+filter_language+"#, codigo_idioma=#"+codigo_idioma+"#")
            if filter_language=="" or (filter_language!="" and filter_language==codigo_idioma):
                logger.info("downloading mirror")
            else:
                logger.info("language "+codigo_idioma+" filtered, skipping")
                continue

            if hasattr(channel, 'play'):
                video_items = channel.play(mirror_item)
            else:
                video_items = [mirror_item]

            if len(video_items)>0:
                video_item = video_items[0]

                # Comprueba que esté disponible
                video_urls, puedes, motivo = servertools.resolve_video_urls_for_playing( video_item.server , video_item.url , video_password="" , muestra_dialogo=False)

                # Lo añade a la lista de descargas
                if puedes:
                    logger.info("downloading mirror started...")
                    # El vídeo de más calidad es el último
                    mediaurl = video_urls[len(video_urls)-1][1]
                    devuelve = downloadtools.downloadbest(video_urls,show_title+" "+episode_title+" "+idioma+" ["+video_item.server+"]",continuar=False)

                    if devuelve==0:
                        logger.info("download ok")
                        descargado = True
                        break
                    elif devuelve==-1:
                        try:
                            
                            platformtools.dialog_ok("plugin" , "Descarga abortada")
                        except:
                            pass
                        return
                    else:
                        logger.info("download error, try another mirror")
                        continue

                else:
                    logger.info("downloading mirror not available... trying next")

        if not descargado:
            logger.info("EPISODIO NO DESCARGADO "+episode_title)



def add_to_favorites(item):
    #Proviene del menu contextual:
    if "item_action" in item:
      item.action = item.item_action
      del item.item_action
      item.context=[]

    from channels import favoritos
    from core import downloadtools
    if not item.fulltitle: item.fulltitle = item.title
    title = platformtools.dialog_input(default=downloadtools.limpia_nombre_excepto_1(item.fulltitle)+" ["+item.channel+"]")
    if title is not None:
        item.title = title
        favoritos.addFavourite(item)
        platformtools.dialog_ok("Pelisalacarta", config.get_localized_string(30102) +"\n"+ item.title +"\n"+ config.get_localized_string(30108))
    return
    
def remove_from_favorites(item):
    from channels import favoritos
    # En "extra" está el nombre del fichero en favoritos
    favoritos.delFavourite(item.extra)
    platformtools.dialog_ok("Pelisalacarta", config.get_localized_string(30102) +"\n"+ item.title +"\n"+ config.get_localized_string(30105))
    platformtools.itemlist_refresh()
    return

def download(item):
    from channels import descargas
    if item.contentType == "list" or item.contentType == "tvshow":
      item.contentType = "video"
    item.play_menu = True
    descargas.save_download(item)
    return

def add_to_library(item):
    if "item_action" in item: 
      item.action = item.item_action
      del item.item_action

    
    if not item.fulltitle=="":
        item.title = item.fulltitle
    library.savelibrary(item)
    platformtools.dialog_ok("Pelisalacarta", config.get_localized_string(30101) +"\n"+ item.title +"\n"+ config.get_localized_string(30135))
    return
    
def delete_file(item):
  os.remove(item.url)
  platformtools.itemlist_refresh()
  return

def send_to_jdownloader(item):
  #d = {"web": url}urllib.urlencode(d)
  from core import scrapertools
  if item.subtitle!="":
      data = scrapertools.cachePage(config.get_setting("jdownloader")+"/action/add/links/grabber0/start1/web="+item.url+ " " +item.thumbnail + " " + item.subtitle)
  else:
      data = scrapertools.cachePage(config.get_setting("jdownloader")+"/action/add/links/grabber0/start1/web="+item.url+ " " +item.thumbnail)
  return

def send_to_pyload(item):
  logger.info("Enviando a pyload...")
  
  if item.Serie!="":
      package_name = item.Serie
  else:
      package_name = "pelisalacarta"

  from core import pyload_client
  pyload_client.download(url=item.url,package_name=package_name)
  return

def search_trailer(item):
  config.set_setting("subtitulo", False)
  item.channel = "trailertools"
  item.action ="buscartrailer"
  item.contextual=True
  run(item)
  return

#Crea la lista de opciones para el menu de reproduccion
def check_video_options(item, video_urls):
  itemlist = []
  #Opciones Reproducir
  playable = (len(video_urls) > 0)
  
  for video_url in video_urls:
    itemlist.append(item.clone(option=config.get_localized_string(30151) + " " + video_url[0], video_url= video_url[1], action="play_video"))
  
  if item.server=="local":                            
    itemlist.append(item.clone(option=config.get_localized_string(30164), action="delete_file"))
    
  if not item.server=="local" and playable:           
    itemlist.append(item.clone(option=config.get_localized_string(30153), action="download", video_urls = video_urls))

  if item.channel=="favoritos":                       
    itemlist.append(item.clone(option=config.get_localized_string(30154), action="remove_from_favorites"))
    
  if not item.channel=="favoritos" and playable:      
    itemlist.append(item.clone(option=config.get_localized_string(30155), action="add_to_favorites", item_action = item.action))

  if not item.strmfile and playable and item.contentType == "movie":                  
    itemlist.append(item.clone(option=config.get_localized_string(30161), action="add_to_library", item_action = item.action))

  if config.get_setting("jdownloader_enabled")== True and playable:
    itemlist.append(item.clone(option=config.get_localized_string(30158), action="send_to_jdownloader"))
  if config.get_setting("pyload_enabled")== True and playable:
    itemlist.append(item.clone(option=config.get_localized_string(30158).replace("jdownloader","pyLoad"), action="send_to_pyload")) 
    
  if not item.channel in ["Trailer","ecarteleratrailers"] and playable:
    itemlist.append(item.clone(option=config.get_localized_string(30162), action="search_trailer"))
    
  return itemlist

#play_menu, abre el menu con las opciones para reproducir
def play_menu(item):

    if item.server=="": item.server="directo"
    
    if item.video_urls:
      video_urls,puedes,motivo = item.video_urls, True, ""
    else:
      video_urls,puedes,motivo = servertools.resolve_video_urls_for_playing(item.server,item.url,item.password,True)
      
    if not "strmfile" in item: item.strmfile=False   
    #TODO: unificar show y Serie ya que se usan indistintamente.
    if not "Serie" in item: item.Serie = item.show
    if item.server=="": item.server="directo"
    
    opciones = check_video_options(item, video_urls)
    if not puedes:
      if item.server!="directo":
        motivo = motivo.replace("<br/>", "\n")
        platformtools.dialog_ok("No puedes ver ese vídeo porque...",motivo+"\n"+item.url)
      else:
        platformtools.dialog_ok("No puedes ver ese vídeo porque...","El servidor donde está alojado no está\nsoportado en pelisalacarta todavía\n"+item.url)

    if len(opciones)==0:
        return
        
    default_action = config.get_setting("default_action")
    logger.info("default_action=%s" % (default_action))
    # Si la accion por defecto es "Preguntar", pregunta
    if default_action==0:
        seleccion = platformtools.dialog_select(config.get_localized_string(30163), [opcion.option for opcion in opciones])
    elif default_action==1:
        seleccion = 0
    elif default_action==2:
        seleccion = len(video_urls)-1
    elif default_action==3:
        seleccion = seleccion
    else:
        seleccion=0

    if seleccion > -1:
      logger.info("seleccion=%d" % seleccion)
      logger.info("seleccion=%s" % opciones[seleccion].option)
      selecteditem = opciones[seleccion]
      del selecteditem.option
      run(opciones[seleccion])

    return

#play_video, Llama a la función especifica de la plataforma para reproducir
def play_video(item):
    platformtools.play_video(item) 
