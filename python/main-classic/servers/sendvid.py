# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para sendvid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    video_urls = []

    data = scrapertools.cache_page(page_url)
    # var video_source = "//cache-2.sendvid.com/1v0chsus.mp4";

    media_url = "http:" + scrapertools.find_single_match(data, 'var\s+video_source\s+\=\s+"([^"]+)"')

    if "cache-1" in media_url:
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " (cache1) [sendvid]", media_url])
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " (cache2) [sendvid]",
                           media_url.replace("cache-1", "cache-2")])

    elif "cache-2" in media_url:
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " (cache1) [sendvid]",
                           media_url.replace("cache-2", "cache-1")])
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " (cache2) [sendvid]", media_url])

    else:
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [sendvid]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # sendvid.com/embed/1v0chsus
    patronvideos = 'sendvid.com/embed/([a-zA-Z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[sendvid]"
        url = "http://sendvid.com/embed/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'sendvid'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
