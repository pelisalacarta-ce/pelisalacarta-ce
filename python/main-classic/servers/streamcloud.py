# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para streamcloud
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("page_url='%s')" % page_url)

    data = scrapertools.cache_page(url=page_url)
    if "<h1>404 Not Found</h1>" in data:
        return False, "El archivo no existe<br/>en streamcloud o ha sido borrado."
    else:
        return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    # Lo pide una vez
    headers = [
        ['User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page(page_url, headers=headers)

    try:
        media_url = scrapertools.get_match(data, 'file\: "([^"]+)"')
    except:
        post = ""
        matches = scrapertools.find_multiple_matches(data, '<input.*?name="([^"]+)".*?value="([^"]*)">')
        for inputname, inputvalue in matches:
            post += inputname + "=" + inputvalue + "&"
        post = post.replace("op=download1", "op=download2")
        data = scrapertools.cache_page(page_url, post=post)

        if 'id="justanotice"' in data:
            logger.info("data=" + data)
            logger.info("Ha saltado el detector de adblock")
            return []

        # Extrae la URL
        media_url = scrapertools.get_match(data, 'file\: "([^"]+)"')

    video_urls = []
    video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [streamcloud]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    devuelve = []

    encontrados = set()
    encontrados.add("http://streamcloud.eu/stylesheets")
    encontrados.add("http://streamcloud.eu/control")
    encontrados.add("http://streamcloud.eu/xupload")
    encontrados.add("http://streamcloud.eu/js")
    encontrados.add("http://streamcloud.eu/favicon")
    encontrados.add("http://streamcloud.eu/reward")
    encontrados.add("http://streamcloud.eu/login")
    encontrados.add("http://streamcloud.eu/deliver")
    encontrados.add("http://streamcloud.eu/faq")
    encontrados.add("http://streamcloud.eu/tos")
    encontrados.add("http://streamcloud.eu/checkfiles")
    encontrados.add("http://streamcloud.eu/contact")
    encontrados.add("http://streamcloud.eu/serve")

    # http://streamcloud.eu/cwvhcluep67i
    patronvideos = '(streamcloud.eu/[a-z0-9]+)'
    logger.info("find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[streamcloud]"
        url = "http://" + match
        if url not in encontrados:
            logger.info("url=" + url)
            devuelve.append([titulo, url, 'streamcloud'])
            encontrados.add(url)
        else:
            logger.info("url duplicada=" + url)

    return devuelve


if __name__ == "__main__":
    import getopt
    import sys

    options, arguments = getopt.getopt(sys.argv[1:], "", ["video_url=", "login=", "password="])

    video_url = ""
    login = ""
    password = ""

    logger.info("%s %s" % (str(options), str(arguments)))

    for option, argument in options:
        print option, argument
        if option == "--video_url":
            video_url = argument
        elif option == "--login":
            login = argument
        elif option == "--password":
            password = argument
        else:
            assert False, "Opcion desconocida"

    if video_url == "":
        print "ejemplo de invocacion"
        print "streamcloud --video_url http://xxx --login usuario --password secreto"
    else:

        if login != "":
            premium = True
        else:
            premium = False

        print get_video_url(video_url, premium, login, password)
