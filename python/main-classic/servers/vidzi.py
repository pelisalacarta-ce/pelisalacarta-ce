# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidzi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools
from lib import jsunpack


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    response = httptools.downloadpage(page_url)
    if not response.sucess or "File was deleted or expired" in response.data:
        return False, "[Vidzi] El archivo no existe o ha sido borrado"
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    if not "embed" in page_url:
        page_url = page_url.replace("http://vidzi.tv/","http://vidzi.tv/embed-") + ".html"
    
    data = httptools.downloadpage(page_url).data
    media_urls = scrapertools.find_multiple_matches(data, 'file\s*:\s*"([^"]+)"')

    if not media_urls:
        data = scrapertools.find_single_match(data, "<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d.*?)</script>")
        data = jsunpack.unpack(data)
        media_urls = scrapertools.find_multiple_matches(data, 'file\s*:\s*"([^"]+)"')

    video_urls = []
    for media_url in media_urls:
        ext = scrapertools.get_filename_from_url(media_url)[-4:]
        if not media_url.endswith("vtt"):
            video_urls.append(["%s [vidzi]" % ext, media_url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []
            
    patronvideos = 'vidzi.tv/(?:embed-|)([0-9A-z]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vidzi]"
        url = "http://vidzi.tv/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vidzi'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)
    return devuelve
