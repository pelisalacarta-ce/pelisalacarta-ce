# -*- coding: iso-8859-1 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para zstream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    if "File was deleted" in data:
        return False, "[Zstream] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=%s" % page_url)
    video_urls = []

    data = httptools.downloadpage(page_url).data

    matches = scrapertools.find_multiple_matches(data, '\{file:"([^"]+)",label:"([^"]+)"')
    for media_url, calidad in matches:
        calidad = "." + media_url.rsplit('.', 1)[1] + " " + calidad
        video_urls.append([calidad + ' [zstream]', media_url])

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://zstream.to/kgcldj6y8l8t.html
    patronvideos = 'zstream.to/(?:embed-|)([A-z0-9]+)'
    logger.info("#%s#" % patronvideos)
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[zstream]"
        url = "http://zstream.to/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'zstream'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
