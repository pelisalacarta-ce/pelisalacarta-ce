# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para auroravid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    if "This file no longer exists on our servers" in data:
        return False, "[Auroravid] El fichero ha sido borrado"

    elif "is being converted" in data:
        return False, "[Auroravid] El fichero está en proceso todavía"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data

    video_urls = []
    videourls = scrapertools.find_multiple_matches(data, 'src\s*:\s*[\'"]([^\'"]+)[\'"]')
    if not videourls:
        videourls = scrapertools.find_multiple_matches(data, '<source src=[\'"]([^\'"]+)[\'"]')
    for videourl in videourls:
        if videourl.endswith(".mpd"):
            id = scrapertools.find_single_match(videourl, '/dash/(.*?)/')
            videourl = "http://www.auroravid.to/download.php%3Ffile=mm" + "%s.mp4" % id

        videourl = re.sub(r'/dl(\d)*/', '/dl/', videourl)
        ext = scrapertools.get_filename_from_url(videourl)[-4:]
        videourl = videourl.replace("%3F", "?") + \
                   "|User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
        video_urls.append([ext + " [auroravid]", videourl])

    return video_urls


def find_videos(data):
    encontrados = set()
    devuelve = []
    data = data.replace('novamov.com', 'auroravid.to')

    # http://embed.novamov.com/embed.php?width=568&height=340&v=zadsdfoc0pirx&px=1
    patronvideos = '(?:embed.|)auroravid.to/(?:video/|embed/\?v=)([A-z0-9]{13})'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[auroravid]"
        url = "http://www.auroravid.to/embed/?v=" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'auroravid'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
