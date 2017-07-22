# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para playwire
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re
import xml.etree.ElementTree as ET

from core import jsontools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cachePage(page_url)
    if ("File was deleted" or "Not Found") in data: return False, "[playwire] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = scrapertools.cachePage(page_url)
    data = jsontools.load_json(data)
    f4m = data['content']['media']['f4m']

    video_urls = []
    data = scrapertools.downloadpageGzip(f4m)

    xml = ET.fromstring(data)
    base_url = xml.find('{http://ns.adobe.com/f4m/1.0}baseURL').text
    for media in xml.findall('{http://ns.adobe.com/f4m/1.0}media'):
        if ".m3u8" in media.get('url'): continue
        media_url = base_url + "/" + media.get('url')
        try:
            height = media.get('height')
            width = media.get('width')
            label = "(" + width + "x" + height + ")"
        except:
            label = ""
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " " + label + " [playwire]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://config.playwire.com/18542/videos/v2/3154852/zeus.json
    # http://cdn.playwire.com/54884/embed/12487.html
    patronvideos = '(?:cdn|config).playwire.com(?:/v2|)/(\d+)/(?:embed|videos/v2|config)/(\d+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[playwire]"
        url = "http://config.playwire.com/%s/videos/v2/%s/zeus.json" % (match[0], match[1])
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'playwire'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
