# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para turbobit
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []
    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://turbobit.net/scz8lxrrgllr.html
    # http://www.turbobit.net/uzo3gcyfmt4b.html
    # http://turbobit.net/eaz9ha3gop65/deadliest.catch.s08e09-killers.mp4.html
    patronvideos = '(turbobit.net/[0-9a-z]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[turbobit]"
        url = "http://" + match + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'turbobit'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
