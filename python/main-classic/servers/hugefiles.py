# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para hugefiles
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Based on the hugefiles resolver from script.modules.urlresolver
# ------------------------------------------------------------

import re
import urllib

from core import logger
from core import scrapertools
from lib import jsunpack


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    # Submit
    post = {}
    r = re.findall(r'type="hidden" name="(.+?)"\s* value="?(.+?)">', data)
    for name, value in r:
        post[name] = value
        post.update({'method_free': 'Free Download'})
    data = scrapertools.cache_page(page_url, post=urllib.urlencode(post))

    # Get link
    sPattern = '''<div id="player_code">.*?<script type='text/javascript'>(eval.+?)</script>'''
    r = re.findall(sPattern, data, re.DOTALL | re.I)
    mediaurl = ""
    if r:
        sUnpacked = jsunpack.unpack(r[0])
        sUnpacked = sUnpacked.replace("\\'", "")
        r = re.findall('file,(.+?)\)\;s1', sUnpacked)
        if not r:
            r = re.findall('"src"value="(.+?)"/><embed', sUnpacked)

        mediaurl = r[0]

    video_urls = []
    video_urls.append([scrapertools.get_filename_from_url(mediaurl)[-4:] + " [hugefiles]", mediaurl])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.hugefiles.net/m23qtxy5bnlw
    patronvideos = 'hugefiles.net/([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[hugefiles]"
        url = "http://www.hugefiles.net/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'hugefiles'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
