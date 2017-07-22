# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Google video
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import urllib

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    response = httptools.downloadpage(page_url, cookies=False, headers={"Referer": page_url})
    if "no+existe" in response.data:
        return False, "[gvideo] El video no existe o ha sido borrado"
    if "Se+ha+excedido+el" in response.data:
        return False, "[gvideo] Se ha excedido el número de reproducciones permitidas"
	return True, ""


def get_video_url(page_url, user="", password="", video_password=""):
    video_urls = []
    urls = []
    response = httptools.downloadpage(page_url, cookies=False, headers={"Referer": page_url})
    cookies = ""
    cookie = response.headers["set-cookie"].split("HttpOnly, ")
    for c in cookie:
        cookies += c.split(";", 1)[0] + "; "
    data = response.data.decode('unicode-escape')
    data = urllib.unquote_plus(urllib.unquote_plus(data))
    headers_string = "|Cookie=" + cookies
    url_streams = scrapertools.find_single_match(data, 'url_encoded_fmt_stream_map=(.*)')
    streams = scrapertools.find_multiple_matches(url_streams,
                                             'itag=(\d+)&url=(.*?)(?:;.*?quality=.*?(?:,|&)|&quality=.*?(?:,|&))')
    itags = {'18':'360p', '22':'720p', '34':'360p', '35':'480p', '37':'1080p', '43':'360p', '59':'480p'}
    for itag, video_url in streams:
        if not video_url in urls:
            video_url += headers_string
            video_urls.append([itags[itag], video_url])
            urls.append(video_url)
    video_urls.sort(key=lambda video_urls: int(video_urls[0].replace("p", "")))
    return video_urls
