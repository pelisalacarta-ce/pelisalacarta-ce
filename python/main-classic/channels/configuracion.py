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
# Configuracion
# ------------------------------------------------------------

import os

from core import config
from core import filetools
from core import logger
from core.item import Item
from core import servertools
from platformcode import platformtools

CHANNELNAME = "configuracion"


def mainlist(item):
    logger.info()

    itemlist = list()
    itemlist.append(Item(channel=CHANNELNAME, title="Preferencias", action="settings", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    if config.get_setting("plugin_updates_available") == 0:
        nuevas = ""
    elif config.get_setting("plugin_updates_available") == 1:
        nuevas = " (1 nueva)"
    else:
        nuevas = " (%s nuevas)" % config.get_setting("plugin_updates_available")

    thumb_configuracion = "thumb_configuracion_%s.png" % config.get_setting("plugin_updates_available")

    itemlist.append(Item(channel=CHANNELNAME, title="Descargar e instalar otras versiones" + nuevas,
                         action="get_all_versions", folder=True,
                         thumbnail=get_thumbnail_path(thumb_configuracion)))

    itemlist.append(Item(channel=CHANNELNAME, title="", action="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    itemlist.append(Item(channel=CHANNELNAME, title="Ajustes especiales", action="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="   Ajustes de Canales", action="menu_channels",
                         folder=True, thumbnail=get_thumbnail_path("thumb_canales.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="   Ajustes de Servidores", action="menu_servers",
                         folder=True, thumbnail=get_thumbnail_path("thumb_canales.png")))
    itemlist.append(Item(channel="novedades", title="   Ajustes de la sección 'Novedades'", action="menu_opciones",
                         folder=True, thumbnail=get_thumbnail_path("thumb_novedades.png")))
    itemlist.append(Item(channel="buscador", title="   Ajustes del buscador global", action="opciones", folder=True,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="   Ajustes de descargas", action="channel_config",
                         config="descargas", folder=True, thumbnail=get_thumbnail_path("thumb_descargas.png")))

    if config.get_library_support():
        itemlist.append(Item(channel="biblioteca", title="   Ajustes de la biblioteca",
                             action="channel_config", folder=True,
                             thumbnail=get_thumbnail_path("thumb_biblioteca.png")))

    itemlist.append(Item(channel=CHANNELNAME, title="   Añadir o Actualizar canal/conector desde una URL",
                         action="menu_addchannels"))
    itemlist.append(Item(channel=CHANNELNAME, action="", title="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="Otras herramientas", action="submenu_tools",
                         folder=True, thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))
    

    return itemlist



def menu_channels(item):
    logger.info()
    itemlist = list()

    itemlist.append(Item(channel=CHANNELNAME, title="Activar/desactivar canales",
                         action="conf_tools", folder=False, extra="channels_onoff",
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    itemlist.append(Item(channel=CHANNELNAME, title="Ajustes por canales",
                         action="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    # Inicio - Canales configurables
    import channelselector
    from core import channeltools

    channel_list = channelselector.filterchannels("all")

    for channel in channel_list:
        channel_parameters = channeltools.get_channel_parameters(channel.channel)

        if channel_parameters["has_settings"]:
            itemlist.append(Item(channel=CHANNELNAME, title="   Configuración del canal '%s'" % channel.title,
                                 action="channel_config", config=channel.channel, folder=False,
                                 thumbnail=channel.thumbnail))
    # Fin - Canales configurables

    itemlist.append(Item(channel=CHANNELNAME, action="", title="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    itemlist.append(Item(channel=CHANNELNAME, title="Herramientas de canales", action="",
                         folder=False, thumbnail=get_thumbnail_path("thumb_canales.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="   Comprobar archivos *_data.json",
                         action="conf_tools", folder=True, extra="lib_check_datajson",
                         thumbnail=get_thumbnail_path("thumb_canales.png")))

    

    return itemlist


def channel_config(item):
    return platformtools.show_channel_settings(channelpath=filetools.join(config.get_runtime_path(), "channels",
                                                                          item.config))

def menu_servers(item):
    logger.info()
    itemlist = list()

    itemlist.append(Item(channel=CHANNELNAME, title="Sevidores bloqueados",
                         action="servers_blacklist", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))
                         
    itemlist.append(Item(channel=CHANNELNAME, title="Servidores favoritos",
                         action="servers_favorites", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))
    
    itemlist.append(Item(channel=CHANNELNAME, title="Ajustes de debriders:",
                         action="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    
    # Inicio - Servidores configurables

    server_list = servertools.get_debriders_list().keys()
    for server in server_list:
        server_parameters = servertools.get_server_parameters(server)
        if server_parameters["has_settings"]:
            itemlist.append(Item(channel=CHANNELNAME, title="   Configuración del servidor '%s'" % server_parameters["name"],
                                 action="server_config", config=server, folder=False,
                                 thumbnail=""))
                                 
    itemlist.append(Item(channel=CHANNELNAME, title="Ajustes de servidores",
                         action="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    server_list = servertools.get_servers_list().keys()

    for server in sorted(server_list):
        server_parameters = servertools.get_server_parameters(server)
        logger.info(server_parameters)
        if server_parameters["has_settings"] and filter(lambda x: x["id"] not in ["black_list", "white_list"], server_parameters["settings"]):
            itemlist.append(Item(channel=CHANNELNAME, title="   Configuración del servidor '%s'" % server_parameters["name"],
                                 action="server_config", config=server, folder=False,
                                 thumbnail=""))
                                 
    # Fin - Servidores configurables

    return itemlist
    
                                                                          
def server_config(item):
    return platformtools.show_channel_settings(channelpath=filetools.join(config.get_runtime_path(), "servers",
                                                                          item.config))


def servers_blacklist(item):
    server_list = servertools.get_servers_list()
    dict_values = {}

    list_controls = [{'id': 'filter_servers',
                      'type': "bool",
                      'label': "@30068",
                      'default': False,
                      'enabled': True,
                      'visible': True}]
    dict_values['filter_servers'] = config.get_setting('filter_servers')

    for i, server in enumerate(sorted(server_list.keys())):
        server_parameters = server_list[server]
        controls, defaults = servertools.get_server_controls_settings(server)
        dict_values[server] = config.get_setting("black_list",server=server)
        
        control = {'id': server,
                   'type': "bool",
                   'label': '    %s' % server_parameters["name"],
                   'default': defaults.get("black_list", False),
                   'enabled': "eq(-%s,True)" % (i + 1),
                   'visible': True}
        list_controls.append(control)


    return platformtools.show_channel_settings(list_controls=list_controls, dict_values=dict_values,
                                               caption="Servidores bloqueados",
                                               callback="cb_servers_blacklist")


def cb_servers_blacklist(item, dict_values):
    f = False
    progreso = platformtools.dialog_progress("Guardando configuración...", "Espere un momento por favor.")
    n = len(dict_values)
    i = 1
    for k,v in dict_values.items():
        if k == 'filter_servers':
            config.set_setting('filter_servers', v)
        else:
            config.set_setting("black_list", v,server=k)
            if v: # Si el servidor esta en la lista negra no puede estar en la de favoritos
                config.set_setting("favorites_servers_list", 100, server=k)
                f = True
                progreso.update((i * 100) / n, "Guardando configuración...%s" % k)
        i += 1

    if not f: # Si no hay ningun servidor en la lista, desactivarla
        config.set_setting('filter_servers', False)

    progreso.close()

def servers_favorites(item):
    server_list = servertools.get_servers_list()
    dict_values = {}

    list_controls = [{'id': 'favorites_servers',
                      'type': "bool",
                      'label': "Ordenar servidores",
                      'default': False,
                      'enabled': True,
                      'visible': True}]
    dict_values['favorites_servers'] = config.get_setting('favorites_servers')

    server_names = ['Ninguno']

    for server in sorted(server_list.keys()):
        if config.get_setting("black_list", server=server):
            continue

        server_names.append(server_list[server]['name'])

        orden = config.get_setting("favorites_servers_list", server=server)

        if orden > 0:
            dict_values[orden] = len(server_names) - 1


    for x in range(1, 6):
        control = {'id': x,
                   'type': "list",
                   'label': "    Servidor #%s" % (x),
                   'lvalues': server_names,
                   'default': 0,
                   'enabled': "eq(-%s,True)" % x,
                   'visible': True}
        list_controls.append(control)


    return platformtools.show_channel_settings(list_controls=list_controls, dict_values=dict_values,
                                           item=server_names,
                                           caption="Servidores favoritos",
                                           callback="cb_servers_favorites")


def cb_servers_favorites(server_names, dict_values):
    dict_name = {}
    progreso = platformtools.dialog_progress("Guardando configuración...", "Espere un momento por favor.")

    for i, v in dict_values.items():
        if i == "favorites_servers":
            config.set_setting("favorites_servers", v)
        elif int(v) > 0:
            dict_name[server_names[v]] = int(i)

    servers_list = servertools.get_servers_list().items()
    n = len(servers_list)
    i = 1
    for server, server_parameters in servers_list:
        if server_parameters['name'] in dict_name.keys():
            config.set_setting("favorites_servers_list", dict_name[server_parameters['name']], server=server)
        else:
            config.set_setting("favorites_servers_list", 0, server=server)
        progreso.update((i * 100) / n, "Guardando configuración...%s" % server_parameters['name'])
        i += 1

    if not dict_name: #Si no hay ningun servidor en lalista desactivarla
        config.set_setting("favorites_servers", False)

    progreso.close()


def get_all_versions(item):
    logger.info()

    itemlist = []

    return itemlist


def settings(item):
    config.open_settings()


def menu_addchannels(item):
    logger.info()
    itemlist = list()
    itemlist.append(Item(channel=CHANNELNAME, title="# Copia de seguridad automática en caso de sobrescritura",
                         action="", text_color="green"))
    itemlist.append(Item(channel=CHANNELNAME, title="Añadir o actualizar canal", action="addchannel", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Añadir o actualizar conector", action="addchannel", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Mostrar ruta de carpeta para copias de seguridad",
                         action="backups", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Eliminar copias de seguridad guardadas", action="backups",
                         folder=False))

    return itemlist


def addchannel(item):
    import os
    import time
    logger.info()

    tecleado = platformtools.dialog_input("", "Introduzca la URL")
    if not tecleado:
        return
    logger.info("url=%s" % tecleado)

    local_folder = config.get_runtime_path()
    if "canal" in item.title:
        local_folder = filetools.join(local_folder, 'channels')
        folder_to_extract = "channels"
        info_accion = "canal"
    else:
        local_folder = filetools.join(local_folder, 'servers')
        folder_to_extract = "servers"
        info_accion = "conector"

    # Detecta si es un enlace a un .py o .xml (pensado sobre todo para enlaces de github)
    try:
        extension = tecleado.rsplit(".", 1)[1]
    except:
        extension = ""

    files = []
    zip = False
    if extension == "py" or extension == "xml":
        filename = tecleado.rsplit("/", 1)[1]
        localfilename = filetools.join(local_folder, filename)
        files.append([tecleado, localfilename, filename])
    else:
        import re
        from core import scrapertools
        # Comprueba si la url apunta a una carpeta completa (channels o servers) de github
        if re.search(r'https://github.com/[^\s]+/'+folder_to_extract, tecleado):
            try:
                data = scrapertools.downloadpage(tecleado)
                matches = scrapertools.find_multiple_matches(data,
                                                             '<td class="content">.*?href="([^"]+)".*?title="([^"]+)"')
                for url, filename in matches:
                    url = "https://raw.githubusercontent.com" + url.replace("/blob/", "/")
                    localfilename = filetools.join(local_folder, filename)
                    files.append([url, localfilename, filename])
            except:
                import traceback
                logger.error("Detalle del error: %s" % traceback.format_exc())
                platformtools.dialog_ok("Error", "La url no es correcta o no está disponible")
                return
        else:
            filename = 'new%s.zip' % info_accion
            localfilename = filetools.join(config.get_data_path(), filename)
            files.append([tecleado, localfilename, filename])
            zip = True

    logger.info("localfilename=%s" % localfilename)
    logger.info("descarga fichero...")

    try:
        if len(files) > 1:
            lista_opciones = ["No", "Sí", "Sí (Sobrescribir todos)"]
            overwrite_all = False
        from core import downloadtools
        for url, localfilename, filename in files:
            result = downloadtools.downloadfile(url, localfilename, continuar=False, resumir=False)
            if result == -3:
                if len(files) == 1:
                    dyesno = platformtools.dialog_yesno("El archivo ya existe", "Ya existe el %s %s. "
                                                                                "¿Desea sobrescribirlo?" %
                                                        (info_accion, filename))
                else:
                    if not overwrite_all:
                        dyesno = platformtools.dialog_select("El archivo %s ya existe, ¿desea sobrescribirlo?"
                                                             % filename, lista_opciones)
                    else:
                        dyesno = 1
                # Diálogo cancelado
                if dyesno == -1:
                    return
                # Caso de carpeta github, opción sobrescribir todos
                elif dyesno == 2:
                    overwrite_all = True
                elif dyesno:
                    hora_folder = "Copia seguridad [%s]" % time.strftime("%d-%m_%H-%M", time.localtime())
                    backup = filetools.join(config.get_data_path(), 'backups', hora_folder, folder_to_extract)
                    if not filetools.exists(backup):
                        os.makedirs(backup)
                    import shutil
                    shutil.copy2(localfilename, filetools.join(backup, filename))
                    downloadtools.downloadfile(url, localfilename, continuar=True, resumir=False)
                else:
                    if len(files) == 1:
                        return
                    else:
                        continue
    except:
        import traceback
        logger.error("Detalle del error: %s" % traceback.format_exc())
        return

    if zip:
        try:
            # Lo descomprime
            logger.info("descomprime fichero...")
            from core import ziptools
            unzipper = ziptools.ziptools()
            logger.info("destpathname=%s" % local_folder)
            unzipper.extract(localfilename, local_folder, folder_to_extract, True, True)
        except:
            import traceback
            logger.error("Detalle del error: %s" % traceback.format_exc())
            # Borra el zip descargado
            filetools.remove(localfilename)
            platformtools.dialog_ok("Error", "Se ha producido un error extrayendo el archivo")
            return

        # Borra el zip descargado
        logger.info("borra fichero...")
        filetools.remove(localfilename)
        logger.info("...fichero borrado")

    platformtools.dialog_ok("Éxito", "Actualización/Instalación realizada correctamente")


def backups(item):
    logger.info()

    ruta = filetools.join(config.get_data_path(), 'backups')
    ruta_split = ""
    if "ruta" in item.title:
        heading = "Ruta de copias de seguridad"
        if not filetools.exists(ruta):
            folders = "Carpeta no creada"
        else:
            folders = str(len(filetools.listdir(ruta))) + " copia/s de seguridad guardadas"
        if len(ruta) > 55:
            ruta_split = ruta[55:]
            ruta = ruta[:55]
        platformtools.dialog_ok(heading, ruta, ruta_split, folders)
    else:
        if not filetools.exists(ruta):
            platformtools.dialog_ok("La carpeta no existe", "No hay copias de seguridad guardadas")
        else:
            dyesno = platformtools.dialog_yesno("Las copias de seguridad se eliminarán", "¿Está seguro?")
            if dyesno:
                import shutil
                shutil.rmtree(ruta, ignore_errors=True)


def get_thumbnail_path(thumb_name):
    import urlparse
    web_path = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/squares/"
    return urlparse.urljoin(web_path, thumb_name)


def submenu_tools(item):
    logger.info()
    itemlist = []

    itemlist.append(Item(channel=CHANNELNAME, title="Herramientas de canales", action="",
                         folder=False, thumbnail=get_thumbnail_path("thumb_canales.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="   Comprobar archivos *_data.json",
                         action="conf_tools", folder=True, extra="lib_check_datajson",
                         thumbnail=get_thumbnail_path("thumb_canales.png")))

    if config.get_library_support():
        itemlist.append(Item(channel=CHANNELNAME, action="", title="", folder=False,
                             thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))
        itemlist.append(Item(channel=CHANNELNAME, title="Herramientas de biblioteca", action="",
                             folder=False, thumbnail=get_thumbnail_path("thumb_biblioteca.png")))
        itemlist.append(Item(channel=CHANNELNAME, action="overwrite_tools", folder=False,
                             thumbnail=get_thumbnail_path("thumb_biblioteca.png"),
                             title="   Sobreescribir toda la biblioteca (strm, nfo y json)"))
        itemlist.append(Item(channel="biblioteca", action="update_biblio", folder=False,
                             thumbnail=get_thumbnail_path("thumb_biblioteca.png"),
                             title="   Buscar nuevos episodios y actualizar biblioteca"))

    return itemlist


def conf_tools(item):
    logger.info()

    # Activar o desactivar canales
    if item.extra == "channels_onoff":
        import channelselector
        from core import channeltools

        channel_list = channelselector.filterchannels("allchannelstatus")

        excluded_channels = ['tengourl',
                             'buscador',
                             'biblioteca',
                             'configuracion',
                             'novedades',
                             'personal',
                             'ayuda',
                             'descargas']

        list_controls = []
        try:
            list_controls.append({'id': "all_channels",
                                  'type': "list",
                                  'label': "Todos los canales",
                                  'default': 0,
                                  'enabled': True,
                                  'visible': True,
                                  'lvalues': ['',
                                              'Activar todos',
                                              'Desactivar todos',
                                              'Establecer estado por defecto']})

            for channel in channel_list:
                # Si el canal esta en la lista de exclusiones lo saltamos
                if channel.channel not in excluded_channels:

                    channel_parameters = channeltools.get_channel_parameters(channel.channel)

                    status_control = ""
                    status = config.get_setting("enabled", channel.channel)
                    # si status no existe es que NO HAY valor en _data.json
                    if status is None:
                        status = channel_parameters["active"]
                        logger.debug("%s | Status (XML): %s" % (channel.channel, status))
                        if not status:
                            status_control = " [COLOR grey](Desactivado por defecto)[/COLOR]"
                    else:
                        logger.debug("%s  | Status: %s" % (channel.channel, status))

                    control = {'id': channel.channel,
                               'type': "bool",
                               'label': channel_parameters["title"] + status_control,
                               'default': status,
                               'enabled': True,
                               'visible': True}
                    list_controls.append(control)

                else:
                    continue

        except:
            import traceback
            logger.error("Error: %s" % traceback.format_exc())
        else:
            return platformtools.show_channel_settings(list_controls=list_controls,
                                                       item=item.clone(channel_list=channel_list),
                                                       caption="Canales",
                                                       callback="channel_status",
                                                       custom_button={"visible": False})

    # Comprobacion de archivos channel_data.json
    elif item.extra == "lib_check_datajson":
        itemlist = []
        import channelselector
        from core import channeltools
        channel_list = channelselector.filterchannels("allchannelstatus")

        # Tener una lista de exclusion no tiene mucho sentido por que se comprueba si
        # el xml tiene "settings", pero por si acaso se deja
        excluded_channels = ['tengourl',
                             'configuracion',
                             'personal',
                             'ayuda']

        try:
            import os
            from core import jsontools
            for channel in channel_list:

                list_status = None
                default_settings = None

                # Se comprueba si el canal esta en la lista de exclusiones
                if channel.channel not in excluded_channels:
                    # Se comprueba que tenga "settings", sino se salta
                    jsonchannel = channeltools.get_channel_json(channel.channel)
                    if not jsonchannel.get("settings"):
                        itemlist.append(Item(channel=CHANNELNAME,
                                             title=channel.title + " - No tiene ajustes por defecto",
                                             action="", folder=False,
                                             thumbnail=channel.thumbnail))
                        continue
                        # logger.info(channel.channel + " SALTADO!")

                    # Se cargan los ajustes del archivo json del canal
                    file_settings = os.path.join(config.get_data_path(), "settings_channels",
                                                 channel.channel + "_data.json")
                    dict_settings = {}
                    dict_file = {}
                    if filetools.exists(file_settings):
                        # logger.info(channel.channel + " Tiene archivo _data.json")
                        channeljson_exists = True
                        # Obtenemos configuracion guardada de ../settings/channel_data.json
                        try:
                            dict_file = jsontools.load_json(open(file_settings, "rb").read())
                            if isinstance(dict_file, dict) and 'settings' in dict_file:
                                dict_settings = dict_file['settings']
                        except EnvironmentError:
                            logger.error("ERROR al leer el archivo: %s" % file_settings)
                    else:
                        # logger.info(channel.channel + " No tiene archivo _data.json")
                        channeljson_exists = False

                    if channeljson_exists == True:
                        try:
                            datajson_size = filetools.getsize(file_settings)
                        except:
                            import traceback
                            logger.error(channel.title + " | Detalle del error: %s" % traceback.format_exc())
                    else:
                        datajson_size = None

                    # Si el _data.json esta vacio o no existe...
                    if (len(dict_settings) and datajson_size) == 0 or channeljson_exists == False:
                        # Obtenemos controles del archivo ../channels/channel.xml
                        needsfix = True
                        try:
                            # Se cargan los ajustes por defecto
                            list_controls, default_settings = channeltools.get_channel_controls_settings(channel.channel)
                            # logger.info(channel.title + " | Default: %s" % default_settings)
                        except:
                            import traceback
                            logger.error(channel.title + " | Detalle del error: %s" % traceback.format_exc())
                            # default_settings = {}

                        # Si _data.json necesita ser reparado o no existe...
                        if needsfix == True or channeljson_exists == False:
                            if default_settings is not None:
                                # Creamos el channel_data.json
                                default_settings.update(dict_settings)
                                dict_settings = default_settings
                                dict_file['settings'] = dict_settings
                                # Creamos el archivo ../settings/channel_data.json
                                json_data = jsontools.dump_json(dict_file)
                                try:
                                    open(file_settings, "wb").write(json_data)
                                    # logger.info(channel.channel + " - Archivo _data.json GUARDADO!")
                                    # El channel_data.json se ha creado/modificado
                                    list_status = " - [COLOR red] CORREGIDO!![/COLOR]"
                                except EnvironmentError:
                                    logger.error("ERROR al salvar el archivo: %s" % file_settings)
                            else:
                                if default_settings is None:
                                    list_status = " - [COLOR red] Imposible cargar los ajustes por defecto![/COLOR]"

                    else:
                        # logger.info(channel.channel + " - NO necesita correccion!")
                        needsfix = False

                    # Si se ha establecido el estado del canal se añade a la lista
                    if needsfix is not None:
                        if needsfix == True:
                            if channeljson_exists == False:
                                list_status = " - Ajustes creados"
                                list_colour = "red"
                            else:
                                list_status = " - No necesita corrección"
                                list_colour = "green"
                        else:
                            # Si "needsfix" es "false" y "datjson_size" es None habra
                            # ocurrido algun error
                            if datajson_size is None:
                                list_status = " - Ha ocurrido algun error"
                                list_colour = "red"
                            else:
                                list_status = " - No necesita corrección"
                                list_colour = "green"

                    if list_status is not None:
                        itemlist.append(Item(channel=CHANNELNAME,
                                             title=channel.title + list_status,
                                             action="", folder=False,
                                             thumbnail=channel.thumbnail,
                                             text_color=list_colour))
                    else:
                        logger.error("Algo va mal con el canal %s" % channel.channel)

                # Si el canal esta en la lista de exclusiones lo saltamos
                else:
                    continue
        except:
            import traceback
            logger.error("Error: %s" % traceback.format_exc())

        return itemlist


def channel_status(item, dict_values):

    try:
        for k in dict_values:

            if k == "all_channels":
                logger.info("Todos los canales | Estado seleccionado: %s" % dict_values[k])
                if dict_values[k] != 0:
                    excluded_channels = ['tengourl', 'buscador',
                                         'biblioteca', 'configuracion',
                                         'novedades', 'personal',
                                         'ayuda', 'descargas']

                    for channel in item.channel_list:
                        if channel.channel not in excluded_channels:
                            from core import channeltools
                            channel_parameters = channeltools.get_channel_parameters(channel.channel)
                            new_status_all = None
                            new_status_all_default = channel_parameters["active"]

                            # Opcion Activar todos
                            if dict_values[k] == 1:
                                new_status_all = True

                            # Opcion Desactivar todos
                            if dict_values[k] == 2:
                                new_status_all = False

                            # Opcion Recuperar estado por defecto
                            if dict_values[k] == 3:
                                # Si tiene "enabled" en el json es porque el estado no es el del xml
                                if config.get_setting("enabled", channel.channel):
                                    new_status_all = new_status_all_default

                                # Si el canal no tiene "enabled" en el json no se guarda, se pasa al siguiente
                                else:
                                    continue

                            # Se guarda el estado del canal
                            if new_status_all is not None:
                                config.set_setting("enabled", new_status_all, channel.channel)
                    break
                else:
                    continue

            else:
                logger.info("Canal: %s | Estado: %s" % (k, dict_values[k]))
                config.set_setting("enabled", dict_values[k], k)
                logger.info("el valor esta como %s " % config.get_setting("enabled", k))

        platformtools.itemlist_update(Item(channel=CHANNELNAME, action="mainlist"))

    except:
        import traceback
        logger.error("Detalle del error: %s" % traceback.format_exc())
        platformtools.dialog_notification("Error", "Se ha producido un error al guardar")


def overwrite_tools(item):
    import library_service
    from core import library

    seleccion = platformtools.dialog_yesno("Sobrescribir toda la biblioteca",
                                           "Esto puede llevar algun tiempo.",
                                           "¿Desea continuar?")
    if seleccion == 1:
        heading = 'Sobrescribiendo biblioteca....'
        p_dialog = platformtools.dialog_progress_bg('pelisalacarta', heading)
        p_dialog.update(0, '')

        import glob
        show_list = glob.glob(filetools.join(library.TVSHOWS_PATH, u'/*/tvshow.nfo'))

        if show_list:
            t = float(100) / len(show_list)

        for i, tvshow_file in enumerate(show_list):
            head_nfo, serie = library.read_nfo(tvshow_file)
            path = filetools.dirname(tvshow_file)

            if not serie.active:
                # si la serie no esta activa descartar
                continue

            # Eliminamos la carpeta con la serie ...
            filetools.rmdirtree(path)

            # ... y la volvemos a añadir
            library_service.update(path, p_dialog, i, t, serie, 3)

        p_dialog.close()
