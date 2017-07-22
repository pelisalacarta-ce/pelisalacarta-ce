# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mediafire
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data

    if "Invalid or Deleted File" in data:
        return False, "[Mediafire] El archivo no existe o ha sido borrado"
    elif "File Removed for Violation" in data:
        return False, "[Mediafire] Archivo eliminado por infracción"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []

    data = httptools.downloadpage(page_url).data
    patron = 'kNO \= "([^"]+)"'
    matches = re.compile(patron, re.DOTALL).findall(data)
    if len(matches) > 0:
        video_urls.append([matches[0][-4:] + " [mediafire]", matches[0]])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.mediafire.com/download.php?pkpnzadbp2qp893
    # http://www.mediafire.com/?4ckgjozbfid
    # http://www.mediafire.com/file/c0ama0jzxk6pbjl
    # Encontrado en animeflv
    # s=mediafire.com%2F%3F7fsmmq2144fx6t4|-|wupload.com%2Ffile%2F2653904582
    patronvideos = 'mediafire.com(?:/download.php\?|/download/|/file/|/\?|\%2F\%3F)([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = "http://www.mediafire.com/?" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'mediafire'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
