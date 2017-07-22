# -*- coding: iso-8859-1 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para VK Server
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    if "This video has been removed from public access" in data:
        return False, "El archivo ya no esta disponible<br/>en VK (ha sido borrado)"
    else:
        return True, ""


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    video_urls = []
    try:
        oid, id = scrapertools.find_single_match(page_url, 'oid=([^&]+)&id=(\d+)')
    except:
        oid, id = scrapertools.find_single_match(page_url, 'video(\d+)_(\d+)')

    from core import httptools
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = "http://vk.com/al_video.php?act=show_inline&al=1&video=%s_%s" % (oid, id)
    data = httptools.downloadpage(url, headers=headers).data

    matches = scrapertools.find_multiple_matches(data, '<source src="([^"]+)" type="video/(\w+)')
    for media_url, ext in matches:
        calidad = scrapertools.find_single_match(media_url, '(\d+)\.%s' % ext)
        video_urls.append(["." + ext + " [vk:" + calidad + "]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://vkontakte.ru/video_ext.php?oid=95855298&id=162902512&hash=4f0d023887f3648e
    # http://vk.com/video_ext.php?oid=70712020&amp;id=159787030&amp;hash=88899d94685174af&amp;hd=3"
    # http://vk.com/video_ext.php?oid=161288347&#038;id=162474656&#038;hash=3b4e73a2c282f9b4&#038;sd
    # http://vk.com/video_ext.php?oid=146263567&id=163818182&hash=2dafe3b87a4da653&sd
    # http://vk.com/video_ext.php?oid=146263567&id=163818182&hash=2dafe3b87a4da653
    # http://vk.com/video_ext.php?oid=-34450039&id=161977144&hash=0305047ffe3c55a8&hd=3
    data = data.replace("&amp;", "&")
    data = data.replace("&#038;", "&")
    patronvideos = '(/video_ext.php\?oid=[^&]+&id=[^&]+&hash=[a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[vk]"
        url = "http://vk.com" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vk'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://vk.com/video97482389_161509127?section=all
    patronvideos = '(vk\.[a-z]+\/video[0-9]+_[0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[vk]"
        url = "http://" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vk'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
