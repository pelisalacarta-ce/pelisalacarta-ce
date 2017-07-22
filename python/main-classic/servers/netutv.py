# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para yaske-netutv, netutv, hqqtv waawtv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re
import urllib

from core import httptools
from core import jsontools
from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    if "hash=" in page_url:
        data = urllib.unquote(httptools.downloadpage(page_url).data)
        id_video = scrapertools.find_single_match(data, "vid\s*=\s*'([^']+)'")
    else:
        id_video = page_url.rsplit("=", 1)[1]
    page_url_hqq = "http://hqq.watch/player/embed_player.php?vid=%s&autoplay=no" % id_video
    data_page_url_hqq = httptools.downloadpage(page_url_hqq, add_referer=True).data

    js_wise = scrapertools.find_single_match(data_page_url_hqq,
                                             "<script type=[\"']text/javascript[\"']>\s*;?(eval.*?)</script>")
    data_unwise = jswise(js_wise).replace("\\", "")
    at = scrapertools.find_single_match(data_unwise, 'var at\s*=\s*"([^"]+)"')
    http_referer = scrapertools.find_single_match(data_unwise, 'var http_referer\s*=\s*"([^"]+)"')

    url = "http://hqq.watch/sec/player/embed_player.php?iss=&vid=%s&at=%s&autoplayed=yes&referer=on" \
          "&http_referer=%s&pass=&embed_from=&need_captcha=0&hash_from=" % (id_video, at, http_referer)
    data_player = httptools.downloadpage(url, add_referer=True).data

    data_unescape = scrapertools.find_multiple_matches(data_player, 'document.write\(unescape\("([^"]+)"')
    data = ""
    for d in data_unescape:
        data += urllib.unquote(d)

    subtitle = scrapertools.find_single_match(data, 'value="sublangs=Spanish.*?sub=([^&]+)&')
    if not subtitle:
        subtitle = scrapertools.find_single_match(data, 'value="sublangs=English.*?sub=([^&]+)&')
    data_unwise_player = ""
    js_wise = scrapertools.find_single_match(data_player,
                                             "<script type=[\"']text/javascript[\"']>\s*;?(eval.*?)</script>")
    if js_wise:
        data_unwise_player = jswise(js_wise).replace("\\", "")

    vars_data = scrapertools.find_single_match(data, '/player/get_md5.php",\s*\{(.*?)\}')
    matches = scrapertools.find_multiple_matches(vars_data, '\s*([^:]+):\s*([^,]*)[,"]')
    params = {}
    for key, value in matches:
        if key == "adb":
            params[key] = "0/"
        elif '"' in value:
            params[key] = value.replace('"', '')
        else:
            value_var = scrapertools.find_single_match(data, 'var\s*%s\s*=\s*"([^"]+)"' % value)
            if not value_var and data_unwise_player:
                value_var = scrapertools.find_single_match(data_unwise_player, 'var\s*%s\s*=\s*"([^"]+)"' % value)
            params[key] = value_var

    params = urllib.urlencode(params)
    head = {'X-Requested-With': 'XMLHttpRequest', 'Referer': url}
    data = httptools.downloadpage("http://hqq.watch/player/get_md5.php?" + params, headers=head).data

    media_urls = []
    url_data = jsontools.load_json(data)
    media_url = tb(url_data["html5_file"].replace("#", ""))

    video_urls = []
    media = media_url + "|User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X)"
    video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [netu.tv]", media, 0, subtitle])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


## Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    ## Patrones
    # http://www.yaske.net/archivos/netu/tv/embed_54b15d2d41641.html
    # http://www.yaske.net/archivos/netu/tv/embed_54b15d2d41641.html?1
    # http://hqq.tv/player/embed_player.php?vid=498OYGN19D65&autoplay=no
    # http://hqq.tv/watch_video.php?v=498OYGN19D65
    # http://netu.tv/player/embed_player.php?vid=82U4BRSOB4UU&autoplay=no
    # http://netu.tv/watch_video.php?v=96WDAAA71A8K
    # http://waaw.tv/player/embed_player.php?vid=82U4BRSOB4UU&autoplay=no
    # http://waaw.tv/watch_video.php?v=96WDAAA71A8K
    patterns = [
        '/netu/tv/(embed_)(.*?$)',
        'hqq.tv/([^=]+)=([a-zA-Z0-9]+)',
        'netu.tv/([^=]+)=([a-zA-Z0-9]+)',
        'waaw.tv/([^=]+)=([a-zA-Z0-9]+)',
        'netu.php\?(nt=)([a-zA-Z0-9]+)',
        'hqq.watch/([^=]+)=([a-zA-Z0-9]+)',
    ]

    url = "http://netu.tv/watch_video.php?v=%s"
    for pattern in patterns:
        logger.info("#" + pattern + "#")
        matches = re.compile(pattern, re.DOTALL).findall(data)
        for prefix, match in matches:
            titulo = "[netu.tv]"
            if "hash.php" in prefix:
                url = "http://hqq.tv/player/hash.php?hash=%s" % match
            else:
                url = url % match
            if url not in encontrados:
                logger.info(" url=" + url)
                devuelve.append([titulo, url, 'netutv'])
                encontrados.add(url)
                break
            else:
                logger.info(" url duplicada=" + url)

    return devuelve


## Obtener la url del m3u8
def tb(b_m3u8_2):
    j = 0
    s2 = ""
    while j < len(b_m3u8_2):
        s2 += "\\u0" + b_m3u8_2[j:(j + 3)]
        j += 3

    return s2.decode('unicode-escape').encode('ASCII', 'ignore')


## --------------------------------------------------------------------------------
## --------------------------------------------------------------------------------

def jswise(wise):
    ## js2python
    def js_wise(wise):

        w, i, s, e = wise

        v0 = 0;
        v1 = 0;
        v2 = 0
        v3 = [];
        v4 = []

        while True:
            if v0 < 5:
                v4.append(w[v0])
            elif v0 < len(w):
                v3.append(w[v0])
            v0 += 1
            if v1 < 5:
                v4.append(i[v1])
            elif v1 < len(i):
                v3.append(i[v1])
            v1 += 1
            if v2 < 5:
                v4.append(s[v2])
            elif v2 < len(s):
                v3.append(s[v2])
            v2 += 1
            if len(w) + len(i) + len(s) + len(e) == len(v3) + len(v4) + len(e): break

        v5 = "".join(v3);
        v6 = "".join(v4)
        v1 = 0
        v7 = []

        for v0 in range(0, len(v3), 2):
            v8 = -1
            if ord(v6[v1]) % 2: v8 = 1
            v7.append(chr(int(v5[v0:v0 + 2], 36) - v8))
            v1 += 1
            if v1 >= len(v4): v1 = 0
        return "".join(v7)

    ## loop2unobfuscated
    while True:
        wise = re.search("var\s.+?\('([^']+)','([^']+)','([^']+)','([^']+)'\)", wise, re.DOTALL)
        if not wise: break
        ret = wise = js_wise(wise.groups())
    return ret
