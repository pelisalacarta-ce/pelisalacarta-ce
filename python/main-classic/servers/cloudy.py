# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para cloudy
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import scrapertools
from core import httptools
from core import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    if "This video is being prepared" in data:
        return False, "[Cloudy] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    video_urls = []
    data = httptools.downloadpage(page_url).data

    media_urls = scrapertools.find_multiple_matches(data, '<source src="([^"]+)"')
    for mediaurl in media_urls:
        title = "%s [cloudy]" % scrapertools.get_filename_from_url(mediaurl)[-4:]
        mediaurl += "|User-Agent=Mozilla/5.0"
        video_urls.append([title, mediaurl])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.cloudy.ec/embed.php?id=189a5a19d08de
    patronvideos = 'cloudy.ec/(?:embed.php\?id=|v/)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[cloudy]"
        url = "https://www.cloudy.ec/embed.php?id=" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'cloudy'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
