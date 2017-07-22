# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidspot
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    # No existe / borrado: http://vidspot.net/8jcgbrzhujri
    data = scrapertools.cache_page("http://anonymouse.org/cgi-bin/anon-www.cgi/" + page_url)
    if "File Not Found" in data or "Archivo no encontrado" in data or '<b class="err">Deleted' in data \
            or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        return False, "No existe o ha sido borrado de vidspot"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=%s" % page_url)

    # Normaliza la URL
    videoid = scrapertools.get_match(page_url, "http://vidspot.net/([a-z0-9A-Z]+)")
    page_url = "http://vidspot.net/embed-%s-728x400.html" % videoid
    data = scrapertools.cachePage(page_url)
    if "Access denied" in data:
        geobloqueo = True
    else:
        geobloqueo = False

    if geobloqueo:
        url = "http://www.videoproxy.co/hide.php"
        post = "go=%s" % page_url
        location = scrapertools.get_header_from_response(url, post=post, header_to_get="location")
        url = "http://www.videoproxy.co/%s" % location
        data = scrapertools.cachePage(url)

    # Extrae la URL
    media_url = scrapertools.find_single_match(data, '"file" : "([^"]+)",')

    video_urls = []

    if media_url != "":
        if geobloqueo:
            url = "http://www.videoproxy.co/hide.php"
            post = "go=%s" % media_url
            location = scrapertools.get_header_from_response(url, post=post, header_to_get="location")
            media_url = "http://www.videoproxy.co/%s&direct=false" % location
        else:
            media_url += "&direct=false"

        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [vidspot]", media_url])

        for video_url in video_urls:
            logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    encontrados.add("http://vidspot.net/embed-theme.html")
    encontrados.add("http://vidspot.net/embed-jquery.html")
    encontrados.add("http://vidspot.net/embed-s.html")
    encontrados.add("http://vidspot.net/embed-images.html")
    encontrados.add("http://vidspot.net/embed-faq.html")
    encontrados.add("http://vidspot.net/embed-embed.html")
    encontrados.add("http://vidspot.net/embed-ri.html")
    encontrados.add("http://vidspot.net/embed-d.html")
    encontrados.add("http://vidspot.net/embed-css.html")
    encontrados.add("http://vidspot.net/embed-js.html")
    encontrados.add("http://vidspot.net/embed-player.html")
    encontrados.add("http://vidspot.net/embed-cgi.html")
    encontrados.add("http://vidspot.net/embed-i.html")
    encontrados.add("http://vidspot.net/images")
    encontrados.add("http://vidspot.net/theme")
    encontrados.add("http://vidspot.net/xupload")
    encontrados.add("http://vidspot.net/s")
    encontrados.add("http://vidspot.net/js")
    encontrados.add("http://vidspot.net/jquery")
    encontrados.add("http://vidspot.net/login")
    encontrados.add("http://vidspot.net/make")
    encontrados.add("http://vidspot.net/i")
    encontrados.add("http://vidspot.net/faq")
    encontrados.add("http://vidspot.net/tos")
    encontrados.add("http://vidspot.net/premium")
    encontrados.add("http://vidspot.net/checkfiles")
    encontrados.add("http://vidspot.net/privacy")
    encontrados.add("http://vidspot.net/refund")
    encontrados.add("http://vidspot.net/links")
    encontrados.add("http://vidspot.net/contact")

    devuelve = []

    # http://vidspot.net/3sw6tewl21sn
    # http://vidspot.net/embed-3sw6tewl21sn.html
    # http://vidspot.net/embed-3sw6tewl21sn-728x400.html
    # http://www.cinetux.org/video/vidspot.php?id=3sw6tewl21sn
    patronvideos = 'vidspot.(?:net/|php\?id=)(?:embed-|)([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    if len(matches) > 0:
        for match in matches:
            titulo = "[vidspot]"
            url = "http://vidspot.net/" + match
            if url not in encontrados:
                logger.info("  url=" + url)
                devuelve.append([titulo, url, 'vidspot'])
                encontrados.add(url)
            else:
                logger.info("  url duplicada=" + url)

    return devuelve
