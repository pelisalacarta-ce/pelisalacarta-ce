# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para watchers
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools
from lib import jsunpack


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    if "File Not Found" in data:
        return False, "[Watchers] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=%s" % page_url)
    video_urls = []

    data = httptools.downloadpage(page_url).data
    packed = scrapertools.find_single_match(data, '(eval\(function\(p,a,c,k,e.*?)</script>').strip()
    unpack = jsunpack.unpack(packed)

    bloque = scrapertools.find_single_match(unpack, 'sources:\[(.*?)\}\]')
    matches = scrapertools.find_multiple_matches(bloque, 'file:"([^"]+)"(?:,label:"([^"]+)"|\})')
    for media_url, calidad in matches:
        ext = scrapertools.get_filename_from_url(media_url)[-4:]
        if calidad:
            ext += " " + calidad + "p"
        media_url += "|Referer=%s" % page_url
        video_urls.append([ext + ' [watchers]', media_url])

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://watchers.to/kgcldj6y8l8t.html
    patronvideos = 'watchers.to/(?:embed-|)([A-z0-9]+)'
    logger.info("#%s#" % patronvideos)
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[watchers]"
        url = "http://watchers.to/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'watchers'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
