# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import glob
import os
import re
import time
from threading import Thread

from core import channeltools
from core import config
from core import logger
from core.item import Item
from platformcode import platformtools


def mainlist(item):
    logger.info()
    item.channel = "buscador"

    itemlist = list()
    context = [{"title": "Elegir canales incluidos",
                "action": "settingCanal",
                "channel": item.channel}]
    itemlist.append(Item(channel=item.channel, action="search",
                         title="Buscar por titulo", context=context,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    itemlist.append(Item(channel=item.channel, action="search",
                         title="Buscar por categorias (busqueda avanzada)", extra="categorias",
                         context=context,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    itemlist.append(Item(channel=item.channel, action="opciones", title="Opciones",
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))

    saved_searches_list = get_saved_searches()
    context2 = context[:]
    context2.append({"title": "Borrar búsquedas guardadas",
                     "action": "clear_saved_searches",
                     "channel": item.channel})
    logger.info("saved_searches_list=%s" % saved_searches_list)
    if saved_searches_list != []:
        itemlist.append(Item(channel=item.channel, action="",
                             title="Busquedas guardadas:", context=context2,
                             thumbnail=get_thumbnail_path("thumb_buscar.png")))
        for saved_search_text in saved_searches_list:
            itemlist.append(Item(channel=item.channel, action="do_search",
                                 title='    "' + saved_search_text + '"',
                                 extra=saved_search_text, context=context2,
                                 category=saved_search_text,
                                 thumbnail=get_thumbnail_path("thumb_buscar.png")))

    return itemlist


def opciones(item):
    itemlist = list()
    itemlist.append(Item(channel=item.channel, action="settingCanal",
                         title="Elegir canales incluidos en la búsqueda",
                         folder=False, thumbnail=get_thumbnail_path("thumb_buscar.png")))
    itemlist.append(Item(channel=item.channel, action="clear_saved_searches",
                         title="Borrar búsquedas guardadas", folder=False,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    itemlist.append(Item(channel=item.channel, action="settings",
                         title="Otros ajustes", folder=False,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    return itemlist


def get_thumbnail_path(thumb_name):
    import urlparse
    web_path = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/squares/"
    return urlparse.urljoin(web_path, thumb_name)


def settings(item):
    return platformtools.show_channel_settings()


def settingCanal(item):
    channels_path = os.path.join(config.get_runtime_path(), "channels", '*.xml')
    channel_language = config.get_setting("channel_language")

    if channel_language == "":
        channel_language = "all"

    list_controls = []
    for infile in sorted(glob.glob(channels_path)):
        channel_name = os.path.basename(infile)[:-4]
        channel_parameters = channeltools.get_channel_parameters(channel_name)

        # No incluir si es un canal inactivo
        if channel_parameters["active"] != True:
            continue

        # No incluir si es un canal para adultos, y el modo adulto está desactivado
        if channel_parameters["adult"] == True and config.get_setting("adult_mode") == 0:
            continue

        # No incluir si el canal es en un idioma filtrado
        if channel_language != "all" and channel_parameters["language"] != channel_language:
            continue

        # No incluir si en la configuracion del canal no existe "include_in_global_search"
        include_in_global_search = channel_parameters["include_in_global_search"]

        if include_in_global_search == False:
            continue
        else:
            # Se busca en la configuración del canal el valor guardado
            include_in_global_search = config.get_setting("include_in_global_search", channel_name)

        control = {'id': channel_name,
                   'type': "bool",
                   'label': channel_parameters["title"],
                   'default': include_in_global_search,
                   'enabled': True,
                   'visible': True}

        list_controls.append(control)


    if config.get_setting("custom_button_value", item.channel):
        custom_button_label = "Ninguno"
    else:
        custom_button_label = "Todos"

    return platformtools.show_channel_settings(list_controls=list_controls,
                                               caption="Canales incluidos en la búsqueda global",
                                               callback="save_settings", item=item,
                                               custom_button={'visible': True,
                                                              'function':"cb_custom_button",
                                                              'close': False,
                                                              'label':custom_button_label})


def save_settings(item, dict_values):
    progreso = platformtools.dialog_progress("Guardando configuración...", "Espere un momento por favor.")
    n = len(dict_values)
    for i, v in enumerate(dict_values):
        progreso.update((i * 100) / n, "Guardando configuración...")
        config.set_setting("include_in_global_search", dict_values[v], v)

    progreso.close()


def cb_custom_button(item, dict_values):
    value = config.get_setting("custom_button_value", item.channel)
    if value == "":
        value = False

    for v in dict_values.keys():
        dict_values[v] = not value

    if config.set_setting("custom_button_value", not value, item.channel) == True:
        return {"label": "Ninguno"}
    else:
        return {"label": "Todos"}


def searchbycat(item):
    # Only in xbmc/kodi
    # Abre un cuadro de dialogo con las categorías en las que hacer la búsqueda

    categories = ["Películas", "Series", "Anime", "Documentales", "VOS", "Latino"]
    categories_id = ["movie", "serie", "anime", "documentary", "vos", "latino"]
    list_controls = []
    for i, category in enumerate(categories):
        control = {'id': categories_id[i],
                   'type': "bool",
                   'label': category,
                   'default': False,
                   'enabled': True,
                   'visible': True}

        list_controls.append(control)
    control = {'id': "separador",
               'type': "label",
               'label': '',
               'default': "",
               'enabled': True,
               'visible': True}
    list_controls.append(control)
    control = {'id': "torrent",
               'type': "bool",
               'label': 'Incluir en la búsqueda canales Torrent',
               'default': True,
               'enabled': True,
               'visible': True}
    list_controls.append(control)

    return platformtools.show_channel_settings(list_controls=list_controls, caption="Elegir categorías",
                                               callback="search_cb", item=item)


def search_cb(item, values=""):
    cat = []
    for c in values:
        if values[c]:
            cat.append(c)

    if not len(cat):
        return None
    else:
        logger.info(item.tostring())
        logger.info(str(cat))
        return do_search(item, cat)


# Al llamar a esta función, el sistema pedirá primero el texto a buscar
# y lo pasará en el parámetro "tecleado"
def search(item, tecleado):
    logger.info()
    itemlist = []
    tecleado = tecleado.replace("+", " ")
    item.category = tecleado

    if tecleado != "":
        save_search(tecleado)

    if item.extra == "categorias":
        item.extra = tecleado
        itemlist = searchbycat(item)
    else:
        item.extra = tecleado
        itemlist = do_search(item, [])

    return itemlist


def show_result(item):
    tecleado = None
    if item.adult and config.get_setting("adult_request_password"):
        # Solicitar contraseña
        tecleado = platformtools.dialog_input("", "Contraseña para canales de adultos", True)
        if tecleado is None or tecleado != config.get_setting("adult_pin"):
            return []

    item.channel = item.__dict__.pop('from_channel')
    item.action = item.__dict__.pop('from_action')
    if item.__dict__.has_key('tecleado'):
        tecleado = item.__dict__.pop('tecleado')

    try:
        channel = __import__('channels.%s' % item.channel, fromlist=["channels.%s" % item.channel])
    except:
        import traceback
        logger.error(traceback.format_exc())
        return []


    if tecleado:
        # Mostrar resultados: agrupados por canales
        return channel.search(item, tecleado)
    else:
        # Mostrar resultados: todos juntos
        try:
            from platformcode import launcher
            launcher.run(item)
        except ImportError:
            return getattr(channel, item.action)(item)



def channel_search(search_results, channel_parameters, tecleado):
    try:
        exec "from channels import " + channel_parameters["channel"] + " as module"
        mainlist = module.mainlist(Item(channel=channel_parameters["channel"]))
        search_items = [item for item in mainlist if item.action == "search"]
        if not search_items:
            search_items = [Item(channel=channel_parameters["channel"], action="search")]

        for item in search_items:
            result = module.search(item.clone(), tecleado)
            if result is None:
                result = []
            if len(result):
                if not channel_parameters["title"] in search_results:
                    search_results[channel_parameters["title"]] = []

                search_results[channel_parameters["title"]].append({"item": item,
                                                                    "itemlist": result,
                                                                    "adult": channel_parameters["adult"]})

    except:
        logger.error("No se puede buscar en: %s" % channel_parameters["title"])
        import traceback
        logger.error(traceback.format_exc())


# Esta es la función que realmente realiza la búsqueda
def do_search(item, categories=[]):
    multithread = config.get_setting("multithread", "buscador")
    result_mode = "result_mode_%s" % config.get_setting("result_mode", "buscador")
    logger.info()

    tecleado = item.extra

    itemlist = []

    channels_path = os.path.join(config.get_runtime_path(), "channels", '*.xml')
    logger.info("channels_path=%s" % channels_path)

    channel_language = config.get_setting("channel_language")
    logger.info("channel_language=%s" % channel_language)
    if channel_language == "":
        channel_language = "all"
        logger.info("channel_language=%s" % channel_language)

    # Para Kodi es necesario esperar antes de cargar el progreso, de lo contrario
    # el cuadro de progreso queda "detras" del cuadro "cargando..." y no se le puede dar a cancelar
    time.sleep(0.5)
    progreso = platformtools.dialog_progress("Buscando '%s'..." % tecleado, "")
    channel_files = sorted(glob.glob(channels_path), key=lambda x: os.path.basename(x))
    number_of_channels = len(channel_files)

    searches = []
    search_results = {}
    start_time = time.time()

    if multithread:
        progreso.update(0, "Buscando '%s'..." % tecleado)

    for index, infile in enumerate(channel_files):
        try:
            percentage = (index * 100) / number_of_channels

            basename = os.path.basename(infile)
            basename_without_extension = basename[:-4]
            if basename_without_extension == "version": continue
            logger.info("%s..." % basename_without_extension)

            channel_parameters = channeltools.get_channel_parameters(basename_without_extension)

            # No busca si es un canal inactivo
            if channel_parameters["active"] != True:
                logger.info("%s no incluido" % basename_without_extension)
                continue

            # En caso de busqueda por categorias
            if categories:
                if not any(cat in channel_parameters["categories"] for cat in categories):
                    logger.info("%s no incluido" % basename_without_extension)
                    continue

            # No busca si es un canal para adultos, y el modo adulto está desactivado
            if channel_parameters["adult"] == True and config.get_setting("adult_mode") == 0:
                logger.info("%s no incluido" % basename_without_extension)
                continue

            # No busca si el canal es en un idioma filtrado
            if channel_language != "all" and channel_parameters["language"] != channel_language:
                logger.info("%s no incluido" % basename_without_extension)
                continue

            # No busca si es un canal excluido de la busqueda global
            include_in_global_search = channel_parameters["include_in_global_search"]
            if include_in_global_search == True:
                # Buscar en la configuracion del canal
                include_in_global_search = config.get_setting("include_in_global_search", basename_without_extension)

            if include_in_global_search != True:
                logger.info("%s no incluido" % basename_without_extension)
                continue

            if progreso.iscanceled():
                progreso.close()
                logger.info("Busqueda cancelada")
                return itemlist

            # Modo Multi Thread
            if multithread:
                t = Thread(target=channel_search, args=[search_results, channel_parameters, tecleado],
                           name=channel_parameters["title"])
                t.setDaemon(True)
                t.start()
                searches.append(t)

            # Modo single Thread
            else:
                logger.info("Intentado busqueda en " + basename_without_extension + " de " + tecleado)
                channel_search(search_results, channel_parameters, tecleado)

            logger.info("%s incluido en la busqueda" % basename_without_extension)
            progreso.update(percentage / 2, "Iniciada busqueda de '%s' en %s..." % (tecleado, channel_parameters["title"]))

        except:
            logger.error("No se puede buscar en: %s" % channel_parameters["title"])
            import traceback
            logger.error(traceback.format_exc())
            continue

    # Modo Multi Thread
    # Usando isAlive() no es necesario try-except,
    # ya que esta funcion (a diferencia de is_alive())
    # es compatible tanto con versiones antiguas de python como nuevas
    if multithread:
        pendent = [a for a in searches if a.isAlive()]
        while pendent:
            percentage = (len(searches) - len(pendent)) * 100 / len(searches)
            completed = len(searches) - len(pendent)

            if len(pendent) > 5:
                progreso.update(percentage, "Busqueda terminada en %d de %d canales..." % (completed, len(searches)))
            else:
                list_pendent_names = [a.getName() for a in pendent]
                mensaje = "Buscando en %s" % (", ".join(list_pendent_names))
                progreso.update(percentage, mensaje)
                logger.debug(mensaje)

            if progreso.iscanceled():
                logger.info("Busqueda cancelada")
                break

            time.sleep(0.5)
            pendent = [a for a in searches if a.isAlive()]

    total = 0

    for channel in sorted(search_results.keys()):
        for search in search_results[channel]:
            total += len(search["itemlist"])
            title = channel
            if result_mode == "result_mode_0":
                if len(search_results[channel]) > 1:
                    title += " [" + search["item"].title.strip() + "]"
                title += " (" + str(len(search["itemlist"])) + ")"

                title = re.sub("\[COLOR [^\]]+\]", "", title)
                title = re.sub("\[/COLOR]", "", title)

                #extra = search["item"].extra + "{}" + search["item"].channel + "{}" + tecleado
                itemlist.append(Item(title=title, channel="buscador", action="show_result", url=search["item"].url,
                                     extra=search["item"].extra, folder=True, adult=search["adult"],from_action="search",
                                     from_channel=search["item"].channel, tecleado=tecleado))
            else:
                title = ">> Resultados del canal %s:" % title
                itemlist.append(Item(title=title, channel="buscador", action="",
                                     folder=False, text_color="yellow"))
                #itemlist.extend(search["itemlist"])
                for i in search["itemlist"]:
                    if i.action:
                        itemlist.append(i.clone(from_action=i.action, from_channel=i.channel, channel="buscador",
                                        action="show_result", adult=search["adult"]))

    title = "Buscando: '%s' | Encontrado: %d vídeos | Tiempo: %2.f segundos" % (tecleado, total, time.time()-start_time)
    itemlist.insert(0, Item(title=title, text_color='yellow'))

    progreso.close()

    return itemlist


def save_search(text):

    saved_searches_limit = int((10, 20, 30, 40, )[int(config.get_setting("saved_searches_limit", "buscador"))])

    current_saved_searches_list = config.get_setting("saved_searches_list", "buscador")
    if current_saved_searches_list is None:
        saved_searches_list = []
    else:
        saved_searches_list = list(current_saved_searches_list)

    if text in saved_searches_list:
        saved_searches_list.remove(text)

    saved_searches_list.insert(0, text)

    config.set_setting("saved_searches_list", saved_searches_list[:saved_searches_limit], "buscador")


def clear_saved_searches(item):

    config.set_setting("saved_searches_list", list(), "buscador")
    platformtools.dialog_ok("Buscador", "Búsquedas borradas correctamente")


def get_saved_searches():

    current_saved_searches_list = config.get_setting("saved_searches_list", "buscador")
    if current_saved_searches_list is None:
        saved_searches_list = []
    else:
        saved_searches_list = list(current_saved_searches_list)

    return saved_searches_list
