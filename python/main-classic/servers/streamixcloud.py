# -*- coding: utf-8 -*-
# --------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para streamixcloud
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# --------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools
from lib import jsunpack


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    if "Not Found" in data:
        return False, "[streamixcloud] El archivo no existe o  ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    video_urls = []
    packed = scrapertools.find_single_match(data, "<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d.*?)</script")
    data = jsunpack.unpack(packed)

    media_url = scrapertools.find_single_match(data, 'sources:\["([^"]+)"')
    ext = scrapertools.get_filename_from_url(media_url)[-4:]
    video_urls.append([".flv [streamixcloud]", media_url.replace(".mp4", ".flv")])
    video_urls.append(["%s [streamixcloud]" % ext, media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://streamix.cloud/amtrusnrbkracsko
    patronvideos = 'streamix.cloud/(?:embed-|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streamixcloud]"
        url = "http://streamix.cloud/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'streamixcloud'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
