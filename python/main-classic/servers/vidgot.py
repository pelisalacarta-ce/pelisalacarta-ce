# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidgot
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

    if "File was deleted" in data:
        return False, "[Vidgot] El fichero ha sido borrado de novamov"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    data_js = scrapertools.find_single_match(data, "<script type='text/javascript'>(eval\(function.*?)</script>")
    data_js = jsunpack.unpack(data_js)

    mediaurls = scrapertools.find_multiple_matches(data_js, '\{file\s*:\s*"([^"]+)"\}')

    video_urls = []
    for mediaurl in mediaurls:
        ext = scrapertools.get_filename_from_url(mediaurl)[-4:]
        if "mp4" not in ext and "m3u8" not in ext:
            continue
        video_urls.append([ext + " [vidgot]", mediaurl])

    return video_urls


def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://vidgot.com/embed-vidk2kbjvpu8121.html
    patronvideos = 'vidgot.com/(?:embed-|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[vidgot]"
        url = "http://www.vidgot.com/embed-%s.html" % match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vidgot'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
