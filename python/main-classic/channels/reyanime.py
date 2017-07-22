# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para reyanime
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item

ANIMEFLV_REQUEST_HEADERS = []
ANIMEFLV_REQUEST_HEADERS.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0"])
ANIMEFLV_REQUEST_HEADERS.append(["Accept-Encoding","gzip, deflate"])
ANIMEFLV_REQUEST_HEADERS.append(["Cache-Control","max-age=0"])
ANIMEFLV_REQUEST_HEADERS.append(["Connection","keep-alive"])
ANIMEFLV_REQUEST_HEADERS.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
ANIMEFLV_REQUEST_HEADERS.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])


def mainlist(item):
    logger.info()

    itemlist = []
    itemlist.append( Item(channel=item.channel, action="series"       , title="En emisión"           , url="http://reyanime.com/ver/emision" , viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="letras"       , title="Por orden alfabético" , url="http://reyanime.com/ver/lista-numeros" ))
    itemlist.append( Item(channel=item.channel, action="generos"      , title="Por géneros"          , url="http://reyanime.com/ver/genero/accion" ))
    itemlist.append( Item(channel=item.channel, action="series"       , title="Últimos agregados"    , url="http://reyanime.com/ver/ultimos" , viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="series"       , title="Proximamente"         , url="http://reyanime.com/ver/proximamente" , viewmode="movie_with_plot"))
  
    return itemlist

def letras(item):
    logger.info()

    itemlist = []
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<div class="alfabeto">(.*?)</div>')
    patron = '<a href="([^"]+)[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.entityunescape(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=item.channel, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot, viewmode="movie_with_plot"))
    return itemlist

def generos(item):
    logger.info()

    itemlist = []
    #itemlist.append( Item(channel=item.channel, action="series" , title="acción" , url="http://reyanime.com/ver/genero/accion", viewmode="movie_with_plot"))

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div class="lista-hoja-genero-2"(.*?)</div>')
    logger.info("data="+data)
    patron = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.entityunescape(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=item.channel, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot, viewmode="movie_with_plot"))
    return itemlist

def series(item):
    logger.info()

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)

    # Extrae las entradas 
    '''
    <a href="/anime/akane-iro-ni-somaru-saka/">
    <div class="anim-list">
    <div id="a49"  class="anim-sinop-estilos-iz">
    <div class="anim-sinopsis-dos-iz">
    <div class="anim-list-genr-iz">

    comedia
    , 

    drama
    , 

    ecchi
    , 

    recuentos de la vida
    , 

    romance


    </div>
    <div class="line-title"></div>
    Juunichi es un joven estudiante con una vida escolar muy normal junto a sus amigos y amigas en la escuela. Sin embargo, cierto día, una chica nueva llega transferida a su salón y se presenta como su &quot;prometida&quot;. Juunichi, que no sabe nada de esto, discute con ella acerca de lo que ha dicho y, fin...
    </div><div class="anim-sinopsis-uno-iz"></div>
    </div>

    <!-- test -->
    <img onmousemove="MM_showHideLayers('a49','','show')" onmouseout="MM_showHideLayers('a49','','hide')" src="/media/cache/8e/e0/8ee04c67c17286efb07a771d48beae76.jpg" width="131" height="" class="img-til"/>

    <div onmousemove="MM_showHideLayers('a49','','show')" onmouseout="MM_showHideLayers('a49','','hide')" class="anime-titulo">
    Akane Iro Ni Somaru Saka
    </div>
    </div>
    </a>

    '''

    patron  = '(<a href="[^"]+"[^<]+'
    patron += '<span[^<]+</span[^<]+'
    patron += '<div id="[^<]+<div[^<]+</div[^<]+<h5.*?</a)'

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        scrapedurl = scrapertools.find_single_match(match,'<a href="([^"]+)"')
        scrapedplot = scrapertools.find_single_match(match,'</h6>([^<]+)</div>')
        scrapedthumbnail = scrapertools.find_single_match(match,'src="([^"]+)"')
        scrapedtitle = scrapertools.find_single_match(match,'<spa[^>]+>([^<]+)</spa')

        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapertools.htmlclean(scrapedplot).strip()
        show = title
        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=item.channel, action="episodios", title=title , url=url , thumbnail=thumbnail , plot=plot , show=show, fulltitle=title, fanart=thumbnail, viewmode="movies_with_plot", folder=True) )

    next_page = scrapertools.find_single_match(data,'<a href="([^"]+)" class="next">siguiente >>')
    if next_page!="":
        itemlist.append( Item(channel=item.channel, action="series", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page, viewmode="movie_with_plot") , folder=True) )

    return itemlist

