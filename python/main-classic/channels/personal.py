# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal personal
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import config
from core import logger
from core import scrapertools
from core.item import Item


def mainlist(item):
    return personal_channel(item)

def personal_channel(item):
    logger.info(item.channel)

    itemlist = []
    if item.url=="":
        if item.channel=="personal":
            item.url = config.get_setting("personalchannelurl")
        elif item.channel=="personal2":
            item.url = config.get_setting("personalchannelurl2")
        elif item.channel=="personal3":
            item.url = config.get_setting("personalchannelurl3")
        elif item.channel=="personal4":
            item.url = config.get_setting("personalchannelurl4")
        elif item.channel=="personal5":
            item.url = config.get_setting("personalchannelurl5")
    logger.info("url="+item.url)
    
    # Si es una URL la descarga
    if item.url.startswith("http://") or item.url.startswith("https://"):
        data = scrapertools.cache_page(item.url)

    # Si es un fichero local, lo abre
    else:
        infile = open( item.url )
        data = infile.read()
        infile.close()
    
    # Paginación
    if item.extra=="":
        pagina_a_mostrar = 1
    else:
        pagina_a_mostrar = int(item.extra)
    
    patron = '<item[^<]+<title>([^<]+)</title[^<]+<link([^>]*)>([^<]+)</link[^<]+<description>([^<]+)</description[^<]+<media.thumbnail url="([^"]+)"[^<]+<media.thumbnail url="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    contador = 1
    pagina_actual = 1
    maximo = int(config.get_setting("personalchannelpage"))
    for scrapedtitle,scrapedurltype,scrapedurl,scrapedplot,scrapedthumbnail,fanart in matches:

        # Si está en la página que debe mostrar añade los items
        if pagina_actual == pagina_a_mostrar:

            title = scrapedtitle.strip()
            url = scrapedurl
            thumbnail = scrapedthumbnail
            plot = scrapedplot
            logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

            if scrapedurltype=="":
                itemlist.append( Item(channel=item.channel, action="play" , title=title , fulltitle=title, url=url, thumbnail=thumbnail, fanart=fanart, plot=plot, folder=False))
            else:
                itemlist.append( Item(channel=item.channel, action="personal_channel" , title=title , fulltitle=title, url=url, thumbnail=thumbnail, fanart=fanart, plot=plot, viewmode="movie_with_plot", folder=True))
        
            contador = contador + 1
            if contador > maximo:
                itemlist.append( Item(channel=item.channel, action="personal_channel" , title=">> Página siguiente" , extra=str(pagina_actual+1), viewmode="movie_with_plot", folder=True))
                break

        # Si no está en la página que debe mostrar, simplemente deja pasar el contador
        else:
            contador = contador + 1
            if contador > maximo:
                pagina_actual = pagina_actual + 1
                contador = 1

    if len(itemlist)==0:
        infile = open( url )
        lines = infile.readlines()
        infile.close()

        for data in lines:
            patron = '([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|(.*)$'
            matches = re.compile(patron,re.DOTALL).findall(data)    
        
            for scrapedtitle,scrapedurl,scrapedthumbnail,fanart,scrapedplot in matches:
                title = scrapedtitle.strip()
                url = scrapedurl
                thumbnail = scrapedthumbnail
                plot = scrapedplot
                logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        
                itemlist.append( Item(channel=item.channel, action="play" , title=title , fulltitle=title, url=url, thumbnail=thumbnail, fanart=fanart, plot=plot, folder=False))

    if len(itemlist)==0:
        
        if url=="":
            itemlist.append( Item(title="La configuración no indica dónde está tu canal"))

    return itemlist

def play(item):
    logger.info()

    from core import servertools
    itemlist=servertools.find_video_items(data=item.url)
    for videoitem in itemlist:
        videoitem.channel=item.channel
        videoitem.folder=False
        videoitem.title=item.title
        videoitem.fulltitle=item.title

    if len(itemlist)==0:
        item.server="directo"
        item.folder=False
        itemlist.append( item )

    return itemlist
