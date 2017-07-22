# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para elitetorrent
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re
import urlparse

from core import logger
from core import scrapertools
from core.item import Item

BASE_URL = 'http://www.elitetorrent.net'


def mainlist(item):
    logger.info()

    itemlist = []
    itemlist.append( Item(channel=item.channel, title="Docus y TV"     , action="peliculas", url="http://www.elitetorrent.net/categoria/6/docus-y-tv/modo:mini", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Estrenos"       , action="peliculas", url="http://www.elitetorrent.net/categoria/1/estrenos/modo:mini", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Películas"      , action="peliculas", url="http://www.elitetorrent.net/categoria/2/peliculas/modo:mini", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Peliculas HDRip", action="peliculas", url="http://www.elitetorrent.net/categoria/13/peliculas-hdrip/modo:mini", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Peliculas MicroHD", action="peliculas", url="http://www.elitetorrent.net/categoria/17/peliculas-microhd/modo:mini", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Peliculas VOSE" , action="peliculas", url="http://www.elitetorrent.net/categoria/14/peliculas-vose/modo:mini", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Series"         , action="peliculas", url="http://www.elitetorrent.net/categoria/4/series/modo:mini", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, title="Series VOSE"    , action="peliculas", url="http://www.elitetorrent.net/categoria/16/series-vose/modo:mini", viewmode="movie_with_plot"))

    return itemlist

def peliculas(item):
    logger.info()
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    if "http://www.bajui.com/redi.php" in data:
        data = scrapertools.cache_page(item.url)

    '''
    <li>
    <a href="/torrent/23471/mandela-microhd-720p"><img src="thumb_fichas/23471.jpg" border="0" title="Mandela (microHD - 720p)" alt="IMG: Mandela (microHD - 720p)"/></a>
    <div class="meta">
    <a class="nombre" href="/torrent/23471/mandela-microhd-720p" title="Mandela (microHD - 720p)">Mandela (microHD - 720p)</a>
    <span class="categoria">Peliculas microHD</span>
    <span class="fecha">Hace 2 sem</span>
    <span class="descrip">Título: Mandela: Del mito al hombre<br />
    '''
    patron =  '<a href="(/torrent/[^"]+)">'
    patron += '<img src="(thumb_fichas/[^"]+)" border="0" title="([^"]+)"[^>]+></a>'
    patron += '.*?<span class="descrip">(.*?)</span>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(BASE_URL, scrapedurl)
        thumbnail = urlparse.urljoin(BASE_URL, scrapedthumbnail)
        plot = re.sub('<[^<]+?>', '', scrapedplot)
        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=item.channel, action="play", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=False) )

    # Extrae el paginador
    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">Siguiente \&raquo\;</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=item.channel, action="peliculas", title="Página siguiente >>" , url=scrapedurl , folder=True, viewmode="movie_with_plot") )

    return itemlist

def play(item):
    logger.info()
    itemlist = []

    data = scrapertools.cache_page(item.url)
    if "http://www.bajui.com/redi.php" in data:
        data = scrapertools.cache_page(item.url)

    #<a href="magnet:?xt=urn:btih:d6wtseg33iisp7jexpl44wfcqh7zzjuh&amp;dn=Abraham+Lincoln+Cazador+de+vampiros+%28HDRip%29+%28EliteTorrent.net%29&amp;tr=http://tracker.torrentbay.to:6969/announce" class="enlace_torrent degradado1">Descargar por magnet link</a> 
    link = scrapertools.get_match(data,'<a href="(magnet[^"]+)" class="enlace_torrent[^>]+>Descargar por magnet link</a>')
    link = urlparse.urljoin(item.url,link)
    logger.info("link="+link)

    itemlist.append( Item(channel=item.channel, action="play", server="torrent", title=item.title , url=link , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    return itemlist
