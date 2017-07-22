# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para veehd
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re
import urllib
import urlparse

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []

    headers = []
    headers.append(['User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:17.0) Gecko/20100101 Firefox/17.0'])
    setcookie = scrapertools.get_header_from_response(page_url, header_to_get="set-cookie")
    logger.info("setcookie=" + setcookie)
    try:
        cookie = scrapertools.get_match(setcookie, "(PHPSESSID.*?)\;")
    except:
        cookie = ""

    if cookie != "":
        headers.append(['Cookie', cookie + "; pp=1356263122; ppt=1"])

    data = scrapertools.cache_page(page_url, headers=headers)
    # logger.info("data="+data)

    url = scrapertools.get_match(data, '\$\("\#playeriframe"\).attr\(\{src \: "([^"]+)"')
    url = urlparse.urljoin(page_url, url)
    logger.info("url=" + url)

    headers.append(['Referer', page_url[:-1]])
    data = scrapertools.cache_page(url, headers=headers)
    logger.info("data=" + data)

    # <param name="src" value="http://v35.veehd.com/dl/f118c68806e2a98ca38a70b44b89d52b/1356264992/6000.4623246.avi&b=390">
    media_url = scrapertools.get_match(data, '<param name="src"value="([^"]+)"')

    video_urls = []

    if len(matches) > 0:
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [veehd]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://veehd.com/video/4623246#
    data = urllib.unquote(data)
    patronvideos = '(veehd.com/video/\d+\#)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veehd]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'veehd'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
