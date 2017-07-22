# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para xvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re

from core import logger
from core import scrapertools


def get_video_url(page_url, video_password):
    video_urls = []
    video_id = scrapertools.get_match(page_url, ".*?video([0-9]+)")
    url = "http://flashservice.xvideos.com/flashservices/gateway.php"
    post = "0003000000010011".decode("hex") + "flashRpc.getVideo" + "0002".decode(
        "hex") + "/1" + "000000190A00000004020008".decode("hex") + video_id + "020000020000020000".decode("hex")
    headers = []
    headers.append(["Content-type", "application/x-amf"])
    headers.append(["Content-length", str(len(post))])

    data = scrapertools.downloadpage(url, post=post, headers=headers)
    try:
        media_url = scrapertools.get_match(data, "(http\://[0-9a-z/_\.]+\.flv\?[0-9a-z&=]+)")
    except:
        post = "0003000000010011".decode("hex") + "flashRpc.getVideo" + "0002".decode(
            "hex") + "/1" + "000000180a00000004020007".decode("hex") + video_id + "020000020000020000".decode("hex")
        data = scrapertools.downloadpage(url, post=post, headers=headers)
        media_url = scrapertools.get_match(data, "(http\://[0-9a-z/_\.]+\.flv\?[0-9a-z&=]+)")

    print   media_url
    video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [xvideos]", media_url])
    return video_urls


def find_videos(data):
    devuelve = []
    patronvideos = 'src="http://flashservice.xvideos.com/embedframe/([0-9]+)" '
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    for match in matches:
        url = "http://www.xvideos.com/video" + match
        titulo = "[xvideos]"
        devuelve.append([titulo, url, 'xvideos'])
    return devuelve
