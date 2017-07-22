# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para depositfiles
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    # Existe: http://depositfiles.com/files/vmhjug6t7
    # No existe: 
    data = scrapertools.cache_page(page_url)
    patron = 'Nombre del Archivo: <b title="([^"]+)">([^<]+)</b>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 0:
        return True, ""
    else:
        patron = '<div class="no_download_msg">([^<]+)<'
        matches = re.compile(patron, re.DOTALL).findall(data)
        if len(matches) > 0:
            return False, "El archivo ya no está disponible<br/>en depositfiles o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []
    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://depositfiles.com/files/jdxpu4cze
    # http://www.depositfiles.com/files/zqeggnpa6
    patronvideos = '(depositfiles.com/files/[a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[depositfiles]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'depositfiles'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
