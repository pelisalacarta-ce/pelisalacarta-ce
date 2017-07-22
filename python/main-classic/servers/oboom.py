# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para uploaz
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

    # http://uploaz.com/file/

    patronvideos = '(oboom.com/[a-zA-Z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[oboom]"
        url = "https://www." + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'oboom'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
