# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mail.ru
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import jsontools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    page_url = page_url.replace("embed/", "").replace(".html", ".json")
    data = httptools.downloadpage(page_url).data
    if '"error":"video_not_found"' in data or '"error":"Can\'t find VideoInstance"' in data:
        return False, "[Mail.ru] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % (page_url))

    video_urls = []
    # Carga la página para coger las cookies
    data = httptools.downloadpage(page_url).data

    # Nueva url
    url = page_url.replace("embed/", "").replace(".html", ".json")
    # Carga los datos y los headers
    response = httptools.downloadpage(url)
    data = jsontools.load_json(response.data)

    # La cookie video_key necesaria para poder visonar el video
    cookie_video_key = scrapertools.find_single_match(response.headers["set-cookie"], '(video_key=[a-f0-9]+)')

    # Formar url del video + cookie video_key
    for videos in data['videos']:
        media_url = videos['url'] + "|Referer=https://my1.imgsmail.ru/r/video2/uvpv3.swf?75&Cookie=" + cookie_video_key
        if not media_url.startswith("http"):
            media_url = "http:" + media_url
        quality = " %s" % videos['key']
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + quality + " [mail.ru]", media_url])
    try:
        video_urls.sort(key=lambda video_urls: int(video_urls[0].rsplit(" ", 2)[1][:-1]))
    except:
        pass

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://videoapi.my.mail.ru/videos/embed/mail/bartos1100/_myvideo/1136.html
    patronvideos = '(?:videoapi|api.video).my.mail.ru/(?:videos|video)/embed/(mail|inbox)/([^/]+)/.*?/(\d+).html'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mail.ru]"
        url = "http://videoapi.my.mail.ru/videos/embed/" + match[0] + "/" + match[1] + "/_myvideo/" + match[2] + ".html"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'mailru'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://my.mail.ru/videos/embed/9sadas5d14fe4ae2
    patronvideos = 'my.mail.ru/(?:videos|video)/embed/(?!mail|inbox)([\w]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mail.ru]"
        url = "http://my.mail.ru/+/video/meta/%s" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'mailru'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
