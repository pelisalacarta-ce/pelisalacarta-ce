# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parámetros de configuración (mediaserver)
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

import sys
import os
import re
import ConfigParser

PLATFORM_NAME = "command-line"
PLUGIN_NAME = "pelisalacarta"

# Fichero de configuración global
CONFIG_FILE_PATH = os.path.join( os.getcwd(),'resources','settings.conf')
print "Config file path "+CONFIG_FILE_PATH

configfile = ConfigParser.SafeConfigParser()
configfile.read( CONFIG_FILE_PATH )

overrides = dict()

TRANSLATION_FILE_PATH = os.path.join(os.getcwd(),"resources","language","Spanish","strings.xml")
try:
    translationsfile = open(TRANSLATION_FILE_PATH,"r")
    translations = translationsfile.read()
    translationsfile.close()
except:
    translations = ""

print "Translations file path "+TRANSLATION_FILE_PATH


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

    # platform.system().lower() es "linux", "sunos", "darwin", "windows"
    import platform
    python_platform_name = platform.system().lower()

    platform = "unknown"
    if python_platform_name=="linux":
        platform = "linux"
    elif python_platform_name=="darwin":
        platform = "osx"
    elif python_platform_name=="windows":
        platform = "windows"

    return platform

def open_settings():
    return None

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
	    try:
	        if name in overrides:
	            dev = overrides[name]
	            #print "Overrides: ",name,"=",dev
	        #elif name=="debug":
	        #    return "true"
	        else:
	            dev=configfile.get("General",name)
	            #print "Config file: ",name,"=",dev
	        #print "get_setting",name,dev
	        return dev
	    except:
	        #print "get_setting",name,"(vacío)"
	        return ""
    
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
    	#print "set_setting",name,value
	    if isinstance(value, bool):
	        if value:
	            value = "true"
	        else:
	            value = "false"
	    elif isinstance(value, (int, long)):
	        value = str(value)
    	overrides[name]=value

def get_localized_string(code):
    cadenas = re.findall('<string id="%d">([^<]+)<' % code,translations)
    if len(cadenas)>0:
        return cadenas[0]
    else:
        return "%d" % code

def get_library_path():
    return None

def get_temp_file(filename):
    return os.path.join(get_data_path(),filename)

def get_data_path():
    data_path = os.path.join( os.path.expanduser("~") , ".pelisalacarta-cli" )
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    return data_path

def get_runtime_path():
    # Como config.py está en el directorio core, el directorio padre es el runtime_path
    # (al menos en la versión command_line que puede ser llamada desde cualquier sitio)
    return os.path.join( os.path.dirname(__file__) , ".." )

def get_cookie_data():
    import os
    ficherocookies = os.path.join( get_data_path(), 'cookies.dat' )

    cookiedatafile = open(ficherocookies,'r')
    cookiedata = cookiedatafile.read()
    cookiedatafile.close();

    return cookiedata

print "get_data_path="+get_data_path()
print "get_runtime_path="+get_runtime_path()

# TODO: Esto debería estar en otro sitio...

# Test if all the required directories are created
def verify_directories_created():
    import logger
    import os
    logger.info()

    # Force download path if empty
    download_path = get_setting("downloadpath")
    if download_path=="":
        download_path = os.path.join( get_data_path() , "downloads")
        set_setting("downloadpath" , download_path)

    # Force download list path if empty
    download_list_path = get_setting("downloadlistpath")
    if download_list_path=="":
        download_list_path = os.path.join( get_data_path() , "downloads" , "list")
        set_setting("downloadlistpath" , download_list_path)

    # Force bookmark path if empty
    bookmark_path = get_setting("bookmarkpath")
    if bookmark_path=="":
        bookmark_path = os.path.join( get_data_path() , "bookmarks")
        set_setting("bookmarkpath" , bookmark_path)

    # Create data_path if not exists
    if not os.path.exists(get_data_path()):
        logger.debug("Creating data_path "+get_data_path())
        try:
            os.mkdir(get_data_path())
        except:
            pass

    # Create download_path if not exists
    if not download_path.lower().startswith("smb") and not os.path.exists(download_path):
        logger.debug("Creating download_path "+download_path)
        try:
            os.mkdir(download_path)
        except:
            pass

    # Create download_list_path if not exists
    if not download_list_path.lower().startswith("smb") and not os.path.exists(download_list_path):
        logger.debug("Creating download_list_path "+download_list_path)
        try:
            os.mkdir(download_list_path)
        except:
            pass

    # Create bookmark_path if not exists
    if not bookmark_path.lower().startswith("smb") and not os.path.exists(bookmark_path):
        logger.debug("Creating bookmark_path "+bookmark_path)
        try:
            os.mkdir(bookmark_path)
        except:
            pass

    # Create library_path if not exists
    if not get_library_path().lower().startswith("smb") and not os.path.exists(get_library_path()):
        logger.debug("Creating library_path "+get_library_path())
        try:
            os.mkdir(get_library_path())
        except:
            pass

    # Checks that a directory "xbmc" is not present on platformcode
    old_xbmc_directory = os.path.join( get_runtime_path() , "platformcode" , "xbmc" )
    if os.path.exists( old_xbmc_directory ):
        logger.debug("Removing old platformcode.xbmc directory")
        try:
            import shutil
            shutil.rmtree(old_xbmc_directory)
        except:
            pass
