# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mega.co.nz
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from platformcode import platformtools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []
    from megaserver import Client

    c = Client(url=page_url, is_playing_fnc=platformtools.is_playing)

    files = c.get_files()

    # si hay mas de 5 archivos crea un playlist con todos
    if len(files) > 5:
        media_url = c.get_play_list()
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [mega]", media_url])
    else:
        for f in files:
            media_url = f["url"]
            video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [mega]", media_url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = '(mega.co.nz/\#\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mega]"
        url = "https://" + match
        if url not in encontrados:
            logger.info(" url=" + url)
            devuelve.append([titulo, url, 'mega'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = '(mega.co.nz/\#F\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mega]"
        url = "https://" + match
        if url not in encontrados:
            logger.info(" url=" + url)
            devuelve.append([titulo, url, 'mega'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = '(mega.nz/\#\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mega]"
        url = "https://" + match
        if url not in encontrados:
            logger.info(" url=" + url)
            devuelve.append([titulo, url, 'mega'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = '(mega.nz/\#F\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mega]"
        url = "https://" + match
        if url not in encontrados:
            logger.info(" url=" + url)
            devuelve.append([titulo, url, 'mega'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
