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
# --------------------------------------------------------------------------------
# json_tools - JSON load and parse functions with library detection
# --------------------------------------------------------------------------------

import re
import sys
import traceback
import logger


try:
    import json
except:
    logger.info("json incluido en el interprete **NO** disponible")

    try:
        import simplejson as json
    except:
        logger.info("simplejson incluido en el interprete **NO** disponible")
        try:
            from lib import simplejson as json
        except:
            logger.info("simplejson en el directorio lib **NO** disponible")
            logger.error("No se ha encontrado un parser de JSON valido")
            json = None
        else:
            logger.info("Usando simplejson en el directorio lib")
    else:
        logger.info("Usando simplejson incluido en el interprete")
else:
    logger.info("Usando json incluido en el interprete")


def load_json(*args, **kwargs):
    if "object_hook" not in kwargs:
        kwargs["object_hook"] = to_utf8

    try:
        value = json.loads(*args, **kwargs)
    except:
        logger.error("**NO** se ha podido cargar el JSON")
        logger.error(traceback.format_exc())
        value = {}

    return value


def dump_json(*args, **kwargs):
    if not kwargs:
        kwargs = {"indent": 4, "skipkeys": True, "sort_keys": True, "ensure_ascii": False}

    try:
        value = json.dumps(*args, **kwargs)
    except:
        logger.error("**NO** se ha podido cargar el JSON")
        logger.error(traceback.format_exc())
        value = ""
    return value


def to_utf8(dct):

    if isinstance(dct, dict):
        return dict((to_utf8(key), to_utf8(value)) for key, value in dct.iteritems())
    elif isinstance(dct, list):
        return [to_utf8(element) for element in dct]
    elif isinstance(dct, unicode):
        return dct.encode('utf-8')
    else:
        return dct


def xmlTojson(file=None, xmldata=None):
    """
    Lee un fichero o texto XML y retorna un diccionario json

    Parametros:
    file (str) -- Ruta completa al archivo XML que se desea convertir en JSON.
    xmldata (str) -- Texto XML que se desea convertir en JSON.

    Retorna:
    Un diccionario construido a partir de los campos del XML.

    """
    from core import filetools
    parse = globals().get(sys._getframe().f_code.co_name)

    if xmldata is None and file is None:
        raise Exception("No hay nada que convertir!")
    elif xmldata is None:
        if not filetools.exists(file):
            raise Exception("El archivo no existe!")
        xmldata = open(file, "rb").read()

    matches = re.compile("<(?P<tag>[^>]+)>[\n]*[\s]*[\t]*(?P<value>.*?)[\n]*[\s]*[\t]*<\/(?P=tag)\s*>",
                         re.DOTALL).findall(xmldata)

    return_dict = {}
    for tag, value in matches:
        # Si tiene elementos
        if "<" and "</" in value:
            if tag in return_dict:
                if type(return_dict[tag]) == list:
                    return_dict[tag].append(parse(xmldata=value))
                else:
                    return_dict[tag] = [return_dict[tag]]
                    return_dict[tag].append(parse(xmldata=value))
            else:
                return_dict[tag] = parse(xmldata=value)

        else:
            if tag in return_dict:
                if type(return_dict[tag]) == list:
                    return_dict[tag].append(value)
                else:
                    return_dict[tag] = [return_dict[tag]]
                    return_dict[tag].append(value)
            else:
                if value in ["true", "false"]:
                    if value == "true":
                        value = True
                    else:
                        value = False

                return_dict[tag] = value

    return return_dict


def get_node_from_data_json(name_file, node, path=None):
    """
    Obtiene el nodo de un fichero JSON

    @param name_file: Puede ser el nombre de un canal o server (sin incluir extension)
     o bien el nombre de un archivo json (con extension)
    @type name_file: str
    @param node: nombre del nodo a obtener
    @type node: str
    @param path: Ruta base del archivo json. Por defecto la ruta de settings_channels.
    @return: dict con el nodo a devolver
    @rtype: dict
    """
    logger.info()
    from core import config
    from core import filetools

    dict_node = {}

    if not name_file.endswith(".json"):
        name_file += "_data.json"

    if not path:
        path = filetools.join(config.get_data_path(), "settings_channels")

    fname = filetools.join(path , name_file)


    if filetools.isfile(fname):
        data = filetools.read(fname)
        dict_data = load_json(data)

        check_json_file(data, fname, dict_data)

        if node in dict_data:
            dict_node = dict_data[node]

    logger.debug("dict_node: %s" % dict_node)

    return dict_node


def check_json_file(data, fname, dict_data):
    """
    Comprueba que si dict_data(conversion del fichero JSON a dict) no es un diccionario, se genere un fichero con
    data de nombre fname.bk.

    @param data: contenido del fichero fname
    @type data: str
    @param fname: nombre del fichero leido
    @type fname: str
    @param dict_data: nombre del diccionario
    @type dict_data: dict
    """
    logger.info()

    if not dict_data:
        logger.error("Error al cargar el json del fichero %s" % fname)

        if data != "":
            # se crea un nuevo fichero
            from core import filetools
            title = filetools.write("%s.bk" % fname, data)
            if title != "":
                logger.error("Ha habido un error al guardar el fichero: %s.bk" % fname)
            else:
                logger.debug("Se ha guardado una copia con el nombre: %s.bk" % fname)
        else:
            logger.debug("Está vacío el fichero: %s" % fname)


def update_json_data(dict_node, name_file, node, path=None):
    """
    actualiza el json_data de un fichero con el diccionario pasado

    @param dict_node: diccionario con el nodo
    @type dict_node: dict
    @param name_file: Puede ser el nombre de un canal o server (sin incluir extension)
     o bien el nombre de un archivo json (con extension)
    @type name_file: str
    @param node: nodo a actualizar
    @param path: Ruta base del archivo json. Por defecto la ruta de settings_channels.
    @return result: Devuelve True si se ha escrito correctamente o False si ha dado un error
    @rtype: bool
    @return json_data
    @rtype: dict
    """
    logger.info()

    from core import config
    from core import filetools
    json_data = {}
    result = False

    if not name_file.endswith(".json"):
        name_file += "_data.json"

    if not path:
        path = filetools.join(config.get_data_path(), "settings_channels")

    fname = filetools.join(path, name_file)

    try:
        data = filetools.read(fname)
        dict_data = load_json(data)
        # es un dict
        if dict_data:
            if node in dict_data:
                logger.debug("   existe el key %s" % node)
                dict_data[node] = dict_node
            else:
                logger.debug("   NO existe el key %s" % node)
                new_dict = {node: dict_node}
                dict_data.update(new_dict)
        else:
            logger.debug("   NO es un dict")
            dict_data = {node: dict_node}
        json_data = dump_json(dict_data)
        result = filetools.write(fname, json_data)
    except:
        logger.error("No se ha podido actualizar %s" % fname)

    return result, json_data
