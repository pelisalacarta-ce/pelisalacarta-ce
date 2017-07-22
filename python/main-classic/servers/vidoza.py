# -*- coding: utf-8 -*-
# --------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidoza
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# --------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    if "Page not found" in data:
        return False, "[vidoza] El archivo no existe o  ha sido borrado"
    elif "Video is processing now" in data:
        return False, "[vidoza] El vídeo se está procesando"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    video_urls = []
    matches = scrapertools.find_multiple_matches(data, 'file\s*:\s*"([^"]+)"\s*,\s*label:"([^"]+)"')
    for media_url, calidad in matches:
        ext = media_url[-4:]
        video_urls.append(["%s %s [vidoza]" % (ext, calidad), media_url])

    video_urls.reverse()
    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://vidoza.net/amtrusnrbkracsko.html
    patronvideos = 'vidoza.net/(?:embed-|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidoza]"
        url = "http://vidoza.net/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vidoza'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
