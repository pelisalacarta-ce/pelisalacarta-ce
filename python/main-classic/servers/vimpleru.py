# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vimple.ru
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import config
from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    if '"title":"Video Not Found"' in data:
        return False, "[Vimple] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url=%s)" % page_url)

    data = httptools.downloadpage(page_url).data

    media_url = scrapertools.find_single_match(data, '"video"[^,]+,"url":"([^"]+)"').replace('\\', '')
    data_cookie = config.get_cookie_data()
    cfduid = scrapertools.find_single_match(data_cookie, '.vimple.ru.*?(__cfduid\t[a-f0-9]+)') \
        .replace('\t', '=')
    univid = scrapertools.find_single_match(data_cookie, '.vimple.ru.*?(UniversalUserID\t[a-f0-9]+)') \
        .replace('\t', '=')

    media_url += "|User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0" \
                 "&Cookie=%s; %s" % (cfduid, univid)

    video_urls = []
    video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [vimple.ru]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://player.vimple.ru/iframe/21ff2440e9174286ad8c22cd2efb94d2
    patronvideos = 'vimple.ru/iframe/([a-f0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vimpleru]"
        url = "http://player.vimple.ru/iframe/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vimpleru'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
