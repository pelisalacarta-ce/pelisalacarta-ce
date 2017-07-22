# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para cnubis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("page_url=" + page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url)
    media_url = scrapertools.find_single_match(data, 'file: "([^"]+)",.*?type: "([^"]+)"')
    logger.info("media_url=" + media_url[0])

    # URL del vídeo
    video_urls.append(["." + media_url[1] + " [cnubis]", media_url[0].replace("https", "http")])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # https://cnubis.com/plugins/mediaplayer/site/_1embed.php?u=9mk&w=640&h=320
    # http://cnubis.com/plugins/mediaplayer/site/_2embed.php?u=2aZD
    # http://cnubis.com/plugins/mediaplayer/embed/_2embed.php?u=U6w
    patronvideos = 'cnubis.com/plugins/mediaplayer/(.*?/[^.]+.php\?u\=[A-Za-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[cnubis]"
        url = "http://cnubis.com/plugins/mediaplayer/%s" % (match)
        if url not in encontrados and id != "":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'cnubis'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
