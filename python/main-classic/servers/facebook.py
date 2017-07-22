# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videos externos de facebook
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re
import urllib

from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    page_url = page_url.replace("amp;", "")
    data = scrapertools.cache_page(page_url)
    logger.info("data=" + data)

    video_urls = []

    patron = "video_src.*?(http.*?)%22%2C%22video_timestamp"
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for match in matches:
        videourl = match
        logger.info(match)
        videourl = videourl.replace('%5C', '')
        videourl = urllib.unquote(videourl)
        video_urls.append(["[facebook]", videourl])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # Facebook para AnimeID    src="http://www.facebook.com/v/194008590634623" type="application/x-shockwave-flash"
    # Facebook para Buena isla src='http://www.facebook.com/v/134004263282552_44773.mp4&amp;video_title=Vid&amp;v=1337'type='application/x-shockwave-flash'
    patronvideos = 'http://www.facebook.com/v/([\d]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Facebook]"
        url = "http://www.facebook.com/video/external_video.php?v=" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'facebook'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # Estos vídeos son en realidad enlaces directos
    # http://video.ak.facebook.com/cfs-ak-ash2/33066/239/133241463372257_27745.mp4
    patronvideos = '(http://video.ak.facebook.com/.*?\.mp4)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[facebook]"
        url = match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'directo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
