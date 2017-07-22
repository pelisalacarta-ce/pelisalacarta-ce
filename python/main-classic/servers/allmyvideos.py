# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allmyvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    # No existe / borrado: http://allmyvideos.net/8jcgbrzhujri
    data = scrapertools.cache_page("http://anonymouse.org/cgi-bin/anon-www.cgi/" + page_url)
    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data or '<b class="err">Deleted' in data \
        or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        return False, "No existe o ha sido borrado de allmyvideos"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=%s" % page_url)

    # Normaliza la URL
    videoid = scrapertools.get_match(page_url, "http://allmyvideos.net/([a-z0-9A-Z]+)")
    page_url = "http://amvtv.net/embed-" + videoid + "-728x400.html"
    data = scrapertools.cachePage(page_url)
    if "Access denied" in data:
        geobloqueo = True
    else:
        geobloqueo = False

    if geobloqueo:
        # url = "http://www.anonymousbrowser.xyz/hide.php"
        # post = "go=%s" % page_url
        url = "http://www.videoproxy.co/hide.php"
        post = "go=%s" % page_url
        location = scrapertools.get_header_from_response(url, post=post, header_to_get="location")
        # url = "http://www.anonymousbrowser.xyz/" + location
        url = "http://www.videoproxy.co/" + location
        data = scrapertools.cachePage(url)

    # Extrae la URL
    media_url = scrapertools.find_single_match(data, '"file" : "([^"]+)",')

    video_urls = []

    if media_url != "":
        if geobloqueo:
            # url = "http://www.anonymousbrowser.xyz/hide.php"
            url = "http://www.videoproxy.co/hide.php"
            post = "go=%s" % media_url
            location = scrapertools.get_header_from_response(url, post=post, header_to_get="location")
            # media_url = "http://www.anonymousbrowser.xyz/" + location + "&direct=false"
            media_url = "http://www.videoproxy.co/" + location + "&direct=false"
        else:
            media_url += "&direct=false"

        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [allmyvideos]", media_url])

        for video_url in video_urls:
            logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    encontrados.add("http://allmyvideos.net/embed-theme.html")
    encontrados.add("http://allmyvideos.net/embed-jquery.html")
    encontrados.add("http://allmyvideos.net/embed-s.html")
    encontrados.add("http://allmyvideos.net/embed-images.html")
    encontrados.add("http://allmyvideos.net/embed-faq.html")
    encontrados.add("http://allmyvideos.net/embed-embed.html")
    encontrados.add("http://allmyvideos.net/embed-ri.html")
    encontrados.add("http://allmyvideos.net/embed-d.html")
    encontrados.add("http://allmyvideos.net/embed-css.html")
    encontrados.add("http://allmyvideos.net/embed-js.html")
    encontrados.add("http://allmyvideos.net/embed-player.html")
    encontrados.add("http://allmyvideos.net/embed-cgi.html")
    encontrados.add("http://allmyvideos.net/embed-i.html")
    encontrados.add("http://allmyvideos.net/images")
    encontrados.add("http://allmyvideos.net/theme")
    encontrados.add("http://allmyvideos.net/xupload")
    encontrados.add("http://allmyvideos.net/s")
    encontrados.add("http://allmyvideos.net/js")
    encontrados.add("http://allmyvideos.net/jquery")
    encontrados.add("http://allmyvideos.net/login")
    encontrados.add("http://allmyvideos.net/make")
    encontrados.add("http://allmyvideos.net/i")
    encontrados.add("http://allmyvideos.net/faq")
    encontrados.add("http://allmyvideos.net/tos")
    encontrados.add("http://allmyvideos.net/premium")
    encontrados.add("http://allmyvideos.net/checkfiles")
    encontrados.add("http://allmyvideos.net/privacy")
    encontrados.add("http://allmyvideos.net/refund")
    encontrados.add("http://allmyvideos.net/links")
    encontrados.add("http://allmyvideos.net/contact")

    devuelve = []

    # http://allmyvideos.net/3sw6tewl21sn
    # http://allmyvideos.net/embed-3sw6tewl21sn.html
    # http://www.cinetux.org/video/allmyvideos.php?id=3sw6tewl21sn
    patronvideos = 'allmyvideos.(?:net/|php\?id=)(?:embed-|)([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    if len(matches) > 0:
        for match in matches:
            titulo = "[allmyvideos]"
            url = "http://allmyvideos.net/" + match
            if url not in encontrados:
                logger.info("  url=" + url)
                devuelve.append([titulo, url, 'allmyvideos'])
                encontrados.add(url)
            else:
                logger.info("  url duplicada=" + url)

    return devuelve
