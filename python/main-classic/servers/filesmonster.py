# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para filesmonster
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("( page_url='%s')")
    video_urls = []
    itemlist = []
    data1 = ''
    data2 = ''
    url = ''
    alerta = '[filesmonster premium]'
    enlace = "no"
    post2 = "username=" + user + "&password=" + password
    login_url = "http://filesmonster.com/api/public/login"
    data1 = scrapertools.cache_page(login_url, post=post2)
    partes1 = data1.split('"')
    estado = partes1[3]
    if estado != 'success': alerta = "[error de filesmonster premium]: " + estado

    id = page_url
    id = id.replace("http://filesmonster.com/download.php", "")
    post = id.replace("?", "")
    url = 'http://filesmonster.com/api/public/premiumDownload'
    data2 = scrapertools.cache_page(url, post=post)

    partes = data2.split('"')

    url = partes[7]
    filename = scrapertools.get_filename_from_url(url)[-4:]
    alerta = filename + " " + alerta
    if "http" not in url: alerta = "[error de filesmonster premium]: " + url

    video_urls.append([alerta, url])

    return video_urls


# Encuentra vÃƒÂ­deos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://uploaz.com/file/
    patronvideos = '"filesmonster.com/download(.*?)"'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[filesmonster]"
        url = "http://filesmonster.com/download" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'filemonster'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
