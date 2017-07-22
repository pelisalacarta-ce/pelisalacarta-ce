# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidabc
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

from core.scrapertools import logger, get_match, find_multiple_matches
from core.httptools import downloadpage

host = "http://vidabc.com"
id_server = "vidabc"

def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = downloadpage(page_url).data
    if "Video is processing now" in data:
        return False, "[vidabc] El archivo se está procesando"
    if "File was deleted" in data:
        return False, "[vidabc] El archivo ha sido borrado"
    return True, ""

def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = downloadpage(page_url).data

    try:
        sources = get_match(data, 'sources\s*:\s* \[([^\]]+)\]')
    except:
        try: from core import jsunpack
        except: from lib import jsunpack
        sources = jsunpack.unpack(get_match(data, '<script[^>]*>(eval.function.p,a,c,k,e,.*?)</script>'))
        sources = get_match(sources, 'sources\s*:\s*\[([^\]]+)\]')

    video_urls = []
    for media_url in find_multiple_matches(sources, '"([^"]+)"'):
        if media_url.endswith(".mp4"):
            video_urls.append([".mp4 [%s]" % id_server, media_url])

        if media_url.endswith(".m3u8"):
            video_urls.append(["M3U8 [%s]" % id_server, media_url])

        if media_url.endswith(".smil"):
            smil_data = downloadpage(media_url).data

            rtmp = get_match(smil_data, 'base="([^"]+)"')
            playpaths = find_multiple_matches(smil_data, 'src="([^"]+)" height="(\d+)"')

            for playpath, inf in playpaths:
                h = get_match(playpath, 'h=([a-z0-9]+)')
                video_urls.append(["RTMP [%s] %s" % (id_server, inf), "%s playpath=%s" % (rtmp, playpath)])

    for video_url in video_urls:
        logger.info("video_url: %s - %s" % (video_url[0], video_url[1]))

    return video_urls

def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://vidabc.com/3unqlhu5en58.html
    # http://vidabc.com/embed-3unqlhu5en58.html
    patronvideos  = "%s.com/(?:embed-|)([a-z0-9]+)" % id_server
    logger.info("[%s.py] find_videos #" % id_server + patronvideos + "#")

    matches = find_multiple_matches(text, patronvideos)

    for match in matches:
        titulo = "[%s]" % id_server
        url = host + "/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, id_server])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