def episodios(item):
    logger.info()
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<div id="box-cap"(.*?)</div>')

    # <a title="active-raid-kidou-kyoushuushitsu-dai-hakkei-12" href="/active-raid-kidou-kyoushuushitsu-dai-hakkei-12/"><b>12</b>
    patron = 'href="([^"]+).*?<b>([^<]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        
        try:
            if len(title)==1:
                title = "1x0"+title
            else:
                title = "1x"+title
        except:
            pass
        
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = item.thumbnail
        plot = item.plot
        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , show=item.show, fulltitle=item.show+" "+title, fanart=thumbnail, folder=True) )

    if config.get_library_support():
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )
        itemlist.append( Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info()
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,"<!--reproductor-->(.*?)<!--!reproductor-->")

    patron = '<iframe src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for page_url in matches:
        logger.info("page_url="+page_url)
        servercode = scrapertools.find_single_match(page_url,'http.//ozhe.larata.in/repro-rc/([^\?]+)')
        logger.info("servercode="+servercode)
        #videoid = scrapertools.find_single_match(page_url,'http://ypfserviclubs.org/repro-rc/[a-z0-9]+\?v\=(.*?)$')
        servername = servercode_to_name(servercode)
        logger.info("servername="+servername)
        #page_url = build_video_url(servername,videoid)

        title = "Ver en "+servername
        itemlist.append( Item(channel=item.channel, action="play", title=title , url=page_url , folder=False) )

    return itemlist

def play(item):
    logger.info()
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)

    listavideos = servertools.findvideos(data)
    for video in listavideos:
        scrapedtitle = item.title+video[0]
        videourl = video[1]
        server = video[2]
        logger.debug("title=["+scrapedtitle+"], url=["+videourl+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=item.channel, action="play", title=scrapedtitle , fulltitle=item.fulltitle, url=videourl , server=server , folder=False) )
    
    return itemlist

def servercode_to_name(servercode):

    '''
    <div class="tabitem" id="vid1"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/amz?v=x3-WAC3XSk4qXWYNNdBtew" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid7"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/shared?v=2e1y6c6ukc?s=l" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid9"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/bam?v=wjYuC" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid10"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/copy?v=VBgxq7HZ7R6k" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid11"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/zipy?v=76.zippyshare.com/v/67769071/file.html" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid12"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/picasa?v=Ybjw5qMf9lEqKjOpNOYO49MTjNZETYmyPJy0liipFm0" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid13"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/vidweed?v=f8e3938b6dedc" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid14"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/shared?v=4ga8g1h402?s=l" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid15"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/vk?v=227799401%26id=169242565%26hash=b6330a77dea8ff0d%26sd" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid16"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/nov?v=ecde7e432d2e2" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid17"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/nowv?v=4c1d0bf33eda3" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid18"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/mbam?v=wjYuC" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid19"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/mvk?v=227799401%26id=169242565%26hash=b6330a77dea8ff0d%26sd" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    <div class="tabitem" id="vid20"  style="display: block; height: 100%;"><iframe src="http://ypfserviclubs.org/repro-rc/mnov?v=ecde7e432d2e2" width="100%" height="100%" frameborder="0" scrolling="no"></iframe></div>';
    '''

    if servercode=="amzcl":
        servername = "amazon"

    elif servercode=="shared":
        servername="sharedcom"
    elif servercode=="daily":
        servername="dailymotion"
    elif servercode=="bam":
        servername="videobam"
    elif servercode=="copy":
        servername="copycom"
    elif servercode=="zipy":
        servername="zippyshare"
    elif servercode=="picasa":
        servername="picasa"
    elif servercode=="vidweed":
        servername="videoweed"
    elif servercode=="shared":
        servername="sharedcom"
    elif servercode=="mrut":
        servername="rutube"
    elif servercode=="rut":
        servername="rutube"
    elif servercode=="vk":
        servername="vk"
    elif servercode=="nov":
        servername="novamov"
    elif servercode=="nowv":
        servername="nowvideo"
    elif servercode=="mbam":
        servername="videobam"
    elif servercode=="mvk":
        servername="vk"
    elif servercode=="mnov":
        servername="novamov"
    else:
        servername=servercode

    return servername
