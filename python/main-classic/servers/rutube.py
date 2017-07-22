# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rutube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import jsontools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cachePage(page_url)
    if ("File was deleted" or "Not Found") in data: return False, "[rutube] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = scrapertools.cachePage(page_url)
    if "embed" in page_url:
        link = scrapertools.find_single_match(data, '<link rel="canonical" href="https://rutube.ru/video/([\da-z]{32})')
        url = "http://rutube.ru/api/play/options/%s/?format=json" % link
        data = scrapertools.cachePage(url)

    data = jsontools.load_json(data)
    m3u8 = data['video_balancer']['m3u8']
    data = scrapertools.downloadpageGzip(m3u8)
    video_urls = []
    mediaurls = scrapertools.find_multiple_matches(data, '(http://.*?)\?i=(.*?)_')
    for media_url, label in mediaurls:
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " (" + label + ") [rutube]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://rutube.ru/video/dbfe808a8828dfcfb8c6b2ed6457eef/
    # http://rutube.ru/play/embed/78451
    patronvideos = 'rutube.ru\/(?:video\/([\da-zA-Z]{32})|play\/embed\/([\d]+))'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[rutube]"
        if len(match[0]) == 32:
            url = "http://rutube.ru/api/play/options/%s/?format=json" % match[0]
        else:
            url = "http://rutube.ru/video/embed/%s" % match[1]
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'rutube'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
