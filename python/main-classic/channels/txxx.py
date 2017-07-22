# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para PelisPlanet
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import sys
import urllib
import urlparse

from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item
from core import channeltools

__channel__ = "txxx"

host = 'http://www.txxx.com'

try:
    __modo_grafico__ = config.get_setting('modo_grafico', __channel__)
    __perfil__ = int(config.get_setting('perfil', __channel__))
except:
    __modo_grafico__ = True
    __perfil__ = 0

# Fijar perfil de color
perfil = [['0xFF6E2802', '0xFFFAA171', '0xFFE9D7940'],
          ['0xFFA5F6AF', '0xFF5FDA6D', '0xFF11811E'],
          ['0xFF58D3F7', '0xFF2E64FE', '0xFF0404B4']]

if __perfil__ - 1 >= 0:
    color1, color2, color3 = perfil[__perfil__-1]
else:
    color1 = color2 = color3 = ""

headers = [['User-Agent', 'Mozilla/50.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'],
           ['Referer', host]]

thumbnail = 'https://raw.githubusercontent.com/Inter95/tvguia/master/thumbnails/adults/%s.png'

def mainlist(item):
    logger.info()

    itemlist = []

    itemlist.append(Item(channel=__channel__, title="Últimas",
                         url=host+'/latest-updates/', action="peliculas",
                         viewmode="movie_with_plot", thumbnail = thumbnail % '1'))

    itemlist.append(Item(channel=__channel__, title="Mejor Valoradas", url=host +
                         '/top-rated/', action="peliculas", viewmode="movie_with_plot",
                         thumbnail = thumbnail % '2'))

    itemlist.append(Item(channel=__channel__, title="Más Populares", url=host +
                         '/most-popular/', action="peliculas", viewmode="movie_with_plot",
                         thumbnail = thumbnail % '3'))

    itemlist.append(Item(channel=__channel__, title="Categorías", action="categorias",
                         url=host + '/categories/', viewmode="movie_with_plot",
                         thumbnail = thumbnail % '4'))

    itemlist.append(Item(channel=__channel__, title="Modelos", action="pornstars",
                         url=host + '/models/', viewmode="movie_with_plot",
                         thumbnail = thumbnail % '6'))

    itemlist.append(Item(channel=__channel__, title="Buscador", action="search",
                         url=host, thumbnail = thumbnail % '5'))

    return itemlist


def peliculas(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)

    patron = 'data-video-id="[^"]+"><div class="un-grid--thumb--content"><a href="([^"]+)".*?' #url
    patron += '<img src="([^"]+)" alt="([^"]+)".*?' #img and title
    patron += '<div class="thumb__duration">([^<]+)</div>' #time
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scarpedtime in matches:
            title = "[%s] - %s" % (scarpedtime, scrapedtitle)

            itemlist.append(item.clone(channel=item.channel, action="play", title=title,
                                       url=scrapedurl, thumbnail=scrapedthumbnail, plot="",
                                       viewmode="movie_with_plot", folder=True))

    # Extrae el paginador                              <a class="btn btn--size--l" href="([^"]+)" title="Page \d+">
    paginacion = scrapertools.find_single_match(data, '<a class=" btn btn--size--l btn--next" href="([^"]+)"')
    paginacion = urlparse.urljoin(item.url, paginacion)

    if paginacion:
        itemlist.append(Item(channel=item.channel, action="peliculas",
                             title="\xc2\xbb Siguiente \xc2\xbb", url=paginacion,
                             thumbnail = thumbnail % 'rarrow'))

    return itemlist


def categorias(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)

    patron = '<div class="c-thumb"><a href="([^"]+)" title="([^"]+)".*?' #url and title
    patron += '<img src="([^"]+)" alt="([^"]+)".*?' #img and plot
    patron += '<div class="c-thumb--overlay c-thumb--overlay-video">.*?<span>([^<]+)</span></div>' #img and plot
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail, plot, vids in matches:
        vids = vids.replace(' ', ',')
        title = "%s (%s)" % (scrapedtitle, vids)
        thumbnail = scrapedthumbnail
        url = scrapedurl
        itemlist.append(Item(channel=item.channel, action="peliculas", fanart=scrapedthumbnail, title=title,
                             url=url, thumbnail=thumbnail, plot=plot,
                             viewmode="movie_with_plot", folder=True))

    return itemlist



def search(item, texto):
    logger.info()

    texto = texto.replace(" ", "+")
    item.url = urlparse.urljoin(item.url, "/search/?s={0}".format(texto))

    try:
        return sub_search(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []


def sub_search(item):
    logger.info()

    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)

    patron = 'data-video-id="[^"]+"><div class="un-grid--thumb--content"><a href="([^"]+)".*?' #url
    patron += '<img src="([^"]+)" alt="([^"]+)"/>.*?' #img and title
    patron += '<div class="thumb__duration">([^<]+)</div>' #time
    matches = scrapertools.find_multiple_matches(data, patron)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scarpedtime in matches:
        title = "[%s] - %s" % (scarpedtime, scrapedtitle)
        itemlist.append(item.clone(title=title, url=scrapedurl, action="play", thumbnail=scrapedthumbnail))

    paginacion = scrapertools.find_single_match(data, '<a class=" btn btn--size--l btn--next" href="([^"]+)"')
    paginacion = urlparse.urljoin(item.url, paginacion)

    if paginacion:
        itemlist.append(Item(channel=item.channel, action="sub_search", title="\xc2\xbb Siguiente \xc2\xbb",
                             url=paginacion, thumbnail = thumbnail % 'rarrow'))

    return itemlist


def pornstars(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)

    patron = '<div class="m_thumb">.*?'
    patron += '<span>([^<]+)</span>.*?' # videos
    patron += '<a href="([^"]+)".*?' # url
    patron += '<img src="([^"]+)".*?' # img
    patron += '<div class="m_thumb--title">([^<]+)</div>' # title

    matches = re.compile(patron, re.DOTALL).findall(data)

    for vids, scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        title = '%s (%s Videos)' % (scrapedtitle, vids)
        thumbnail = scrapedthumbnail
        url = scrapedurl

        itemlist.append(Item(channel=item.channel, action="peliculas", title=title, url=host + url,
                             thumbnail=thumbnail, plot="", viewmode="movie_with_plot", folder=True))

    paginacion = scrapertools.find_single_match(data, '<a class=" btn btn--size--l btn--next" href="([^"]+)"')
    paginacion = urlparse.urljoin(item.url, paginacion)

    if paginacion:
        itemlist.append(Item(channel=item.channel, action="pornstars", title="\xc2\xbb Siguiente \xc2\xbb", url=paginacion,
                             thumbnail="https://raw.githubusercontent.com/Inter95/tvguia/master/thumbnails/adults/rarrow.png",
                             ))

    return itemlist


def play(item):
    logger.info()
    itemlist=[]
    data = scrapertools.downloadpage(item.url)
    url= scrapertools.get_match(data,"label': '','file': '([^']+)','type': \"hls\",'default': true" )
    itemlist.append( Item(channel=item.channel, action="play", server="directo", title=item.title , url=url , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    return itemlist
