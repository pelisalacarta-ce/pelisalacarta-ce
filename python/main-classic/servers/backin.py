# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para backin.net
# by be4t5
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    # if '<meta property="og:title" content=""/>' in data:
    # return False,"The video has been cancelled from Backin.net"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    video_urls = []
    headers = []
    headers.append(["User-Agent",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"])

    # First access
    data = scrapertools.cache_page(page_url, headers=headers)
    logger.info("data=" + data)

    # URL
    url = scrapertools.find_single_match(data, 'type="video/mp4" src="([^"]+)"')
    logger.info("url=" + url)

    # URL del vídeo
    video_urls.append([".mp4" + " [backin]", url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://backin.net/iwbe6genso37
    patronvideos = '(?:backin).net/([A-Z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[backin]"
        url = "http://backin.net/s/generating.php?code=" + match
        if url not in encontrados and id != "":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'backin'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://cineblog01.pw/HR/go.php?id=6475
    temp = text.split('<strong>Streaming')
    if (len(temp) > 1):
        tem = temp[1].split('Download')
        patronvideos = '(?:HR)/go.php\?id\=([A-Z0-9]+)'
        logger.info("#" + patronvideos + "#")
        matches = re.compile(patronvideos, re.DOTALL).findall(tem[0])
    else:
        matches = []
    page = scrapertools.find_single_match(text, 'rel="canonical" href="([^"]+)"')
    from lib import mechanize
    br = mechanize.Browser()
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)

    for match in matches:
        titulo = "[backin]"
        url = "http://cineblog01.pw/HR/go.php?id=" + match
        r = br.open(page)
        req = br.click_link(url=url)
        data = br.open(req)
        data = data.read()
        id = scrapertools.find_single_match(data, 'http://backin.net/([^"]+)"')
        url = "http://backin.net/s/generating.php?code=" + id
        if url not in encontrados and id != "":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'backin'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://vcrypt.net/sb/0a8hqibleus5
    # Filmpertutti.eu
    tem = text.split('<p><strong>Download:<br />')
    patronvideos = 'http://vcrypt.net/sb/([^"]+)'
    matches = re.compile(patronvideos, re.DOTALL).findall(tem[0])
    page = scrapertools.find_single_match(text, 'rel="canonical" href="([^"]+)"')

    for match in matches:
        titulo = "[backin]"
        url = "http://vcrypt.net/sb/" + match
        r = br.open(url)
        data = r.read()
        id = scrapertools.find_single_match(data, '/streams-([^"]+)-')
        url = "http://backin.net/s/generating.php?code=" + id
        if url not in encontrados and id != "":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'backin'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
