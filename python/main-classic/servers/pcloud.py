# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para pCloud
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    if "Invalid link" in data: return False, "[pCloud] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = scrapertools.cache_page(page_url)
    media_url = scrapertools.find_single_match(data, '"downloadlink":.*?"([^"]+)"')
    media_url = media_url.replace("\\", "")

    video_urls = []
    video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [pCloud]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # https://my.pcloud.com/publink/show?code=XZhKu7Z49dTa1sEfLX9Tjgk8tESFGfXTjk
    patronvideos = "(my.pcloud.com/publink/show\?code=[A-z0-9]+)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[pCloud]"
        url = "https://%s" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'pCloud'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
