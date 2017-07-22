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

import glob
import os
import traceback
import urlparse

from core import channeltools
from core import config
from core import logger
from core.item import Item


def getmainlist(preferred_thumb=""):
    logger.info()
    itemlist = list()

    # Añade los canales que forman el menú principal

    itemlist.append(Item(title=config.get_localized_string(30130), channel="novedades", action="mainlist",
                         thumbnail=get_thumb(preferred_thumb, "thumb_novedades.png"),
                         category=config.get_localized_string(30119), viewmode="thumbnails",
                         context=[{"title": "Configurar novedades", "channel": "novedades", "action": "menu_opciones",
                                   "goto": True}]))

    itemlist.append(Item(title=config.get_localized_string(30118), channel="channelselector", action="getchanneltypes",
                         thumbnail=get_thumb(preferred_thumb, "thumb_canales.png"),
                         category=config.get_localized_string(30119), viewmode="thumbnails"))

    itemlist.append(Item(title=config.get_localized_string(30103), channel="buscador", action="mainlist",
                         thumbnail=get_thumb(preferred_thumb, "thumb_buscar.png"),
                         category=config.get_localized_string(30119), viewmode="list",
                         context=[{"title": "Configurar buscador", "channel": "buscador", "action": "opciones",
                                   "goto": True}]))

    itemlist.append(Item(title=config.get_localized_string(30102), channel="favoritos", action="mainlist",
                         thumbnail=get_thumb(preferred_thumb, "thumb_favoritos.png"),
                         category=config.get_localized_string(30102), viewmode="thumbnails"))

    if config.get_library_support():

        itemlist.append(Item(title=config.get_localized_string(30131), channel="biblioteca", action="mainlist",
                             thumbnail=get_thumb(preferred_thumb, "thumb_biblioteca.png"),
                             category=config.get_localized_string(30119), viewmode="thumbnails",
                             context=[{"title": "Configurar biblioteca", "channel": "biblioteca",
                                       "action": "channel_config"}]))

    itemlist.append(Item(title=config.get_localized_string(30101), channel="descargas", action="mainlist",
                         thumbnail=get_thumb(preferred_thumb, "thumb_descargas.png"), viewmode="list",
                         context=[{"title": "Configurar descargas", "channel": "configuracion", "config": "descargas",
                                   "action": "channel_config"}]))

    thumb_configuracion = "thumb_configuracion_%s.png" % config.get_setting("plugin_updates_available")

    itemlist.append(Item(title=config.get_localized_string(30100), channel="configuracion", action="mainlist",
                         thumbnail=get_thumb(preferred_thumb, thumb_configuracion),
                         category=config.get_localized_string(30100), viewmode="list"))

    itemlist.append(Item(title=config.get_localized_string(30104), channel="ayuda", action="mainlist",
                         thumbnail=get_thumb(preferred_thumb, "thumb_ayuda.png"),
                         category=config.get_localized_string(30104), viewmode="list"))
    return itemlist


def get_thumb(preferred_thumb, thumb_name):
    return urlparse.urljoin(get_thumbnail_path(preferred_thumb), thumb_name)


def getchanneltypes(preferred_thumb=""):
    logger.info()

    # Lista de categorias
    channel_types = ["movie", "serie", "anime", "documentary", "vos", "torrent", "latino"]
    dict_types_lang = {'movie': config.get_localized_string(30122), 'serie': config.get_localized_string(30123),
                       'anime': config.get_localized_string(30124), 'documentary': config.get_localized_string(30125),
                       'vos': config.get_localized_string(30136), 'adult': config.get_localized_string(30126),
                       'latino': config.get_localized_string(30127)}

    if config.get_setting("adult_mode") != 0:
        channel_types.append("adult")

    channel_language = config.get_setting("channel_language")
    logger.info("channel_language="+channel_language)

    # Ahora construye el itemlist ordenadamente
    itemlist = list()
    title = config.get_localized_string(30121)
    itemlist.append(Item(title=title, channel="channelselector", action="filterchannels",
                         category=title, channel_type="all",
                         thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb), "thumb_canales_todos.png"),
                         viewmode="thumbnails"))

    for channel_type in channel_types:
        logger.info("channel_type="+channel_type)
        title = dict_types_lang.get(channel_type, channel_type)
        itemlist.append(Item(title=title, channel="channelselector", action="filterchannels", category=title,
                             channel_type=channel_type, viewmode="thumbnails",
                             thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),
                                                        "thumb_canales_"+channel_type+".png")))

    return itemlist


