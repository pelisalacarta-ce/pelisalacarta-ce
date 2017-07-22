# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para enlaces a torrent y magnet
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re

from core import logger


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("server=torrent, la url es la buena")
    if page_url.startswith("magnet:"):
        video_urls = [["magnet: [torrent]", page_url]]
    else:
        video_urls = [[".torrent [torrent]", page_url]]

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    patronvideos = '(http:\/\/(?:.*?)\.torrent)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[torrent]"
        url = match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'torrent'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = '(magnet:\?xt=urn:[^"]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[torrent]"
        url = match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'torrent'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)
    return devuelve
