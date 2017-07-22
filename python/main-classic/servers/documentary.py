# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para documentary.es
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url)

    try:
        # var videoVars = {"videoNonceVar":"94767795ce","post_id":"2835"};
        videoNonceVar = scrapertools.get_match(data,
                                               'var\s*videoVars\s*\=\s*\{"videoNonceVar"\:"([^"]+)","post_id"\:"\d+"')
        post_id = scrapertools.get_match(data, 'var\s*videoVars\s*\=\s*\{"videoNonceVar"\:"[^"]+","post_id"\:"(\d+)"')

        # http://documentary.es/wp-admin/admin-ajax.php?postId=2835&videoNonce=94767795ce&action=getVideo&_=1385893877929
        import random
        url = "http://documentary.es/wp-admin/admin-ajax.php?postId=" + post_id + "&videoNonce=" + videoNonceVar + "&action=getVideo&_=" + str(
            random.randint(10000000000, 9999999999999))
        data = scrapertools.cache_page(url)

        # {"videoUrl":"http:\/\/www.dailymotion.com\/embed\/video\/xioggh?autoplay=1&defaultSubtitle=es"}
        data = data.replace("\\", "")
    except:
        pass

    from core import servertools
    real_urls = servertools.find_video_items(data=data)
    if len(real_urls) > 0:
        item = real_urls[len(real_urls) - 1]
        servermodule = __import__('servers.%s' % item.server, None, None, ["servers.%s" % item.server])
        # exec "import " + item.server
        # exec "servermodule = " + item.server
        video_urls = servermodule.get_video_url(item.url)

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # <iframe src="http://documentary.es/2321-mundos-invisibles-1x02-mas-alla-de-nuestra-vision-720p?embed"
    patronvideos = 'http://documentary.es/(\d+[a-z0-9\-]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[documentary.es]"
        url = "http://documentary.es/" + match + "?embed"
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'documentary'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
