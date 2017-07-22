# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para userporn
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import base64
import re

from core import logger
from core import scrapertools

HOSTER_KEY = "NTI2NzI5Cgo="


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    video_urls = []
    # Espera un poco como hace el player flash
    logger.info("waiting 3 secs")
    import time
    time.sleep(3)

    # Obtiene el id
    code = Extract_id(page_url)

    # Descarga el json con los detalles del vídeo
    # http://www.userporn.com/player_control/settings.php?v=dvthddkC7l4J&em=TRUE&fv=v1.1.45
    controluri = "http://userporn.com/player_control/settings.php?v=" + code + "&em=TRUE&fv=v1.1.45"
    datajson = scrapertools.cachePage(controluri)
    # logger.info("response="+datajson);

    # Convierte el json en un diccionario
    datajson = datajson.replace("false", "False").replace("true", "True")
    datajson = datajson.replace("null", "None")
    datadict = eval("(" + datajson + ")")

    # Formatos
    formatos = datadict["settings"]["res"]

    for formato in formatos:
        uri = base64.decodestring(formato["u"])
        resolucion = formato["l"]
        import videobb
        video_url = videobb.build_url(uri, HOSTER_KEY, datajson)
        video_urls.append(["%s [userporn]" % resolucion, video_url.replace(":80", "")])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


def Extract_id(url):
    _VALID_URL = r'^((?:http://)?(?:\w+\.)?userporn\.com/(?:(?:(?:e/)|(?:video/))|(?:(?:flash/)|(?:f/)))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
    # Extract video id from URL
    mobj = re.match(_VALID_URL, url)
    if mobj is None:
        logger.info('ERROR: URL invalida: %s' % url)
        return ""
    id = mobj.group(2)
    logger.info("extracted code=" + id)
    return id


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # Enlace estricto a userporn")
    # userporn tipo "http://www.userporn.com/f/szIwlZD8ewaH.swf"
    patronvideos = 'userporn.com\/f\/([A-Z0-9a-z]{12}).swf'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[userporn]"
        url = "http://www.userporn.com/video/" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'userporn'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # logger.info ("1) Enlace estricto a userporn")
    # userporn tipo "http://www.userporn.com/video/ZIeb370iuHE4"
    patronvideos = 'userporn.com\/video\/([A-Z0-9a-z]{12})'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[userporn]"
        url = "http://www.userporn.com/video/" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'userporn'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # logger.info ("2) Enlace estricto a userporn")
    # userporn tipo "http://www.userporn.com/e/LLqVzhw5ft7T"
    patronvideos = 'userporn.com\/e\/([A-Z0-9a-z]{12})'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[userporn]"
        url = "http://www.userporn.com/video/" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'userporn'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = "http\:\/\/(?:www\.)?userporn.com\/(?:(?:e/|flash/)|(?:(?:video/|f/)))?([a-zA-Z0-9]{0,12})"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    # print data
    for match in matches:
        titulo = "[Userporn]"
        url = "http://www.userporn.com/video/" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'userporn'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