def filterchannels(category, preferred_thumb=""):
    logger.info()

    channelslist = []

    # Si category = "allchannelstatus" es que estamos activando/desactivando canales
    appenddisabledchannels = False
    if category == "allchannelstatus":
        category = "all"
        appenddisabledchannels = True

    # Lee la lista de canales
    channel_path = os.path.join(config.get_runtime_path(), "channels", '*.xml')
    logger.info("channel_path="+channel_path)

    channel_files = glob.glob(channel_path)
    logger.info("channel_files encontrados "+str(len(channel_files)))

    channel_language = config.get_setting("channel_language")
    logger.info("channel_language="+channel_language)
    if channel_language == "":
        channel_language = "all"
        logger.info("channel_language="+channel_language)

    for channel in channel_files:
        logger.info("channel="+channel)

        try:
            channel_parameters = channeltools.get_channel_parameters(channel[:-4])

            # si el canal no es compatible, no se muestra
            if not channel_parameters["compatible"]:
                continue

            # Si no es un canal lo saltamos
            if not channel_parameters["channel"]:
                continue
            logger.info("channel_parameters="+repr(channel_parameters))

            # Si prefiere el bannermenu y el canal lo tiene, cambia ahora de idea
            if preferred_thumb == "bannermenu" and "bannermenu" in channel_parameters:
                channel_parameters["thumbnail"] = channel_parameters["bannermenu"]

            # si en el xml el canal está desactivado no se muestra el canal en la lista
            if not channel_parameters["active"]:
                continue

            # Se salta el canal si no está activo y no estamos activando/desactivando los canales
            channel_status = config.get_setting("enabled", channel_parameters["channel"])

            if channel_status is None:
                # si channel_status no existe es que NO HAY valor en _data.json.
                # como hemos llegado hasta aquí (el canal está activo en xml), se devuelve True
                channel_status = True

            # fix temporal para solucionar que enabled aparezca como "true/false"(str) y sea true/false(bool)
            # TODO borrar este fix en la versión > 4.2.1, ya que no sería necesario
            else:
                if isinstance(channel_status, basestring):
                    if channel_status == "true":
                        channel_status = True
                    else:
                        channel_status = False
                    config.set_setting("enabled", channel_status, channel_parameters["channel"])

            if channel_status != True:
                # si obtenemos el listado de canales desde "activar/desactivar canales", y el canal está desactivado
                # lo mostramos, si estamos listando todos los canales desde el listado general y está desactivado,
                # no se muestra
                if appenddisabledchannels != True:
                    continue

            # Se salta el canal para adultos si el modo adultos está desactivado
            if channel_parameters["adult"] == True and config.get_setting("adult_mode") == 0:
                continue

            # Se salta el canal si está en un idioma filtrado
            if channel_language != "all" \
                    and channel_parameters["language"] != config.get_setting("channel_language"):
                continue

            # Se salta el canal si está en una categoria filtrado
            if category != "all" and category not in channel_parameters["categories"]:
                continue

            # Si tiene configuración añadimos un item en el contexto
            context = []
            if channel_parameters["has_settings"]:
                context.append({"title": "Configurar canal", "channel": "configuracion", "action": "channel_config",
                                "config": channel_parameters["channel"]})

            # Si ha llegado hasta aquí, lo añade
            channelslist.append(Item(title=channel_parameters["title"], channel=channel_parameters["channel"],
                                     action="mainlist", thumbnail=channel_parameters["thumbnail"],
                                     fanart=channel_parameters["fanart"], category=channel_parameters["title"],
                                     language=channel_parameters["language"], viewmode="list",
                                     version=channel_parameters["version"], context=context))

        except:
            logger.error("Se ha producido un error al leer los datos del canal " + channel)
            import traceback
            logger.error(traceback.format_exc())

    channelslist.sort(key=lambda item: item.title.lower().strip())

    if category == "all":
        if config.get_setting("personalchannel5") == True:
            channelslist.insert(0, Item(title=config.get_setting("personalchannelname5"), action="mainlist",
                                        channel="personal5", thumbnail=config.get_setting("personalchannellogo5"),
                                        type="generic", viewmode="list"))
        if config.get_setting("personalchannel4") == True:
            channelslist.insert(0, Item(title=config.get_setting("personalchannelname4"), action="mainlist",
                                        channel="personal4", thumbnail=config.get_setting("personalchannellogo4"),
                                        type="generic", viewmode="list"))
        if config.get_setting("personalchannel3") == True:
            channelslist.insert(0, Item(title=config.get_setting("personalchannelname3"), action="mainlist",
                                        channel="personal3", thumbnail=config.get_setting("personalchannellogo3"),
                                        type="generic", viewmode="list"))
        if config.get_setting("personalchannel2") == True:
            channelslist.insert(0, Item(title=config.get_setting("personalchannelname2"), action="mainlist",
                                        channel="personal2", thumbnail=config.get_setting("personalchannellogo2"),
                                        type="generic", viewmode="list"))
        if config.get_setting("personalchannel") == True:
            channelslist.insert(0, Item(title=config.get_setting("personalchannelname"), action="mainlist",
                                        channel="personal", thumbnail=config.get_setting("personalchannellogo"),
                                        type="generic", viewmode="list"))

        channel_parameters = channeltools.get_channel_parameters("tengourl")
        # Si prefiere el bannermenu y el canal lo tiene, cambia ahora de idea
        if preferred_thumb == "bannermenu" and "bannermenu" in channel_parameters:
            channel_parameters["thumbnail"] = channel_parameters["bannermenu"]

        channelslist.insert(0, Item(title="Tengo una URL", action="mainlist", channel="tengourl",
                                    thumbnail=channel_parameters["thumbnail"], type="generic", viewmode="list"))

    return channelslist


def get_thumbnail_path(preferred_thumb=""):

    web_path = ""

    if preferred_thumb == "":
        thumbnail_type = config.get_setting("thumbnail_type")
        if thumbnail_type == "":
            thumbnail_type = 2
        if thumbnail_type == 0:
            web_path = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/posters/"
        elif thumbnail_type == 1:
            web_path = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/banners/"
        elif thumbnail_type == 2:
            web_path = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/squares/"
    else:
        web_path = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/" + preferred_thumb + "/"

    return web_path
