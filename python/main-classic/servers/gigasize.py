# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para gigasize
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    # Vídeo borrado: http://www.gigasize.com/get/097fadecgh7pf
    # Video erróneo: 
    data = scrapertools.cache_page(page_url)
    if '<h2 class="error">Download error</h2>' in data:
        return False, "El enlace no es válido<br/>o ha sido borrado de gigasize"
    else:
        return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.gigasize.com/get/097f9cgh7pf
    patronvideos = '(gigasize.com/get/[a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[gigasize]"
        url = "http://www." + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'gigasize'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://www.gigasize.com/get.php?d=097f9cgh7pf
    patronvideos = 'gigasize.com/get.php\?d\=([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[gigasize]"
        url = "http://www.gigasize.com/get/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'gigasize'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
