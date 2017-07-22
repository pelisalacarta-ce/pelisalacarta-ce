# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mp4upload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    logger.info("data=" + data)
    media_url = scrapertools.find_single_match(data, '"file": "(.+?)"')
    logger.info("media_url=" + media_url)
    media_url = media_url.replace("?start=0", "")
    logger.info("media_url=" + media_url)

    video_urls = list()
    video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [mp4upload]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    encontrados.add("http://www.mp4upload.com/embed/embed")
    devuelve = []

    # http://www.mp4upload.com/embed-g4vrsasad9iu.html
    patronvideos = 'mp4upload.com/embed-([A-Za-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mp4upload]"
        url = "http://www.mp4upload.com/embed-" + match + ".html"
        if url not in encontrados and match != "embed":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'mp4upload'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
