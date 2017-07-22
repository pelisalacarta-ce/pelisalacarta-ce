# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para filefactory
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []
    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = "(www.filefactory.com/file.*?\.mkv)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filefactory]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'filefactory'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = "(www.filefactory.com/file.*?\.mp4)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filefactory]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'filefactory'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://www.filefactory.com/file/35ip193vzp1f/n/HMD-5x19-ESP.avi
    patronvideos = "(www.filefactory.com/file.*?\.avi)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filefactory]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'filefactory'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = "(www.filefactory.com/file.*?\.rar)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filefactory]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'filefactory'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://filefactory.com/file/15437757
    patronvideos = '(filefactory.com/file/[a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[filefactory]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'filefactory'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
