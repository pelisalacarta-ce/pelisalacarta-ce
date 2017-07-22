# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para 4shared
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re

from core import logger
from core import scrapertools


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    video_urls = []

    if page_url.startswith("http://www.4shared"):
        # http://www.4shared.com/embed/392975628/ff297d3f
        page_url = scrapertools.get_header_from_response(page_url, header_to_get="location")

        # http://www.4shared.com/flash/player.swf?file=http://dc237.4shared.com/img/392975628/ff297d3f/dlink__2Fdownload_2Flj9Qu-tF_3Ftsid_3D20101030-200423-87e3ba9b/preview.flv&d
        logger.info("redirect a '%s'" % page_url)
        patron = "file\=([^\&]+)\&"
        matches = re.compile(patron, re.DOTALL).findall(page_url)

        try:
            video_urls.append(["[fourshared]", matches[0]])
        except:
            pass
    else:
        video_urls.append(["[fourshared]", page_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = "(http://www.4shared.com/embed/[A-Z0-9a-z]+/[A-Z0-9a-z]+)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'fourshared'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = 'file=(http\://[a-z0-9]+.4shared.com/img/.*?\.flv)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'fourshared'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = '"(http://www.4shared.com.*?)"'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados and url != "http://www.4shared.com/flash/player.swf":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'fourshared'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = "'(http://www.4shared.com.*?)'"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[4shared]"
        url = match

        if url not in encontrados and url != "http://www.4shared.com/flash/player.swf":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'fourshared'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
