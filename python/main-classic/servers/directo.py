# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vídeos directos (urls simples)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re

from core import logger


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    video_urls = [["%s [directo]" % page_url[-4:], page_url]]

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # mysites.com
    patronvideos = "(http://[a-zA-Z0-9]+\.mysites\.com\/get_file\/.*?\.mp4)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Directo]"
        url = match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'directo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = 'flashvars="file=(http://[^\.]+.myspacecdn[^\&]+)&'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'Directo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = '(http://[^\.]+\.myspacecdn.*?\.flv)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'Directo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = '(http://api.ning.com.*?\.flv)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'Directo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # file=http://es.video.netlogstatic.com//v/oo/004/398/4398830.flv&
    # http://es.video.netlogstatic.com//v/oo/004/398/4398830.flv
    patronvideos = "file\=(http\:\/\/es.video.netlogstatic[^\&]+)\&"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Directo]"
        url = match

        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'directo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    patronvideos = "file=http.*?mangaid.com(.*?)&amp;backcolor="
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)
    cont = 0
    for match in matches:
        cont = cont + 1
        titulo = " Parte %s [Directo]" % (cont)
        url = "http://mangaid.com" + match
        url = url.replace('%2F', '/').replace('%3F', '?').replace('%23', '#')
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'directo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://peliculasid.net/plugins/rip-google.php?id=8dpjvXV7bq05QjAnl93yu9MTjNZETYmyPJy0liipFm0#.mp4
    patronvideos = "so\.addVariable\(\’file\’,\’(http\://peliculasid[^\']+)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)
    cont = 0
    for match in matches:
        cont = cont + 1
        titulo = "[Directo]" % (cont)
        url = match
        url = url.replace('%2F', '/').replace('%3F', '?').replace('%23', '#')
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'directo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
