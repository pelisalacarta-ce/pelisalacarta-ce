# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para speedvideo
# by be4t5
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import base64
import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    video_urls = []

    data = scrapertools.cachePage(page_url)

    codif = scrapertools.find_single_match(data, 'var [a-z]+ = ([0-9]+);')
    link = scrapertools.find_single_match(data, 'linkfile ="([^"]+)"')
    numero = int(codif)

    # Decrypt link base64 // python version of speedvideo's base64_decode() [javascript]

    link1 = link[:numero]
    link2 = link[numero + 10:]
    link = link1 + link2
    media_url = base64.b64decode(link)

    video_urls.append(["." + media_url.rsplit('.', 1)[1] + ' [speedvideo]', media_url])

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://speedvideo.net/embed-fmbvopi1381q-530x302.html
    # http://speedvideo.net/hs7djap7jwrw/Tekken.Kazuyas.Revenge.2014.iTALiAN.Subbed.DVDRiP.XViD.NeWZoNe.avi.html
    patronvideos = 'speedvideo.net/(?:embed-|)([A-Z0-9a-z]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[speedvideo]"
        url = "http://speedvideo.net/embed-%s.html" % match
        if url not in encontrados and url != "http://speedvideo.net/embed":
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'speedvideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

            # Cineblog by be4t5
    patronvideos = 'cineblog01.../HR/go.php\?id\=([0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)
    page = scrapertools.find_single_match(text, 'rel="canonical" href="([^"]+)"')
    from lib import mechanize
    br = mechanize.Browser()
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_robots(False)

    for match in matches:

        titulo = "[speedvideo]"
        url = "http://cineblog01.pw/HR/go.php?id=" + match
        r = br.open(page)
        req = br.click_link(url=url)
        data = br.open(req)
        data = data.read()
        data = scrapertools.find_single_match(data, 'speedvideo.net/([^"]+)"?')
        if data == "":
            continue
        d = data.split('-')
        if len(d) > 1:
            data = d[1]

        url = "http://speedvideo.net/" + data
        d = scrapertools.cache_page(url)
        ma = scrapertools.find_single_match(d, '<title>Watch ([^<]+)</title>')
        ma = titulo + " " + ma

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([ma, url, 'speedvideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
