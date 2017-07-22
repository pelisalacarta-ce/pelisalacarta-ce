# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidto.me
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools

def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    if "Not Found" in data or "File Does not Exist" in data:
        return False, "[Vidto.me] El fichero no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = httptools.downloadpage(page_url).data
    # Extrae la URL
    # {file:"http://188.240.220.186/drjhpzy4lqqwws4phv3twywfxej5nwmi4nhxlriivuopt2pul3o4bkge5hxa/video.mp4",label:"240p"}
    video_urls = []
    media_urls = scrapertools.find_multiple_matches(data, '\{file\s*:\s*"([^"]+)",label\s*:\s*"([^"]+)"\}')
    for media_url, label in media_urls:
        ext = scrapertools.get_filename_from_url(media_url)[-4:]
        video_urls.append(["%s (%s) [vidto.me]" % (ext, label), media_url])

    video_urls.reverse()
    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    # http://vidto.me/z3nnqbspjyne
    # http://vidto.me/embed-z3nnqbspjyne
    patronvideos = 'vidto.me/(?:embed-|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidto.me]"
        url = "http://vidto.me/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vidtome'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
