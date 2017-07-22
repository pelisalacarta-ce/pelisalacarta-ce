# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Configuracion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os, re
import bridge
from types import *

PLATFORM_NAME = "plex"
settings_types = None

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
    return False


def get_system_platform():
    return ""


def open_settings():
    return

  
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
        from core import channeltools
        return channeltools.get_channel_setting(name, channel)

            
    elif server:
        from core import servertools
        return servertools.get_server_setting(name, server)

    # Global setting
    else:
        # Devolvemos el valor del parametro global 'name'
        if name=="cache.dir":
            value = ""

        if name=="debug" or name=="download.enabled":
            value = False
	    
        if name=="cookies.dir":
            value = os.getcwd() #TODO no parece funcionar
	
        if name=="cache.mode" or name=="thumbnail_type":
            value = 2

        else:
            value = bridge.get_setting(name)

            # hack para devolver el tipo correspondiente
            settings_types = get_settings_types()

            if isinstance(settings_types.get(name),tuple) and settings_types[name][0] == 'enum':
                value = settings_types[name][1].index(value)

            elif settings_types.get(name) == 'bool':
                value = bool(value)

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
        try:
            settings_types = get_settings_types()

            if settings_types.has_key(name):
                # El parametro esta en Preferences: lo abrimos y eliminamos la linea
                sep = os.path.sep
                user_preferences = get_data_path().replace(sep + "Data" + sep, sep + "Preferences" + sep) + ".xml"
                data = open(user_preferences, "rb").readlines()

                for line in data:
                    if re.match("<%s/?>" % name, line.strip()):
                        data.remove(line)

                # Añadir al final del listado el parametro con su nuevo valor
                if value:
                    data.insert(-1, "  <{0}>{1}</{0}>\n".format(name, value))
                else:
                    data.insert(-1, "  <{0}/>\n".format(name))

                # Guardar el archivo de nuevo
                out_file = open(user_preferences, "wb")
                for line in data:
                    out_file.write(line)

            else:
                # El parametro no esta en Preferences: Lo añadimos a dict_global
                bridge.dict_global[name] = value

        except:
            return None

    return value


def get_settings_types():
    """
    Devuelve un diccionario con los parametros (key) de la configuracion global y sus tipos (value)

    :return: dict
    """
    global settings_types

    if not settings_types:
        from core import jsontools

        settings_types = {}
        fname = os.path.abspath( os.path.join( os.path.dirname(__file__) , "..", "..", "..", "DefaultPrefs.json" ) )
        infile = open(fname)
        data = infile.read()
        infile.close()

        for d in jsontools.load_json(data):
            if d["type"] == 'enum':
                settings_types[d["id"]] = (d["type"],d["values"])
            else:
                settings_types[d["id"]] = d["type"]

    return settings_types


def get_localized_string(code):
   import bridge
   return bridge.get_localized_string(code)

def get_library_path():
   return ""

def get_temp_file(filename):
   return ""

def get_runtime_path():
   return os.path.abspath( os.path.join( os.path.dirname(__file__) , ".." ) )

def get_data_path():
   return os.getcwd()

def get_cookie_data():
   import os
   ficherocookies = os.path.join( get_data_path(), 'cookies.lwp' )

   cookiedatafile = open(ficherocookies,'r')
   cookiedata = cookiedatafile.read()
   cookiedatafile.close()

   return cookiedata

def verify_directories_created():
   return
