# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para thevideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools
from lib import jsunpack


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = httptools.downloadpage(page_url).data

    match = scrapertools.find_single_match(data, "<script type='text/javascript'>(.*?)</script>")
    if match.startswith("eval"):
        match = jsunpack.unpack(match)

    # Extrae la URL
    # {file:"http://95.211.81.229/kj2vy4rle46vtaw52bsj4ooof6meikcbmwimkrthrahbmy4re3eqg3buhoza/v.mp4",label:"240p"
    video_urls = []
    media_urls = scrapertools.find_multiple_matches(match, '\{file\:"([^"]+)",label:"([^"]+)"')
    subtitle = scrapertools.find_single_match(match, 'tracks: \[\{file: "([^"]+)", label: "Spanish"')
    for media_url, quality in media_urls:
        video_urls.append([media_url[-4:] + " [thevideos] " + quality, media_url, 0, subtitle])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    # http://thevideos.tv/fxp1ffutzw2y.html
    # http://thevideos.tv/embed-fxp1ffutzw2y.html
    patronvideos = 'thevideos.tv/(?:embed-|)([a-z0-9A-Z]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[thevideos]"
        url = "http://thevideos.tv/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'thevideos'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
