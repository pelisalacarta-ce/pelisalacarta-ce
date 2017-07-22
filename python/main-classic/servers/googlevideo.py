# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Google Video basado en flashvideodownloader.org
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    video_urls = []

    # Lo extrae a partir de flashvideodownloader.org
    if page_url.startswith("http://"):
        url = 'http://www.flashvideodownloader.org/download.php?u=' + page_url
    else:
        url = 'http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid=' + page_url
    logger.info("url=" + url)
    data = scrapertools.cache_page(url)

    # Extrae el vídeo
    newpatron = '</script>.*?<a href="(.*?)" title="Click to Download">'
    newmatches = re.compile(newpatron, re.DOTALL).findall(data)
    if len(newmatches) > 0:
        video_urls.append(["[googlevideo]", newmatches[0]])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    patronvideos = 'http://video.google.com/googleplayer.swf.*?docid=([0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[googlevideo]"
        if match.count("&") > 0:
            primera = match.find("&")
            url = match[:primera]
        else:
            url = match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'googlevideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
