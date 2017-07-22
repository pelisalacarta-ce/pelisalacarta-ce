# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para divxstage/cloudtime
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools

host = "http://www.cloudtime.to"


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url.replace('/embed/?v=', '/video/')).data

    if "This file no longer exists" in data:
        return False, "El archivo no existe<br/>en divxstage o ha sido borrado."

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    if "divxstage.net" in page_url:
        page_url = page_url.replace("divxstage.net", "cloudtime.to")

    data = httptools.downloadpage(page_url).data

    video_urls = []
    videourls = scrapertools.find_multiple_matches(data, 'src\s*:\s*[\'"]([^\'"]+)[\'"]')
    if not videourls:
        videourls = scrapertools.find_multiple_matches(data, '<source src=[\'"]([^\'"]+)[\'"]')
    for videourl in videourls:
        if videourl.endswith(".mpd"):
            id = scrapertools.find_single_match(videourl, '/dash/(.*?)/')
            videourl = "http://www.cloudtime.to/download.php%3Ffile=mm" + "%s.mp4" % id

        videourl = re.sub(r'/dl(\d)*/', '/dl/', videourl)
        ext = scrapertools.get_filename_from_url(videourl)[-4:]
        videourl = videourl.replace("%3F", "?") + \
                   "|User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
        video_urls.append([ext + " [cloudtime]", videourl])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # divxstage http://www.divxstage.net/video/of7ww1tdv62gf"
    patronvideos = 'divxstage[^/]+/video/(\w+)$'
    logger.info("#" + patronvideos + "#")
    matches = scrapertools.find_multiple_matches(data, patronvideos)

    for match in matches:
        titulo = "[Divxstage]"
        url = host + "/embed/?v=" + match
        if url not in encontrados:
            logger.info("url=" + url)
            devuelve.append([titulo, url, 'divxstage'])
            encontrados.add(url)
        else:
            logger.info("url duplicada=" + url)

    # divxstage http://www.cloudtime.to/video/of7ww1tdv62gf"
    patronvideos = 'cloudtime[^/]+/(?:video/|embed/\?v=)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = scrapertools.find_multiple_matches(data, patronvideos)

    for match in matches:
        titulo = "[Cloudtime]"
        url = host + "/embed/?v=" + match
        if url not in encontrados:
            logger.info("url=" + url)
            devuelve.append([titulo, url, 'divxstage'])
            encontrados.add(url)
        else:
            logger.info("url duplicada=" + url)

    return devuelve
