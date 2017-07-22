# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para fileflyer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    # Vídeo borrado: http://www.fileflyer.com/view/fioZRBu
    # Video erróneo: 
    data = scrapertools.cache_page(page_url)
    if '<a href="/RemoveDetail.aspx">' in data:
        return False, "El archivo ya no está disponible<br/>en fileflyer (ha sido borrado)"
    else:
        return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url)
    location = scrapertools.get_match(data,
                                      '<td class="dwnlbtn"[^<]+<a id="[^"]+" title="[^"]+" class="[^"]+" href="([^"]+)"')

    video_urls.append([scrapertools.get_filename_from_url(location)[-4:] + " [fileflyer]", location])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.fileflyer.com/view/fioZRBu
    patronvideos = '(fileflyer.com/view/[a-zA-Z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[fileflyer]"
        url = "http://www." + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'fileflyer'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
