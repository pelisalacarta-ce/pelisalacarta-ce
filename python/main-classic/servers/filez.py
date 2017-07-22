# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para filez
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url, follow_redirects=False)

    if data.headers.get("location"):
        return False, "[filez] El archivo ha sido eliminado o no existe"
    
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    
    data = httptools.downloadpage(page_url).data

    video_urls = []
    media_urls = scrapertools.find_multiple_matches(data, 'file\s*:\s*"([^"]+)",\s*type\s*:\s*"([^"]+)"')
    for media_url, ext in media_urls:
        video_urls.append([".%s [filez]" % ext, media_url])

    if not video_urls:
        media_urls = scrapertools.find_multiple_matches(data, '<embed.*?src="([^"]+)"')    
        for media_url in media_urls:
            media_url = media_url.replace("https:", "http:")
            ext = httptools.downloadpage(media_url, only_headers=True).headers.get("content-disposition", "")
            ext = scrapertools.find_single_match(ext, 'filename="([^"]+)"')
            if ext:
                ext = ext[-4:]
            video_urls.append(["%s [filez]" % ext, media_url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos = 'filez.tv/(?:embed/u=|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filez]"
        url = "https://filez.tv/embed/u=" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'filez'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
