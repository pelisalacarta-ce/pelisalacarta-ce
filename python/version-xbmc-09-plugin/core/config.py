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
# Parámetros de configuración (XBMC)
# ------------------------------------------------------------

import os
import sys
import xbmc
import xbmcplugin

PLATFORM_NAME = "xbmc-plugin"
PLUGIN_NAME = "pelisalacarta"

def get_platform(full_version=False):
    #full_version solo es util en xbmc/kodi
    ret = {
        'num_version': 9.0 ,
        'name_version': PLATFORM_NAME ,
        'video_db': "",
        'plaform': PLATFORM_NAME
        }

    if full_version:
        return ret
    else:
        return PLATFORM_NAME


def is_xbmc():
    return True


def get_library_support():
    return True


def get_system_platform():
    """ fonction: pour recuperer la platform que xbmc tourne """
    platform = "unknown"
    if xbmc.getCondVisibility("system.platform.linux"):
        platform = "linux"
    elif xbmc.getCondVisibility("system.platform.xbox"):
        platform = "xbox"
    elif xbmc.getCondVisibility("system.platform.windows"):
        platform = "windows"
    elif xbmc.getCondVisibility("system.platform.osx"):
        platform = "osx"
    return platform


def open_settings():
    xbmcplugin.openSettings(sys.argv[0])


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
        value = xbmcplugin.getSetting(channel + name)
        # Translate Path if start with "special://"
        if value.startswith("special://") and "librarypath" not in name:
            value = xbmc.translatePath(value)

        # logger.info("config.get_setting -> '"+value+"'")

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

            xbmcplugin.setSetting(name, value)
        except:
            return None

        return value


def get_localized_string(code):
    dev = xbmc.getLocalizedString(code)

    try:
        dev = dev.encode("utf-8")
    except:
        pass

    return dev


def get_library_config_path():
    value = get_setting("librarypath")
    if value == "":
        verify_directories_created()
        value = get_setting("librarypath")
    return value

def get_library_path():
    return xbmc.translatePath(get_library_config_path())


def get_temp_file(filename):
    return xbmc.translatePath(os.path.join("special://temp/", filename))


def get_runtime_path():
    return os.getcwd()


def get_data_path():
    dev = xbmc.translatePath("special://profile/plugin_data/video/pelisalacarta")

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
                    ["settings_path",    "settings_channels"]]

    for path, default in config_paths:
        saved_path = get_setting(path)
        if not saved_path:
            saved_path = "special://profile/plugin_data/video/pelisalacarta/" + default
            set_setting(path, saved_path)

        saved_path = xbmc.translatePath(saved_path)
        if not filetools.exists(saved_path):
            logger.debug("Creating %s: %s" % (path, saved_path))
            filetools.mkdir(saved_path)

        # Biblioteca
        if path == "librarypath":
            set_setting("library_version", "v4")
