# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración - xbmc
#------------------------------------------------------------
# tvalacarta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Historial de cambios:
#------------------------------------------------------------

TAG_VERSION = "10.25"
TAG_VERSION_XBMC = "4.2 beta 1"
PLATFORM_NAME = "boxee"

print "[config.py] boxee config "+TAG_VERSION+" ("+TAG_VERSION_XBMC+")"

import os,re
import xbmc
import mc

PLUGIN_NAME = "pelisalacarta"

def get_platform(full_version=False):
    #full_version solo es util en xbmc/kodi
    ret = {
        'num_version': float(TAG_VERSION) ,
        'name_version': PLATFORM_NAME ,
        'video_db': "",
        'plaform': PLATFORM_NAME
        }

    if full_version:
        return ret
    else:
        return PLATFORM_NAME

def get_version():
    return TAG_VERSION

def get_system_platform():
    return "boxee"

def is_xbmc():
    return False

def get_library_support():
    return True

def open_settings():
    import xbmcplugin
    import sys
    xbmcplugin.openSettings( sys.argv[ 0 ] )

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

        # xbmc.log("config.get_setting reading channel setting '"+name+"' from channel xml")
        from core import channeltools
        value = channeltools.get_channel_setting(name, channel)
        # xbmc.log.info("config.get_setting -> '"+repr(value)+"'")

        return value
            
    elif server:
        # xbmc.log("config.get_setting reading server setting '"+name+"' from server xml")
        from core import servertools
        value = servertools.get_server_setting(name, server)
        # xbmc.log("config.get_setting -> '"+repr(value)+"'")

        return value

    # Global setting
    else:
        #xbmc.log("config.get_setting reading main setting '"+name+"'")
        import xbmcplugin
        value = xbmcplugin.getSetting(name)
        #xbmc.log("config.get_setting -> '"+value+"'")

        # hack para devolver el tipo correspondiente
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            try:
                value = int(value)
            except ValueError:
                pass

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
            if isinstance(value, bool):
                if value:
                    value = "true"
                else:
                    value = "false"
            elif isinstance(value, (int, long)):
                value = str(value)

            import xbmcplugin
            xbmcplugin.setSetting(name, value)
        except:
            return None

        return value

def get_localized_string(code):
    cadenas = re.findall('<string id="%d">([^<]+)<' % code,translations)
    if len(cadenas)>0:
        return cadenas[0]
    else:
        return "%d" % code
    
def get_library_path():
    #return os.path.join( get_data_path(), 'library' )
    default = os.path.join( get_data_path(), 'library' )

    value = get_setting("librarypath")
    if value=="":
        value=default
    return value

def get_temp_file(filename):
    return os.path.join( mc.GetTempDir(), filename )

def get_runtime_path():
    app = mc.GetApp();
    return app.GetAppDir()

def get_data_path():
    return os.getcwd()

def get_boxee_plugin_path():
    return os.path.abspath(os.path.join(get_runtime_path(),"..","..","plugins","video","info.mimediacenter."+PLUGIN_NAME))

# Test if all the required directories are created
def verify_directories_created():
    import logger
    #xbmc.log("pelisalacarta.core.config.verify_directories_created")

    # Force download path if empty
    download_path = get_setting("downloadpath")
    if download_path == "":
        if is_xbmc():
            download_path_special = "special://profile/addon_data/plugin.video." + PLUGIN_NAME + "/downloads"
            set_setting("downloadpath", download_path_special)
        else:
            download_path = os.path.join(get_data_path(), "downloads")
            set_setting("downloadpath", download_path)

    # Force download list path if empty
    download_list_path = get_setting("downloadlistpath")
    if download_list_path == "":
        if is_xbmc():
            download_list_path_special = "special://profile/addon_data/plugin.video." + PLUGIN_NAME + "/downloads/list"
            set_setting("downloadlistpath", download_list_path_special)
        else:
            download_list_path = os.path.join(get_data_path(), "downloads", "list")
            set_setting("downloadlistpath", download_list_path)

    # Force bookmark path if empty
    bookmark_path = get_setting("bookmarkpath")
    if bookmark_path == "":
        if is_xbmc():
            bookmark_path_special = "special://profile/addon_data/plugin.video." + PLUGIN_NAME + "/downloads/list"
            set_setting("bookmarkpath", bookmark_path_special)
        else:
            bookmark_path = os.path.join(get_data_path(), "bookmarks")
            set_setting("bookmarkpath", bookmark_path)

    # Create data_path if not exists
    if not os.path.exists(get_data_path()):
        logger.debug("Creating data_path " + get_data_path())
        try:
            os.mkdir(get_data_path())
        except:
            pass

    # Create download_path if not exists
    if not download_path.lower().startswith("smb") and not os.path.exists(download_path):
        logger.debug("Creating download_path " + download_path)
        try:
            os.mkdir(download_path)
        except:
            pass

    # Create download_list_path if not exists
    if not download_list_path.lower().startswith("smb") and not os.path.exists(download_list_path):
        logger.debug("Creating download_list_path " + download_list_path)
        try:
            os.mkdir(download_list_path)
        except:
            pass

    # Create bookmark_path if not exists
    if not bookmark_path.lower().startswith("smb") and not os.path.exists(bookmark_path):
        logger.debug("Creating bookmark_path " + bookmark_path)
        try:
            os.mkdir(bookmark_path)
        except:
            pass

    # Create library_path if not exists
    if not get_library_path().lower().startswith("smb") and not os.path.exists(get_library_path()):
        logger.debug("Creating library_path " + get_library_path())
        try:
            os.mkdir(get_library_path())
        except:
            pass

    # Create settings_path is not exists
    settings_path = os.path.join(get_data_path(), "settings_channels")
    if not os.path.exists(settings_path):
        logger.debug("Creating settings_path " + settings_path)
        try:
            os.mkdir(settings_path)
        except:
            pass

# Literales
TRANSLATION_FILE_PATH = os.path.join(get_runtime_path(),"resources","language","Spanish","strings.xml")
translationsfile = open(TRANSLATION_FILE_PATH,"r")
translations = translationsfile.read()
translationsfile.close()

print "[config.py] runtime path = "+get_runtime_path()
print "[config.py] data path = "+get_data_path()
print "[config.py] language file path "+TRANSLATION_FILE_PATH
print "[config.py] temp path = "+get_temp_file("test")
print "[config.py] plugin path = "+get_boxee_plugin_path()
print "[config.py] version = "+get_version()

# Si no existe la versión, borra el directorio de plugin/video/info.mimediacenter.tvalacarta (copia del apps/info.mimediacenter.tvalacarta)
if not os.path.exists( os.path.join(get_boxee_plugin_path(),get_version()) ):
    print "[config.py] borra el directorio "+get_boxee_plugin_path()
    import shutil
    try:
        shutil.rmtree(get_boxee_plugin_path())
    except:
        pass
    
# Clona el directorio de apps a plugin/video
if not os.path.exists( get_boxee_plugin_path() ):
    print "[config.py] clona el directorio de "+get_runtime_path()+" a "+get_boxee_plugin_path()
    import shutil
    shutil.copytree( get_runtime_path() , get_boxee_plugin_path() )
    
    # Crea el fichero de la versión para no volver a clonarlo más
    f = open( os.path.join(get_boxee_plugin_path(),get_version()), 'w')
    f.write("done")
    f.close()
