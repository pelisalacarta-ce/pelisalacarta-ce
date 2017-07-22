# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para streaminto
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    if "File was deleted" in data:
        return False, "El archivo no existe<br/>en streaminto o ha sido borrado."
    elif "Video is processing now" in data:
        return False, "El archivo está siendo procesado<br/>Prueba dentro de un rato."
    else:
        return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = re.sub(r'\n|\t|\s+', '', httptools.downloadpage(page_url).data)

    video_urls = []
    try:
        media_url = scrapertools.get_match(data, """.setup\({file:"([^"]+)",image""")
    except:
        js_data = scrapertools.find_single_match(data, "(eval.function.p,a,c,k,e.*?)</script>")
        js_data = unPack(js_data)
        media_url = scrapertools.get_match(js_data, """.setup\({file:"([^"]+)",image""")

    if media_url.endswith("v.mp4"):
        media_url_mp42flv = re.sub(r'/v.mp4$', '/v.flv', media_url)
        video_urls.append(
            [scrapertools.get_filename_from_url(media_url_mp42flv)[-4:] + " [streaminto]", media_url_mp42flv])
    if media_url.endswith("v.flv"):
        media_url_flv2mp4 = re.sub(r'/v.flv$', '/v.mp4', media_url)
        video_urls.append(
            [scrapertools.get_filename_from_url(media_url_flv2mp4)[-4:] + " [streaminto]", media_url_flv2mp4])
    video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [streaminto]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    encontrados.add("http://streamin.to/embed-theme.html")
    encontrados.add("http://streamin.to/embed-jquery.html")
    encontrados.add("http://streamin.to/embed-s.html")
    encontrados.add("http://streamin.to/embed-images.html")
    encontrados.add("http://streamin.to/embed-faq.html")
    encontrados.add("http://streamin.to/embed-embed.html")
    encontrados.add("http://streamin.to/embed-ri.html")
    encontrados.add("http://streamin.to/embed-d.html")
    encontrados.add("http://streamin.to/embed-css.html")
    encontrados.add("http://streamin.to/embed-js.html")
    encontrados.add("http://streamin.to/embed-player.html")
    encontrados.add("http://streamin.to/embed-cgi.html")
    devuelve = []

    # http://streamin.to/z3nnqbspjyne
    patronvideos = 'streamin.to/([a-z0-9A-Z]+)'
    logger.info(" #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streaminto]"
        url = "http://streamin.to/embed-" + match + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'streaminto'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://streamin.to/embed-z3nnqbspjyne.html
    patronvideos = 'streamin.to/embed-([a-z0-9A-Z]+)'
    logger.info(" #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streaminto]"
        url = "http://streamin.to/embed-" + match + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'streaminto'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve


def unPack(packed):
    pattern = "}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('([^']+)'\)"
    d = [d for d in re.search(pattern, packed, re.DOTALL).groups()]

    p = d[0];
    a = int(d[1]);
    c = int(d[2]);
    k = d[3].split(d[4])

    if a <= 62:
        toString = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        toString = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

    def e(c):
        return toString[c] if c < a else toString[c // a] + toString[c % a]

    while c > 0:
        c -= 1
        if k[c]:
            x = e(c)
        else:
            x = k[c]
        y = k[c]
        p = re.sub(r"(\b%s\b)" % x, y, p)

    return p
