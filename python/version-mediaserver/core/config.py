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
# Parámetros de configuración (mediaserver)
# ------------------------------------------------------------

import os
import re
import threading

PLATFORM_NAME = "mediaserver"
PLUGIN_NAME = "pelisalacarta"

settings_dic ={}
settings_types = {}
adult_setting = {}


def get_platform(full_version=False):
    #full_version solo es util en xbmc/kodi
    ret = {
        'num_version': 1.0 ,
        'name_version': PLATFORM_NAME ,
        'video_db': "",
        'plaform': PLATFORM_NAME
        }

    if full_version:
        return ret
    else:
        return PLATFORM_NAME


def is_xbmc():
    return False


def get_library_support():
    return True


def get_system_platform():
    """ fonction: pour recuperer la platform que xbmc tourne """
    platform = "unknown"
    if sys.platform == "linux" or sys.platform == "linux2":
        platform = "linux"
    elif sys.platform == "darwin":
        platform = "osx"
    elif sys.platform == "win32":
        platform = "windows"
    
    return platform


def open_settings():
    Opciones =[]
    from xml.dom import minidom
    settings = open(menufilepath, 'rb').read()
    xmldoc= minidom.parseString(settings)
    for category in xmldoc.getElementsByTagName("category"):
      for setting in category.getElementsByTagName("setting"):
        Opciones.append(dict(setting.attributes.items() + [(u"category",category.getAttribute("label")),(u"value",get_setting(setting.getAttribute("id")))]))

    from platformcode import platformtools
    global adult_setting
    adult_password = get_setting('adult_password')
    if not adult_password:
        adult_password = set_setting('adult_password', '0000')
    adult_mode = get_setting('adult_mode')
    adult_request_password = get_setting('adult_request_password')

    platformtools.open_settings(Opciones)

    # Hemos accedido a la seccion de Canales para adultos
    if get_setting('adult_aux_intro_password'):
        # La contraseña de acceso es correcta
        if get_setting('adult_aux_intro_password') == adult_password:
            
            # Cambio de contraseña
            if get_setting('adult_aux_new_password1'):
                if get_setting('adult_aux_new_password1') == get_setting('adult_aux_new_password2'):
                    set_setting('adult_password', get_setting('adult_aux_new_password1'))
                else:
                    platformtools.dialog_ok("Canales para adultos",
                                    "Los campos 'Nueva contraseña' y 'Confirmar nueva contraseña' no coinciden.",
                                    "Entre de nuevo en 'Preferencias' para cambiar la contraseña")



            # Fijar adult_pin
            adult_pin = ""
            if get_setting("adult_request_password") == True:
                adult_pin = get_setting("adult_password")
            set_setting("adult_pin", adult_pin)
            
            #Solo esta sesion:
            id = threading.current_thread().name
            if get_setting("adult_mode") == 2:
              adult_setting[id] = True
              set_setting("adult_mode", "0")
            else:
              adult_setting = {}

        else:
            platformtools.dialog_ok("Canales para adultos", "La contraseña no es correcta.",
                                    "Los cambios realizados en esta sección no se guardaran.")
            # Deshacer cambios
            set_setting("adult_mode", adult_mode)
            set_setting("adult_request_password", adult_request_password)


        # Borramos settings auxiliares
        set_setting('adult_aux_intro_password', '')
        set_setting('adult_aux_new_password1', '')
        set_setting('adult_aux_new_password2', '')


