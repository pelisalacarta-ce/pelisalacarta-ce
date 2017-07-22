# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para freakshare
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    # Existe: http://freakshare.com/files/wy6vs8zu/4x01-mundo-primitivo.avi.html
    # No existe: 
    data = scrapertools.cache_page(page_url)
    patron = '<h1 class="box_heading" style="text-align:center;">([^<]+)</h1>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    if len(matches) > 0:
        return True, ""
    else:
        patron = '<div style="text-align:center;"> (Este archivo no existe)'
        matches = re.compile(patron, re.DOTALL).findall(data)
        if len(matches) > 0:
            return False, matches[0]

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []
    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://freakshare.com/files/##/###.rar
    patronvideos = '(freakshare.com/files/.*?\.rar)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[freakshare]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'freakshare'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://freakshare.com/files/wy6vs8zu/4x01-mundo-primitivo.avi.html
    patronvideos = '(freakshare.com/files/.*?\.html)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[freakshare]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'freakshare'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
