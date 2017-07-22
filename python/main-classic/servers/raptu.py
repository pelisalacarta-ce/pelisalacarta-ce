# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para raptu
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    try:
        response = httptools.downloadpage(page_url)
    except:
        pass

    if not response.data or "urlopen error [Errno 1]" in str(response.code):
        from core import config
        if config.is_xbmc():
            return False, "[Raptu] Este conector solo funciona a partir de Kodi 17"
        elif config.get_platform() == "plex":
            return False, "[Raptu] Este conector no funciona con tu versión de Plex, intenta actualizarla"
        elif config.get_platform() == "mediaserver":
            return False, "[Raptu] Este conector requiere actualizar python a la versión 2.7.9 o superior"

    if "Object not found" in response.data:
        return False, "[Raptu] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    video_urls = []
    #Detección de subtítulos
    subtitulo = ""
    videos = scrapertools.find_multiple_matches(data, '"file"\s*:\s*"([^"]+)","label"\s*:\s*"([^"]+)"')
    for video_url, calidad in videos:
        video_url = video_url.replace("\\", "")
        extension = scrapertools.get_filename_from_url(video_url)[-4:]
        if ".srt" in extension:
            subtitulo = "https://www.raptu.com"+video_url
        else:
            video_urls.append(["%s %s [raptu]" % (extension, calidad), video_url, 0, subtitulo])

    try:
        video_urls.sort(key=lambda it: int(it[0].split("p ", 1)[0].rsplit(" ")[1]))
    except:
        pass
    for video_url in video_urls:
        logger.info(" %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # https://www.raptu.com/?v=ZapZwMMA
    # https://www.raptu.com/embed/ZupZwMML
    # https://www.raptu.com/e/FF8L2P8V26
    patronvideos = 'raptu.com/(?:\?v=|embed/|e/)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[raptu]"
        url = "https://raptu.com/embed/%s" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'raptu'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
