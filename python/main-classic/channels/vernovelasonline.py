# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal de Ver Nnovelas Online
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item

host = "http://ver-novelas-online.com/"

def mainlist(item):
    logger.info()
    itemlist = []
    itemlist.append(Item(channel = item.channel, title = "Ultimos capitulos subidos", action = "capitulos_ultimos", url = host))
    itemlist.append(Item(channel = item.channel, title = "Novelas por letra", action = "novelas_letra", url = host + "video/category/letra-" ))
    itemlist.append(Item(channel = item.channel, title = "Novelas en emision (Sin caratulas)", action = "novelas_emision", url = host))
    itemlist.append(Item(channel = item.channel, title = ""))
    itemlist.append(Item(channel = item.channel, title = "Buscar novela", action = "search", url = host + "?s="))
    return itemlist

def newest(categoria):
    logger.info()
    itemlist = []
    item = Item()
    try:
        item.channel = "vernovelasonline"
        item.extra = "newest"
        item.url = "http://www.ver-novelas-online.com/"
        item.action = "capitulos_ultimos"
        itemlist = capitulos_ultimos(item)
    # Se captura la excepcion, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


def novelas_emision(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = data.replace("\n","")
    block = scrapertools.find_single_match(data, '<aside id="text-2.*?</aside>')
    match = scrapertools.find_multiple_matches(block, 'a href="([^"]+)">([^<]+)')
    for url, titulo in match:
        itemlist.append(Item(channel = item.channel,
        action = "capitulos_de_una_novela",
        title = titulo,
        url = url,
        extra1 = titulo
        ))
    return itemlist

def novelas_letra(item):
    logger.info()
    itemlist = []
    for letra in "abcdefghijklmnopqrstuvwxyz":
        itemlist.append(item.clone(title = letra.upper(), url = item.url+letra, action = "lista"))
    return itemlist


def search(item, texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = "http://ver-novelas-online.com/?s=" + texto
    item.extra = "busca"
    if texto!='':
        return lista(item)
    else:
        return []    


def lista(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = data.replace("\n","")
    accion = "capitulos_de_una_novela"
    patron = """itemprop="url" href="([^"]+)".*?mark">([^<]*)</a>.*?href="([^"]+)"""
    if item.extra == "busca":
        patron = """itemprop="url" href="([^"]+)".*?mark">([^<]*)</a>.*?href='([^']+)"""
        accion = "findvideos"
    matches = scrapertools.find_multiple_matches(data, patron)
    for url, title, thumbnail in matches:
        mtitle = title.replace("CAPITULOS COMPLETOS","").title()
        mextra1 = scrapertools.find_single_match(mtitle, "(?i)(.*?) Capitulo")
        mextra2 = scrapertools.find_single_match(mtitle, "(?i)(cap.*?[0-9]+)").title()
        if mextra1 == "":
            mextra1 = mextra2 = mtitle
        itemlist.append(Item(channel = item.channel,
        action = accion,
        title = mtitle,
        url = url,
        thumbnail = thumbnail,
        fantart = thumbnail,
        plot = "prueba de plot",
        extra1 = mextra1,
        extra2 = mextra2
        ))
    mpagina = scrapertools.find_single_match(data, 'page-numbers" href="([^"]+)')
    pagina = scrapertools.find_single_match(mpagina, "page/([0-9]+)")
    if len(pagina)>0 and "busca" not in item.extra:
        itemlist.append(
                 Item(channel = item.channel,
                 action = "lista",
                 title = "Pagina: "+pagina,
                 url = mpagina,
                 extra = item.extra
                 ))
    return itemlist

def capitulos_ultimos(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = data.replace("\n","")
    patron  = "<div class='item'>.*?<a href='([^']+)"
    patron += ".*?title='([^']+)"
    patron += ".*?img src='([^']+)"
    matches = scrapertools.find_multiple_matches(data,patron)
    for url, title, thumbnail in matches:
        mextra1 = scrapertools.find_single_match(title, "(?i)(.*?) Capitulo")
        mextra2 = scrapertools.find_single_match(title, "(?i)(cap.*?[0-9]+)").title()
        itemlist.append(
               Item(channel = item.channel,
                    action = "findvideos",
                    title = title.title(),
                    url = url,
                    thumbnail = thumbnail,
                    extra1 = mextra1,
                    extra2 = mextra2
                    ))
    mpagina = scrapertools.find_single_match(data, 'next" href="([^"]+)')
    pagina = scrapertools.find_single_match(mpagina, "page/([0-9]+)")
    if "newest" not in item.extra:
        itemlist.append(
                 Item(channel = item.channel,
                 action = "capitulos_ultimos",
                 title = "Pagina: "+pagina,
                 url = mpagina
                 ))
    return itemlist

def capitulos_de_una_novela(item):
    logger.info()
    itemlist = []
    url = item.url
    data = httptools.downloadpage(url).data
    if len(item.thumbnail) == 0:
        item.thumbnail = scrapertools.find_single_match(data, 'og:image" content="([^"]+)' )
    matches = scrapertools.find_multiple_matches(data, '<a target="_blank" href="([^"]+)">([^<]+)')

    for url, titulo in matches:
        mextra2 = scrapertools.find_single_match(titulo,"(?i)(cap.*?[0-9]+)")
        itemlist.append(
              Item(channel = item.channel,
                   action = "findvideos",
                   title = titulo,
                   thumbnail = item.thumbnail,
                   url = url,
                   extra1 = item.extra1,
                   extra2 = mextra2
                   ))
    itemlist.append(Item(channel = item.channel, title = "Novela: [COLOR=blue]" + item.extra1 + "[/COLOR]"))
    # PARA INVERTIR EL ORDEN DE LA LISTA
    itemlist = itemlist[::-1]
    return itemlist

def findvideos(item):
    data = httptools.downloadpage(item.url).data
    data = data.replace("&quot;","").replace("\n","").replace("\\","")
    itemlist = servertools.find_video_items(data = data)
    for video in itemlist:
        video.channel = item.channel
        video.action = "play"
        video.thumbnail = item.thumbnail
        video.fulltitle = item.extra1 + " / " +item.extra2
        video.title = "Ver en: " + video.server
    itemlist.append(Item(channel = item.channel) )
    block = scrapertools.find_single_match(data, '<div class="btn-group-justified">.*?</div>')
    if len(block)>0:
        matches = scrapertools.find_multiple_matches(block, 'href="([^"]+).*?hidden-xs">([^<]+)')
        for url, xs in matches:
            accion = "findvideos"
            capitulo = scrapertools.find_single_match(url, "capitulo-([^/]+)")
            if "DE CAPITULOS" in xs:
                xs = "LISTA" + xs + ": " + item.extra1
                accion = "capitulos_de_una_novela"
            else:
                xs += ": " + capitulo
                capitulo = "Capitulo " + capitulo
            itemlist.append(
                  Item(channel = item.channel,
                  title = "[COLOR=yellow]" + xs.title() + "[/COLOR]",
                  action = accion,
                  url = url,
                  thumbnail = item.thumbnail,
                  extra1 = item.extra1,
                  extra2 = capitulo
                  ))
    else:
        url = scrapertools.find_single_match(data, "<p><a href='(.*?)'\s+style='float:right")
        capitulo = scrapertools.find_single_match(item.extra2, "(?i)capitulo ([^/]+)")
        itemlist.append(
              Item(channel = item.channel,
              title = "[COLOR=yellow]" + "" + "Listado de Capitulos: "+item.extra1.title() +"[/COLOR]",
              action = "capitulos_de_una_novela",
              url = url,
              thumbnail = item.thumbnail,
              extra1 = item.extra1,
              extra2 = capitulo
              ))
    return itemlist