def get_setting(name, channel="", server=""):
    """
    Retorna el valor de configuracion del parametro solicitado.

    Devuelve el valor del parametro 'name' en la configuracion global o en la configuracion propia del canal 'channel'.

    Si se especifica el nombre del canal busca en la ruta \addon_data\plugin.video.pelisalacarta\settings_channels el
    archivo channel_data.json y lee el valor del parametro 'name'. Si el archivo channel_data.json no existe busca en la
     carpeta channels el archivo channel.xml y crea un archivo channel_data.json antes de retornar el valor solicitado.
    Si el parametro 'name' no existe en channel_data.json lo busca en la configuracion global y si ahi tampoco existe
    devuelve un str vacio.

    Parametros:
    name -- nombre del parametro
    channel [opcional] -- nombre del canal

    Retorna:
    value -- El valor del parametro 'name'

    """

    # Specific channel setting
    if channel:

        # logger.info("config.get_setting reading channel setting '"+name+"' from channel xml")
        from core import channeltools
        value = channeltools.get_channel_setting(name, channel)
        # logger.info("config.get_setting -> '"+repr(value)+"'")

        return value
            
    elif server:
        # logger.info("config.get_setting reading server setting '"+name+"' from server xml")
        from core import servertools
        value = servertools.get_server_setting(name, server)
        # logger.info("config.get_setting -> '"+repr(value)+"'")

        return value

    # Global setting
    else:
        # logger.info("config.get_setting reading main setting '"+name+"'")
        global settings_dic
        value = settings_dic.get(name, "")
        
        if name == "adult_mode":
            global adult_setting
            id = threading.current_thread().name
            if adult_setting.get(id) == True:
                value = "2"


        # hack para devolver el tipo correspondiente
        global settings_types

        if settings_types.get(name) in ['enum', 'number']:
            try:
                value = int(value)
            except:
                value = 0

        elif settings_types.get(name) == 'bool':
            value = value == 'true'

        elif not settings_types.has_key(name):
            try:
                t = eval (value)
                value = t[0](t[1])
            except:
                value = None


        return value


def set_setting(name, value, channel="", server=""):
    """
    Fija el valor de configuracion del parametro indicado.

    Establece 'value' como el valor del parametro 'name' en la configuracion global o en la configuracion propia del
    canal 'channel'.
    Devuelve el valor cambiado o None si la asignacion no se ha podido completar.

    Si se especifica el nombre del canal busca en la ruta \addon_data\plugin.video.pelisalacarta\settings_channels el
    archivo channel_data.json y establece el parametro 'name' al valor indicado por 'value'. Si el archivo
    channel_data.json no existe busca en la carpeta channels el archivo channel.xml y crea un archivo channel_data.json
    antes de modificar el parametro 'name'.
    Si el parametro 'name' no existe lo añade, con su valor, al archivo correspondiente.


    Parametros:
    name -- nombre del parametro
    value -- valor del parametro
    channel [opcional] -- nombre del canal

    Retorna:
    'value' en caso de que se haya podido fijar el valor y None en caso contrario

    """
    if channel:
        from core import channeltools
        return channeltools.set_channel_setting(name, value, channel)
    elif server:
        from core import servertools
        return servertools.set_server_setting(name, value, server)
    else:
        global settings_dic
        global settings_types


        if settings_types.get(name) == 'bool':
            if value:
                new_value = "true"
            else:
                new_value = "false"

        elif settings_types.get(name):
            new_value = str(value)

        else:
            if isinstance(value, basestring):
                new_value = "(%s, %s)" % (type(value).__name__, repr(value))
            else:
                new_value = "(%s, %s)" % (type(value).__name__, value)


        settings_dic[name]=new_value

        from xml.dom import minidom
        #Crea un Nuevo XML vacio
        new_settings = minidom.getDOMImplementation().createDocument(None, "settings", None)
        new_settings_root = new_settings.documentElement
      
        for key in settings_dic:
          nodo = new_settings.createElement("setting")
          nodo.setAttribute("value",settings_dic[key])
          nodo.setAttribute("id",key)    
          new_settings_root.appendChild(nodo)
        
        fichero = open(configfilepath, "w")
        fichero.write(new_settings.toprettyxml(encoding='utf-8'))
        fichero.close()
        return value


def get_localized_string(code):
    translationsfile = open(TRANSLATION_FILE_PATH,"r")
    translations = translationsfile.read()
    translationsfile.close()
    cadenas = re.findall('<string id="%s">([^<]+)<' % code,translations)
    if len(cadenas)>0:
        dev =  cadenas[0]
    else:
        dev =  "%d" % code

    try:
        dev = dev.encode("utf-8")
    except:
        pass

    return dev


