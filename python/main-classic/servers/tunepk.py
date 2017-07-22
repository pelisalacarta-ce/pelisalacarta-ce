# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para tune.pk
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re

from core import logger
from core import scrapertools


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    video_urls = []

    data = scrapertools.cache_page(page_url)
    logger.info(data)
    patron = 'file: "([^"]+)",\s+'
    patron += 'width: "[^"]+",\s+'
    patron += 'height: "[^"]+",\s+'
    patron += 'label : "([^"]+)",\s+'
    patron += 'type : "([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for url, calidad, formato in matches:
        video_url = ["%s %s [tune.pk]" % (calidad, formato), url]
        video_urls.append(video_url)

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # Código embed
    patronvideos = 'tune.pk/player/embed_player.php\?vid\=(\d+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[tune.pk]"
        url = "http://embed.tune.pk/play/" + match + "?autoplay=no"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'tunepk'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
