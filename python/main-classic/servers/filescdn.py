# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Conector para FilesCDN por Hernan_Ar_c
# ------------------------------------------------------------

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data

    if "File was deleted" in data:
        return False, "[FilesCDN] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    video_urls = []
    data = httptools.downloadpage(page_url).data
    url = scrapertools.find_single_match(data, '(?i)link:\s*"(https://.*?filescdn\.com.*?mp4)"')
    url = url.replace(':443', '')
    video_urls.append(['filescdn', url])

    return video_urls


def find_videos(page_url):
    encontrados = set()
    devuelve = []
    titulo = "[filescdn]"
    url = scrapertools.find_single_match(page_url,
                                         '((?:(?:http:\/\/|https:\/\/)filescdn\.com\/(?:embed-.*?\.html|[a-zA-Z0-9]+)))')
    if len(url) > 0 and url not in encontrados:
        logger.info("  url=" + url)
        devuelve.append([titulo, url, 'filescdn'])
        encontrados.add(url)
        logger.info("  url duplicada=" + url)

    return devuelve