def get_library_path():
    value = get_setting("librarypath")
    if value == "":
        verify_directories_created()
        value = get_setting("librarypath")

    return value


def get_temp_file(filename):
    import tempfile
    return os.path.join(tempfile.gettempdir(), filename)


def get_runtime_path():
    return os.getcwd()


def get_data_path():
    dev = os.path.join( os.path.expanduser("~") , ".pelisalacarta" )

    #Crea el directorio si no existe
    if not os.path.exists(dev):
        os.makedirs(dev)

    return dev


def get_cookie_data():
    import os
    ficherocookies = os.path.join(get_data_path(), 'cookies.dat')

    cookiedatafile = open(ficherocookies, 'r')
    cookiedata = cookiedatafile.read()
    cookiedatafile.close()

    return cookiedata


# Test if all the required directories are created
def verify_directories_created():
    from core import logger
    from core import filetools

    config_paths = [["librarypath",      "library"],
                    ["downloadpath",     "downloads"],
                    ["downloadlistpath", "downloads/list"],
                    ["bookmarkpath",     "favorites"],
                    ["settings_path",    "settings_channels"]]
    
    
    for path, default in config_paths:
      saved_path = get_setting(path)
      if not saved_path:
        saved_path = filetools.join(get_data_path() , *default.split("/"))
        set_setting(path, saved_path)

      if not filetools.exists(saved_path): 
        logger.debug("Creating %s: %s" % (path, saved_path))
        filetools.mkdir(saved_path)
        
        #Biblioteca
        if path == "librarypath":
          set_setting("library_version", "v4")



def get_local_ip():
  import socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('8.8.8.8', 53))  # connecting to a UDP address doesn't send packets
  myip = s.getsockname()[0]
  return myip


def load_settings():
    global settings_dic
    global settings_types
    defaults = {}
    from xml.etree import ElementTree
   
    encontrado = False
    #Lee el archivo XML (si existe)
    if os.path.exists(configfilepath):
      settings = open(configfilepath, 'rb').read()
      root = ElementTree.fromstring(settings)
      for target in root.findall("setting"):
        settings_dic[target.get("id")] = target.get("value")


    defaultsettings = open(menufilepath, 'rb').read()
    root = ElementTree.fromstring(defaultsettings)
    for category in root.findall("category"):
      for target in category.findall("setting"):
        if target.get("id"):
          defaults[target.get("id")] = target.get("default")
          settings_types[target.get("id")] = target.get("type")
      
    for key in defaults:
      if not key in settings_dic:
        settings_dic[key] = defaults[key]
    set_settings(settings_dic)



def set_settings(JsonRespuesta):
    for Ajuste in JsonRespuesta:
      settings_dic[Ajuste]=JsonRespuesta[Ajuste].encode("utf8")
    from xml.dom import minidom
    #Crea un Nuevo XML vacio
    new_settings = minidom.getDOMImplementation().createDocument(None, "settings", None)
    new_settings_root = new_settings.documentElement
    
    for key in settings_dic:
      nodo = new_settings.createElement("setting")
      nodo.setAttribute("value",settings_dic[key])
      nodo.setAttribute("id",key)    
      new_settings_root.appendChild(nodo)
      
    fichero = open(configfilepath, "w")
    fichero.write(new_settings.toprettyxml(encoding='utf-8'))
    fichero.close()



# Fichero de configuración
menufilepath= os.path.join(get_runtime_path(),"resources", "settings.xml")
configfilepath = os.path.join( get_data_path() , "settings.xml")
if not os.path.exists(get_data_path()): os.mkdir(get_data_path())   
# Literales
TRANSLATION_FILE_PATH = os.path.join(get_runtime_path(),"resources","language","Spanish","strings.xml")
load_settings()
