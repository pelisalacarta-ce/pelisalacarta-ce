# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Vimeo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import jsontools
from core import logger
from core import scrapertools


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    headers = [['User-Agent', 'Mozilla/5.0']]
    if "|" in page_url:
        page_url, referer = page_url.split("|", 1)
        headers.append(['Referer', referer])

    if not page_url.endswith("/config"):
        page_url = find_videos(page_url)[0][1]

    video_urls = []
    data = scrapertools.downloadpage(page_url, headers=headers)
    json_object = jsontools.load_json(data)

    url_data = json_object['request']['files']['progressive']
    for data_media in url_data:
        media_url = data_media['url']
        title = "%s (%s) [vimeo]" % (data_media['mime'].replace("video/", "."), data_media['quality'])
        video_urls.append([title, media_url, data_media['height']])

    video_urls.sort(key=lambda x: x[2])
    try:
        video_urls.insert(0, [".m3u8 (SD) [vimeo]", json_object['request']['files']['hls']['cdns']
        ["akfire_interconnect"]["url"].replace("master.m3u8", "playlist.m3u8"), 0])
    except:
        pass
    for video_url in video_urls:
        video_url[2] = 0
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    referer = ""
    if "|" in text:
        referer = "|" + text.split("|", 1)[1]
    # http://player.vimeo.com/video/17555432?title=0&amp;byline=0&amp;portrait=0
    # http://vimeo.com/17555432
    patronvideos = '(?:vimeo.com/|player.vimeo.com/video/)([0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vimeo]"
        url = "https://player.vimeo.com/video/%s/config%s" % (match, referer)
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'vimeo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
