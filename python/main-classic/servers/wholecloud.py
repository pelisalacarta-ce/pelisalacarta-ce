# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para wholecloud
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data

    if "This file no longer exists on our servers" in data:
        return False, "[wholecloud] El archivo ha sido eliminado o no existe"
    if "This video is not yet ready" in data:
        return False, "[wholecloud] El archivo no está listo, se está subiendo o convirtiendo"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = httptools.downloadpage(page_url).data

    video_urls = []
    media_urls = scrapertools.find_multiple_matches(data, '<source src="([^"]+)"')
    if not media_urls:
        media_url = scrapertools.find_single_match(data, 'src="/api/toker.php\?f=([^"]+)"')
        ext = scrapertools.get_filename_from_url(media_url)[-4:]
        media_url = "http://wholecloud.net/download.php?file=%s|User-Agent=Mozilla/5.0" % media_url
        video_urls.append([ext + " [wholecloud]", media_url])
    else:
        for media_url in media_urls:
            ext = scrapertools.get_filename_from_url(media_url)[-4:]
            media_url += "|User-Agent=Mozilla/5.0"
            video_urls.append([ext + " [wholecloud]", media_url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos = 'wholecloud.net/(?:video/|embed/?v=)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    for match in matches:
        titulo = "[wholecloud]"
        url = "http://wholecloud.net/embed/?v=" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'wholecloud'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
