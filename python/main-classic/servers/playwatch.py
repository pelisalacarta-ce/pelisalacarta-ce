# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para playwatch
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import base64
import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    response = httptools.downloadpage(page_url, follow_redirects=False)

    if not response.sucess or response.headers.get("location"):
        return False, "[Playwatch] El fichero no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = httptools.downloadpage(page_url, follow_redirects=False).data

    code = scrapertools.find_single_match(data, ' tracker:\s*"([^"]+)"')
    media_url = base64.b64decode(code)
    ext = scrapertools.get_filename_from_url(media_url)[-4:]
    video_urls = [["%s  [playwatch]" % ext, media_url]]

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    # http://playwatch.me/z3nnqbspjyne
    # http://playwatch.me/embed/z3nnqbspjyne
    patronvideos = 'playwatch.me/(?:embed/|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[playwatch]"
        url = "http://playwatch.me/embed/%s" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'playwatch'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
