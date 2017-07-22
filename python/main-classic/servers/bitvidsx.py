# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para bitvidsx ex videoweed
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    if "This video is not yet ready" in data:
        return False, "[Bitvid] El fichero está en proceso todavía o ha sido eliminado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data

    video_urls = []
    videourls = scrapertools.find_multiple_matches(data, 'src\s*:\s*[\'"]([^\'"]+)[\'"]')
    if not videourls:
        videourls = scrapertools.find_multiple_matches(data, '<source src=[\'"]([^\'"]+)[\'"]')
    for videourl in videourls:
        if videourl.endswith(".mpd"):
            id = scrapertools.find_single_match(videourl, '/dash/(.*?)/')
            videourl = "http://www.bitvid.sx/download.php%3Ffile=mm" + "%s.mp4" % id

        videourl = re.sub(r'/dl(\d)*/', '/dl/', videourl)
        ext = scrapertools.get_filename_from_url(videourl)[-4:]
        videourl = videourl.replace("%3F", "?") + \
                   "|User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
        video_urls.append([ext + " [bitvid]", videourl])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    data = data.replace('videoweed.es', 'bitvid.sx')

    patronvideos = '(?:embed.|)bitvid.sx/(?:file/|embed/\?v=)([A-z0-9]{13})'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitvidsx]"
        url = "http://www.bitvid.sx/embed/?v=" + match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'bitvidsx'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # rep="/rep2.php?vw=wuogenrzatq40&t=18&c=13"
    patronvideos = 'src="" rep="([^"]+)" width="([^"]+)" height="([^"]+)"'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[bitvidsx]"
        url = match[0]
        url = url.replace("/rep2.php?vw=", "http://www.bitvid.sx/embed/?v=")

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'bitvidsx'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
