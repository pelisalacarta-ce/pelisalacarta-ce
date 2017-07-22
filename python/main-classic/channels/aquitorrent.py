# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import os
import re
import sys
import unicodedata
import urllib2
import urlparse

import xbmc
import xbmcgui
from core import config
from core import logger
from core import scrapertools
from core.item import Item
from core.scrapertools import decodeHtmlentities as dhe

host = "http://www.aquitorrent.com/"

ACTION_SHOW_FULLSCREEN = 36
ACTION_GESTURE_SWIPE_LEFT = 511
ACTION_SELECT_ITEM = 7
ACTION_PREVIOUS_MENU = 10
ACTION_MOVE_LEFT = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_DOWN = 4
ACTION_MOVE_UP = 3
OPTION_PANEL = 6
OPTIONS_OK = 5

api_key="2e2160006592024ba87ccdf78c28f49f"
api_fankey ="dffe90fba4d02c199ae7a9e71330c987"

def mainlist(item):
    logger.info()

    itemlist = []
    itemlist.append( Item(channel=item.channel, title="Peliculas"      , action="peliculas", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=PELICULAS", thumbnail="http://imgc.allpostersimages.com/images/P-473-488-90/37/3710/L3YAF00Z/posters/conrad-knutsen-cinema.jpg", fanart="http://s6.postimg.org/m8dipognl/aquitorrentfanart2.jpg"))
    itemlist.append( Item(channel=item.channel, action="peliculas", title="Series", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=SERIES", thumbnail="http://s6.postimg.org/nbxn1n1ap/aquitserielogo.jpg", fanart="http://s6.postimg.org/x6os7v58x/aquitorretseries.jpg"))
    itemlist.append( Item(channel=item.channel, action="peliculas", title="Películas HD", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=Peliculas%20HD", thumbnail="http://s6.postimg.org/4uymx2vyp/aquithdlogo.jpg", fanart="http://s6.postimg.org/umxqri72p/aquitphd3.jpg"))
    itemlist.append( Item(channel=item.channel, action="peliculas", title="Películas 3D", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=PELICULAS%203D", thumbnail="http://s6.postimg.org/53rm99jdd/aquit3dlogo.jpg", fanart="http://s6.postimg.org/9i03l3txt/aquit3d.jpg"))
    itemlist.append( Item(channel=item.channel, action="peliculas", title="Películas V.O.S.", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=PELICULAS%20V.O.S.", thumbnail="http://s6.postimg.org/fofbx2s0h/aquitvostub2.jpg", fanart="http://s6.postimg.org/wss1m0aj5/aquitvos.jpg"))
    itemlist.append( Item(channel=item.channel, action="peliculas", title="Docus y TV", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=Docus%20y%20TV",  thumbnail="http://s6.postimg.org/5mnir1w0h/tv_docaquit.jpg", fanart="http://s6.postimg.org/5lrd2uyc1/aquitdoctv3_an.jpg"))
    itemlist.append( Item(channel=item.channel, action="peliculas", title="Clásicos Disney", url="http://www.aquitorrent.com/torr.asp?pagina=1&tipo=CLASICOS%20DISNEY", thumbnail="http://s6.postimg.org/87xosbas1/Walt_Disney.jpg", fanart="http://s6.postimg.org/5m0jucd3l/aquitwalt.jpg"))
    
    itemlist.append( Item(channel=item.channel, action="search", title="Buscar...", url="", thumbnail="http://s6.postimg.org/gninw2o9d/searchaquittub.jpg", fanart="http://s6.postimg.org/b4kpslglt/searchaquit.jpg"))
    
    

    return itemlist


                

def search(item,texto):
    logger.info("texto="+texto)
    texto = texto.replace(" ","+")
    item.url = "http://www.aquitorrent.com/buscar.asp?q=%s" % (texto)
    try:
        
        return buscador(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def buscador(item):
    logger.info()
    
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    #quitamos los titulos de los href en enlaces<
    data = re.sub(r'&/[^"]+">','">',data)

    patron = '<h2 class="post-title entry-title">.*?'
    patron += '<a href=".([^"]+)".*?>'
    patron += '([^<]+)</a>.*?'
    patron += '<img src="([^"]+)".*?'
    patron += '<b>([^"]+)</b>'
    
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedinfo in matches:
        if "Serie" in scrapedurl:
            info_serie =scrapertools.get_match(scrapedtitle,'- (\d+x\d+)')
            info_serie=re.sub(r"FINAL","",info_serie)
            title_fan = scrapertools.get_match(scrapedtitle,'(.*?)-')
            title_fan = title_fan.strip()
        else:
            info_serie=""
            title_fan = scrapedtitle.strip()
        scrapedinfo = scrapedinfo.replace("<br>","-")
        scrapedinfo = scrapedinfo.replace(scrapedinfo,"[COLOR green]"+scrapedinfo+"[/COLOR]")
        scrapedtitle= scrapedtitle.replace(scrapedtitle,"[COLOR white]"+scrapedtitle+"[/COLOR]")
        scrapedtitle = scrapedtitle + " (" + scrapedinfo + ")"
        # Arregla la url y thumbnail
        #scrapedurl = fix_url(scrapedurl)
        scrapedthumbnail = fix_url(scrapedthumbnail)
        
        
        if "tipo=Docus" in item.url :
            action= "findvideos"
        else:
            action = "fanart"
        extra = title_fan+"|"+info_serie
        itemlist.append( Item(channel=item.channel, title =scrapedtitle , url= urlparse.urljoin(host, scrapedurl), action=action, fanart="http://imgur.com/IXzCDF3.jpg", extra=extra,thumbnail=scrapedthumbnail) )

    return itemlist


def peliculas(item):
    logger.info()

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    #quitamos los titulos de los href en enlaces<
    data = re.sub(r'&/[^"]+">','">',data)
    
    
    patron = '<div class="sompret-image">'
    patron += '<a href=".([^"]+)".*?>'
    patron += '<img src="([^"]+)".*?'
    patron += 'title="(.*?) -.*?'
    patron += '<div class="sompret-header">(.*?)</div>.*?'
    patron += '<b>([^"]+)</b>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    
   
    for scrapedurl, scrapedthumbnail, scrapedtitle,scrapedinfoserie, scrapedinfo in matches:
        title_fan= re.sub(r"!|¡","",scrapedtitle)
        title_fan = title_fan.strip()
        info_serie =scrapedinfoserie.strip()
        scrapedinfo = scrapedinfo.replace("<br>","-")
        scrapedinfo = scrapedinfo.replace(scrapedinfo,"[COLOR green]"+scrapedinfo+"[/COLOR]")
        scrapedtitle= scrapedtitle.replace(scrapedtitle,"[COLOR white]"+scrapedtitle+"[/COLOR]")
        if "tipo=SERIES" in item.url:
            scrapedinfoserie= scrapertools.get_match(scrapedinfoserie,'.*?-(.*)')
            scrapedinfoserie = scrapedinfoserie.replace(scrapedinfoserie,"[COLOR yellow]"+scrapedinfoserie+"[/COLOR]")
            scrapedtitle =scrapedtitle + " " + scrapedinfoserie + " " + " (" + scrapedinfo + ")"
        else:
            scrapedtitle = scrapedtitle + " (" + scrapedinfo + ")"
        # Arregla la url y thumbnail
        #scrapedurl = fix_url(scrapedurl)
        scrapedthumbnail = fix_url(scrapedthumbnail)
        
        if "tipo=Docus" in item.url:
            action= "findvideos"
        else:
            action = "fanart"

        extra = title_fan+"|"+info_serie
        itemlist.append( Item(channel=item.channel, title =scrapedtitle , url=urlparse.urljoin(host, scrapedurl), action=action, fanart="http://imgur.com/IXzCDF3.jpg", extra = extra, thumbnail=scrapedthumbnail) )

    ## Paginación
    pagina = int(scrapertools.get_match(item.url,"pagina=(\d+)"))+1
    pagina = "pagina=%s" % (pagina)
    next_page = re.sub(r"pagina=\d+", pagina, item.url)
    title= "[COLOR green]Pagina siguiente>>[/COLOR]"
    if pagina in data:
        itemlist.append( Item(channel=item.channel, title=title, url=next_page, fanart="http://imgur.com/IXzCDF3.jpg", thumbnail="http://s6.postimg.org/4hpbrb13l/texflecha2.png",
            action="peliculas", folder=True) )


    
    return itemlist

def fanart(item):
    logger.info()
    itemlist = []
    url = item.url
    data = scrapertools.cache_page(url)
    data = re.sub(r"\n|\r|\t|\s{2}|\(.*?\)|&nbsp;","",data)
    info_serie =item.extra.split("|")[1]
    title_fan=item.extra.split("|")[0]
    title = re.sub(r"!|¡|,","",title_fan)
    title= title.replace(' ','%20')
    title = ''.join((c for c in unicodedata.normalize('NFD',unicode(title.decode('utf-8'))) if unicodedata.category(c) != 'Mn')).encode("ascii", "ignore")
    try:
      sinopsis=scrapertools.get_match(data,'<span style="text-align: justify;">(.*?)<\/span>')
      if "<br />" in sinopsis:
         sinopsis=scrapertools.get_match(data,'Sinopsis(.*?)<\/span>').strip()
    except:
         sinopsis=""
    
    logger.info("yuuuu")
    logger.info(title)

    year=""
    item.title = re.sub(r"-|\(.*?\)|\d+x\d+","",item.title)
    if not "Series" in item.url:
        if "tipo=CLASICOS" in item.url:
           title = title +"%20Disney"
        urlyear = item.url
        data = scrapertools.cache_page(urlyear)
        try:
            year =scrapertools.get_match(data,'<span style="text-align: justify;">.*?Año.*?(\d\d\d\d)')
        except:
            year = ""
        #filmafinity
        url = "http://www.filmaffinity.com/es/advsearch.php?stext={0}&stype%5B%5D=title&country=&genre=&fromyear={1}&toyear={1}".format(title, year)
        data = scrapertools.downloadpage(url)

        url_filmaf = scrapertools.find_single_match(data, '<div class="mc-poster">\s*<a title="[^"]*" href="([^"]+)"')
        if url_filmaf:
           url_filmaf = "http://www.filmaffinity.com%s" % url_filmaf
           data = scrapertools.downloadpage(url_filmaf)
        else:

               try:
                 url_bing="http://www.bing.com/search?q=%s+%s+site:filmaffinity.com" %  (title.replace(' ', '+'),  year)
                 data = browser (url_bing)
                 data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;','',data)

                 if "myaddrproxy.php" in data:
                     subdata_bing = scrapertools.get_match(data,'li class="b_algo"><div class="b_title"><h2>(<a href="/ myaddrproxy.php/http/www.filmaffinity.com/es/film.*?)"')
                     subdata_bing = re.sub(r'\/myaddrproxy.php\/http\/','',subdata_bing)
                 else:
                     subdata_bing = scrapertools.get_match(data,'li class="b_algo"><h2>(<a href="http://www.filmaffinity.com/es/film.*?)"')
    
                 url_filma = scrapertools.get_match(subdata_bing,'<a href="([^"]+)')
    
                 if not "http" in url_filma:
                    data = scrapertools.cachePage ("http://"+url_filma)
                 else:
                    data = scrapertools.cachePage (url_filma)
                 data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            
               except:
                 pass
        if sinopsis == " ":
           try:
            sinopsis = scrapertools.find_single_match(data, '<dd itemprop="description">(.*?)</dd>')
            sinopsis = sinopsis.replace("<br><br />", "\n")
            sinopsis=re.sub(r"\(FILMAFFINITY\)<br />","",sinopsis)
           except:
              pass
        try:
            rating_filma=scrapertools.get_match(data,'itemprop="ratingValue" content="(.*?)">')
        except:
            rating_filma = "Sin puntuacion"
        
        critica=""
        patron = '<div itemprop="reviewBody">(.*?)</div>.*?itemprop="author">(.*?)\s*<i alt="([^"]+)"'
        matches_reviews = scrapertools.find_multiple_matches(data, patron)

        if matches_reviews:
            for review, autor, valoracion in matches_reviews:
                review = dhe(scrapertools.htmlclean(review))
                review += "\n" + autor +"[CR]"
                review = re.sub(r'Puntuac.*?\)','',review)
                if "positiva" in valoracion:
                    critica += "[COLOR green][B]%s[/B][/COLOR]\n" % review
                elif "neutral" in valoracion:
                    critica += "[COLOR yellow][B]%s[/B][/COLOR]\n" % review
                else:
                    critica += "[COLOR red][B]%s[/B][/COLOR]\n" % review
        else:
             critica = "[COLOR floralwhite][B]Esta película no tiene críticas todavía...[/B][/COLOR]"
        print "ozuu"
        print critica
    
        url="http://api.themoviedb.org/3/search/movie?api_key="+api_key+"&query=" + title +"&year="+year+ "&language=es&include_adult=false"
        data = scrapertools.cachePage(url)
        data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
        patron = '"page":1.*?,"id":(.*?),.*?"backdrop_path":(.*?),"popularity"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        
        if len(matches)==0:
            
                title= re.sub(r":.*|\(.*?\)","",title)
                url="http://api.themoviedb.org/3/search/movie?api_key="+api_key+"&query=" + title + "&language=es&include_adult=false"
                
                data = scrapertools.cachePage(url)
                data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
                patron = '"page":1.*?,"id":(.*?),.*?"backdrop_path":(.*?),"popularity"'
                matches = re.compile(patron,re.DOTALL).findall(data)
                if len(matches)==0:
                    extra=item.thumbnail+"|"+""+"|"+""+"|"+"Sin puntuación"+"|"+rating_filma+"|"+critica
                    show= item.fanart+"|"+""+"|"+sinopsis
                    posterdb = item.thumbnail
                    fanart_info = item.fanart
                    fanart_3 = ""
                    fanart_2 = item.fanart
                    category= item.thumbnail
                    id_scraper=""
                        
                    itemlist.append( Item(channel=item.channel, title=item.title, url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.fanart,extra = extra, show= show, category= category,folder=True) )
    
        for id, fan in matches:
            
            fan = re.sub(r'\\|"','',fan)
            
            try:
                rating = scrapertools.find_single_match(data,'"vote_average":(.*?)}')
            except:
                rating = "Sin puntuación"
            
            id_scraper =id+"|"+"peli"+"|"+rating+"|"+rating_filma+"|"+critica
            try:
                posterdb = scrapertools.get_match(data,'"page":1,.*?"poster_path":"\\\(.*?)"')
                posterdb =  "https://image.tmdb.org/t/p/original" + posterdb
            except:
                posterdb = item.thumbnail

            if "null" in fan:
                fanart = item.fanart
            else:
                fanart="https://image.tmdb.org/t/p/original" + fan
            item.extra= fanart
            
            url ="http://api.themoviedb.org/3/movie/"+id+"/images?api_key="+api_key+""
            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            
            patron = '"backdrops".*?"file_path":".*?",.*?"file_path":"(.*?)",.*?"file_path":"(.*?)",.*?"file_path":"(.*?)"'
            matches = re.compile(patron,re.DOTALL).findall(data)

            if len(matches) == 0:
              patron = '"backdrops".*?"file_path":"(.*?)",.*?"file_path":"(.*?)",.*?"file_path":"(.*?)"'
              matches = re.compile(patron,re.DOTALL).findall(data)
              if len(matches) == 0:
                  fanart_info = item.extra
                  fanart_3 = ""
                  fanart_2 = item.extra
            for fanart_info, fanart_3, fanart_2 in matches:
                fanart_info = "https://image.tmdb.org/t/p/original" + fanart_info
                fanart_3 = "https://image.tmdb.org/t/p/original" + fanart_3
                fanart_2 = "https://image.tmdb.org/t/p/original" + fanart_2
    
            #clearart, fanart_2 y logo
            url ="http://webservice.fanart.tv/v3/movies/"+id+"?api_key="+api_fankey
            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            patron = '"hdmovielogo":.*?"url": "([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
        
            if '"moviedisc"' in data:
                disc = scrapertools.get_match(data,'"moviedisc":.*?"url": "([^"]+)"')
            if '"movieposter"' in data:
                poster = scrapertools.get_match(data,'"movieposter":.*?"url": "([^"]+)"')
            if '"moviethumb"' in data:
                thumb = scrapertools.get_match(data,'"moviethumb":.*?"url": "([^"]+)"')
            if '"moviebanner"' in data:
                banner= scrapertools.get_match(data,'"moviebanner":.*?"url": "([^"]+)"')
        
            if len(matches)==0:
                extra=  posterdb
                #"http://es.seaicons.com/wp-content/uploads/2015/11/Editing-Overview-Pages-1-icon.png"
                show =fanart_2+"|"+fanart_3+"|"+sinopsis
                category = posterdb
                        
                itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=posterdb, fanart=item.extra, extra=extra, show=show, category= category, folder=True) )
            for logo in matches:
                if '"hdmovieclearart"' in data:
                    clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                    if '"moviebackground"' in data:
                    
                        extra=clear
                        show= fanart_2+"|"+fanart_3+"|"+sinopsis
                        if '"moviedisc"' in data:
                            category= disc
                        else:
                            category= clear
                        itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category,folder=True) )
                    else:
                        extra= clear
                        show=fanart_2+"|"+fanart_3+"|"+sinopsis
                        if '"moviedisc"' in data:
                            category= disc
                        else:
                            category= clear
                        itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category, folder=True) )
                                                                                                
                if '"moviebackground"' in data:
                                                                                                    
                    if '"hdmovieclearart"' in data:
                        clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                        extra=clear
                        show= fanart_2+"|"+fanart_3+"|"+sinopsis
                        if '"moviedisc"' in data:
                            category= disc
                        else:
                            category= clear
                    else:
                        extra=logo
                        show= fanart_2+"|"+fanart_3+"|"+sinopsis
                        if '"moviedisc"' in data:
                            category= disc
                        else:
                            category= logo
                                
                        itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show,  category= category, folder=True) )
                                                                                                                                                                    
                                                                                                                                                                    
                                                                                                                                                                    
                                                                                                                                                                    
                if not '"hdmovieclearart"' in data and not '"moviebackground"' in data:
                    extra= logo
                    show=  fanart_2+"|"+fanart_3+"|"+sinopsis
                    if '"moviedisc"' in data:
                        category= disc
                    else:
                        category= item.extra
                    itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show ,  category= category, folder=True) )



    else:
        urlyear = item.url
        data = scrapertools.cache_page(urlyear)
        try:
            year =scrapertools.get_match(data,'<span style="text-align: justify;">.*?Año.*?(\d\d\d\d)')
        except:
              try:
                 year =scrapertools.get_match(data,'SINOPSIS.*? \((\d\d\d\d)')
              except:
                 year = ""
        if year !="":
           url = "http://www.filmaffinity.com/es/advsearch.php?stext={0}&stype%5B%5D=title&country=&ggenre=TV_SE&fromyear={1}&toyear={1}".format(title, year)
           data = scrapertools.downloadpage(url)

           url_filmaf = scrapertools.find_single_match(data, '<div class="mc-poster">\s*<a title="[^"]*" href="([^"]+)"')
           if url_filmaf:
              url_filmaf = "http://www.filmaffinity.com%s" % url_filmaf
              data = scrapertools.downloadpage(url_filmaf)
        
        else:

               try:
                 url_bing="http://www.bing.com/search?q=%s+%s+site:filmaffinity.com" %  (title.replace(' ', '+'),  year)
                 data = browser (url_bing)
                 data = re.sub(r'\n|\r|\t|\s{2}|&nbsp;','',data)

                 if "myaddrproxy.php" in data:
                     subdata_bing = scrapertools.get_match(data,'li class="b_algo"><div class="b_title"><h2>(<a href="/ myaddrproxy.php/http/www.filmaffinity.com/es/film.*?)"')
                     subdata_bing = re.sub(r'\/myaddrproxy.php\/http\/','',subdata_bing)
                 else:
                     subdata_bing = scrapertools.get_match(data,'li class="b_algo"><h2>(<a href="http://www.filmaffinity.com/es/film.*?)"')
    
                 url_filma = scrapertools.get_match(subdata_bing,'<a href="([^"]+)')
                 if not "http" in url_filma:
                    data = scrapertools.cachePage ("http://"+url_filma)
                 else:
                    data = scrapertools.cachePage (url_filma)
                 data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            
               except:
                 pass
        if sinopsis == " ":
           try:
            sinopsis = scrapertools.find_single_match(data, '<dd itemprop="description">(.*?)</dd>')
            sinopsis = sinopsis.replace("<br><br />", "\n")
            sinopsis=re.sub(r"\(FILMAFFINITY\)<br />","",sinopsis)
           except:
              pass
        try:
            rating_filma=scrapertools.get_match(data,'itemprop="ratingValue" content="(.*?)">')
        except:
            rating_filma = "Sin puntuacion"
        print "lobeznito"
        print rating_filma
        
        critica=""
        patron = '<div itemprop="reviewBody">(.*?)</div>.*?itemprop="author">(.*?)\s*<i alt="([^"]+)"'
        matches_reviews = scrapertools.find_multiple_matches(data, patron)

        if matches_reviews:
            for review, autor, valoracion in matches_reviews:
                review = dhe(scrapertools.htmlclean(review))
                review += "\n" + autor +"[CR]"
                review = re.sub(r'Puntuac.*?\)','',review)
                if "positiva" in valoracion:
                    critica += "[COLOR green][B]%s[/B][/COLOR]\n" % review
                elif "neutral" in valoracion:
                    critica += "[COLOR yellow][B]%s[/B][/COLOR]\n" % review
                else:
                    critica += "[COLOR red][B]%s[/B][/COLOR]\n" % review
        else:
             critica = "[COLOR floralwhite][B]Esta serie no tiene críticas[/B][/COLOR]"


        ###Busqueda en tmdb
        
        url_tmdb="http://api.themoviedb.org/3/search/tv?api_key="+api_key+"&query=" + title +"&language=es&include_adult=false&first_air_date_year="+year
        data_tmdb = scrapertools.cachePage(url_tmdb)
        data_tmdb = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data_tmdb)
        patron = '"page":1.*?,"id":(.*?),"backdrop_path":(.*?),"vote_average"'
        matches = re.compile(patron,re.DOTALL).findall(data_tmdb)
        ###Busqueda en bing el id de imdb de la serie
        if len(matches)==0:
         url_tmdb="http://api.themoviedb.org/3/search/tv?api_key="+api_key+"&query=" + title +"&language=es"
         data_tmdb = scrapertools.cachePage(url_tmdb)
         data_tmdb = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data_tmdb)
         patron = '"page":1.*?,"id":(.*?),"backdrop_path":(.*?),"vote_average"'
         matches = re.compile(patron,re.DOTALL).findall(data_tmdb)
         if len(matches)==0:
          urlbing_imdb = "http://www.bing.com/search?q=%s+%s+tv+series+site:imdb.com" % (title.replace(' ', '+'),  year)
          data = browser (urlbing_imdb)
          data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|http://ssl-proxy.my-addr.org/myaddrproxy.php/","",data)
          try:
            subdata_imdb =scrapertools.find_single_match(data,'<li class="b_algo">(.*?)h="ID.*?<strong>.*?TV Series')
          except:
             pass
        
    
          try:
              imdb_id = scrapertools.get_match(subdata_imdb,'<a href=.*?http.*?imdb.com/title/(.*?)/.*?"')
          except:
              imdb_id = ""
          ###Busca id de tvdb y tmdb mediante imdb id
         
          urlremotetbdb = "https://api.themoviedb.org/3/find/"+imdb_id+"?api_key="+api_key+"&external_source=imdb_id&language=es"
          data_tmdb= scrapertools.cachePage(urlremotetbdb)
          matches= scrapertools.find_multiple_matches(data_tmdb,'"tv_results":.*?"id":(.*?),.*?"poster_path":(.*?),"popularity"')
         
          if len(matches)==0:
             id_tmdb=""
             fanart_3 = ""
             extra= item.thumbnail+"|"+year+"|"+"no data"+"|"+"no data"+"|"+rating_filma+"|"+critica+"|"+""+"|"+id_tmdb
             show=  item.fanart+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+item.thumbnail+"|"+id_tmdb
             fanart_info = item.fanart
             fanart_2=item.fanart
             id_scraper = " "+"|"+"serie"+"|"+rating_filma+"|"+critica+"|"+" "
             category= ""
             posterdb= item.thumbnail
             itemlist.append( Item(channel=item.channel, title=item.title, url=item.url, action="findvideos", thumbnail=item.thumbnail, fulltitle=info_serie,fanart=item.fanart ,extra=extra, category= category,  show=show , folder=True) )


        for id_tmdb, fan in matches:
            ###Busca id tvdb
            urlid_tvdb="https://api.themoviedb.org/3/tv/"+id_tmdb+"/external_ids?api_key="+api_key+"&language=es"
            data_tvdb = scrapertools.cachePage(urlid_tvdb)
            id= scrapertools.find_single_match(data_tvdb,'tvdb_id":(.*?),"tvrage_id"')
            if id == "null":
               id = ""
            category = id
            ###Busqueda nºepisodios y temporadas,status
            url_status ="http://api.themoviedb.org/3/tv/"+id_tmdb+"?api_key="+api_key+"&append_to_response=credits&language=es"
            data_status= scrapertools.cachePage(url_status)
            season_episodes=scrapertools.find_single_match(data_status,'"(number_of_episodes":\d+,"number_of_seasons":\d+,)"')
            season_episodes=re.sub(r'"','',season_episodes)
            season_episodes=re.sub(r'number_of_episodes','Episodios ',season_episodes)
            season_episodes=re.sub(r'number_of_seasons','Temporadas',season_episodes)
            season_episodes=re.sub(r'_',' ',season_episodes)
            status = scrapertools.find_single_match(data_status,'"status":"(.*?)"')
            if status== "Ended":
                status ="Finalizada"
            else:
                status = "En emisión"
            status = status +" ("+ season_episodes+")"
            status= re.sub(r',','.',status)
            #######

            fan = re.sub(r'\\|"','',fan)
            try:
             #rating tvdb
             url_rating_tvdb = "http://thetvdb.com/api/1D62F2F90030C444/series/"+id+"/es.xml"
             print "pepote"
             print url_rating_tvdb
             data = scrapertools.cachePage(url_rating_tvdb)
             rating =scrapertools.find_single_match(data,'<Rating>(.*?)<')
            except:
              ratintg_tvdb = ""
              try:
                rating = scrapertools.get_match(data,'"vote_average":(.*?),')
              except:
                
                rating = "Sin puntuación"
         
            id_scraper =id_tmdb+"|"+"serie"+"|"+rating_filma+"|"+critica+"|"+rating+"|"+status #+"|"+emision
            posterdb = scrapertools.find_single_match(data_tmdb,'"poster_path":(.*?)","popularity"')

            if "null" in posterdb:
                posterdb = item.thumbnail
            else:
                posterdb = re.sub(r'\\|"','',posterdb)
                posterdb =  "https://image.tmdb.org/t/p/original" + posterdb
            if "null" in fan:
                fanart = item.fanart
            else:
                fanart="https://image.tmdb.org/t/p/original" + fan

            item.extra= fanart
            
            url ="http://api.themoviedb.org/3/tv/"+id_tmdb+"/images?api_key="+api_key

            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            
            patron = '"backdrops".*?"file_path":".*?",.*?"file_path":"(.*?)",.*?"file_path":"(.*?)",.*?"file_path":"(.*?)"'
            matches = re.compile(patron,re.DOTALL).findall(data)

            if len(matches) == 0:
              patron = '"backdrops".*?"file_path":"(.*?)",.*?"file_path":"(.*?)",.*?"file_path":"(.*?)"'
              matches = re.compile(patron,re.DOTALL).findall(data)
              if len(matches) == 0:
                  fanart_info= item.extra
                  fanart_3 = ""
                  fanart_2 = item.extra
            for fanart_info, fanart_3, fanart_2 in matches:
                fanart_info = "https://image.tmdb.org/t/p/original" + fanart_info
                fanart_3 = "https://image.tmdb.org/t/p/original" + fanart_3
                fanart_2 = "https://image.tmdb.org/t/p/original" + fanart_2
                if fanart== item.fanart:
                    fanart= fanart_info
            url ="http://webservice.fanart.tv/v3/tv/"+id+"?api_key="+api_fankey
            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            patron = '"clearlogo":.*?"url": "([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            if '"tvbanner"' in data:
                tvbanner = scrapertools.get_match(data,'"tvbanner":.*?"url": "([^"]+)"')
                tfv=tvbanner
            elif '"tvposter"' in data:
                tvposter = scrapertools.get_match(data,'"tvposter":.*?"url": "([^"]+)"')
                tfv=tvposter
            else:
                tfv = posterdb
            if '"tvthumb"' in data:
                tvthumb = scrapertools.get_match(data,'"tvthumb":.*?"url": "([^"]+)"')
            if '"hdtvlogo"' in data:
                hdtvlogo = scrapertools.get_match(data,'"hdtvlogo":.*?"url": "([^"]+)"')
            if '"hdclearart"' in data:
                hdtvclear = scrapertools.get_match(data,'"hdclearart":.*?"url": "([^"]+)"')
            if len(matches)==0:
                if '"hdtvlogo"' in data:
                    if "showbackground" in data:
                
                        if '"hdclearart"' in data:
                            thumbnail = hdtvlogo
                            extra=  hdtvclear+"|"+year
                            show = fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                        else:
                            thumbnail = hdtvlogo
                            extra= thumbnail+"|"+year
                            show = fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                        itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, fulltitle=info_serie, thumbnail=thumbnail, fanart=item.extra, category=category, extra=extra, show=show, folder=True) )
                                                                        
                                                                        
                    else:
                        if '"hdclearart"' in data:
                            thumbnail= hdtvlogo
                            extra= hdtvclear+"|"+year
                            show= fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                        else:
                            thumbnail= hdtvlogo
                            extra= thumbnail+"|"+year
                            show= fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                        itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url,fulltitle=info_serie, thumbnail=thumbnail, fanart=item.extra, extra=extra, show=show,  category= category, folder=True) )
                else:
                
                    extra=  ""+"|"+year
                    show = fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                    itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url,  fulltitle=info_serie, thumbnail=posterdb, fanart=fanart, extra=extra, show=show, category = category, folder=True) )
                                                                                                                                
            for logo in matches:
                if '"hdtvlogo"' in data:
                    thumbnail = hdtvlogo
                elif not '"hdtvlogo"' in data :
                        if '"clearlogo"' in data:
                            thumbnail= logo
                else:
                    thumbnail= item.thumbnail
                if '"clearart"' in data:
                    clear=scrapertools.get_match(data,'"clearart":.*?"url": "([^"]+)"')
                    if "showbackground" in data:
                                
                        extra=clear+"|"+year
                        show= fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                        itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, fulltitle=info_serie, thumbnail=thumbnail, fanart=item.extra, extra=extra,show=show, category= category,  folder=True) )
                    else:
                        extra= clear+"|"+year
                        show=fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                        itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, fulltitle=info_serie, thumbnail=thumbnail, fanart=item.extra, extra=extra,show=show, category= category, folder=True) )
                                     
                if "showbackground" in data:
                        
                    if '"clearart"' in data:
                        clear=scrapertools.get_match(data,'"clearart":.*?"url": "([^"]+)"')
                        extra=clear+"|"+year
                        show= fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                    else:
                        extra=logo+"|"+year
                        show= fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                        itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, fulltitle=info_serie, thumbnail=thumbnail, fanart=item.extra, extra=extra,show=show,  category = category, folder=True) )
                                     
                if not '"clearart"' in data and not '"showbackground"' in data:
                        if '"hdclearart"' in data:
                            extra= hdtvclear+"|"+year
                            show= fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                        else:
                            extra= thumbnail+"|"+year
                            show=  fanart_2+"|"+fanart_3+"|"+sinopsis+"|"+title_fan+"|"+tfv+"|"+id_tmdb
                        itemlist.append( Item(channel=item.channel, title = item.title , action="findvideos", url=item.url, fulltitle=info_serie, thumbnail=thumbnail, fanart=item.extra, extra=extra,show=show , category = category, folder=True) )
    title_info ="[COLOR lemonchiffon]Info[/COLOR]"
    if not "Series" in item.url:
       thumbnail = posterdb
    if "Series" in item.url:
        if '"tvposter"' in data:
            thumbnail= scrapertools.get_match(data,'"tvposter":.*?"url": "([^"]+)"')
        else:
            thumbnail = posterdb
        
        if "tvbanner" in data:
            category = tvbanner
        else:
            category = show
        if '"tvthumb"' in data:
            plot = item.plot+"|"+tvthumb
        else:
            plot = item.plot+"|"+item.thumbnail
        if '"tvbanner"' in data:
            plot=plot+"|"+ tvbanner
        elif '"tvthumb"' in data:
            plot=plot+"|"+ tvthumb
        else:
            plot=plot+"|"+ item.thumbnail
    else:
        if '"moviethumb"' in data:
            plot = item.plot+"|"+thumb
        else:
            plot = item.plot+"|"+posterdb

        if '"moviebanner"' in data:
            plot=plot+"|"+ banner
        else:
            if '"hdmovieclearart"' in data:
                plot=plot+"|"+ clear
            
            else:
                plot=plot+"|"+ posterdb

    id = id_scraper

    extra = extra+"|"+id+"|"+title.encode('utf8')

    itemlist.append( Item(channel=item.channel, action="info" , title=title_info ,plot = plot, url=item.url, thumbnail=thumbnail, fanart=fanart_info, extra= extra, category = category, show= show, viewmode="movie_with_plot", folder=False ))

    return itemlist

def findvideos(item):
    logger.info()
    itemlist = []
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    # Torrent en zip
    patron = '<h1 class="post-title entry-title">([^<]+)</h1>.*?</b><br><br>.*?'
    patron+= 'href="(.*?\.zip)".*?'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        for scrapedtitle, scrapedzip in matches:
            # Arregla la url y extrae el torrent
            scrapedtorrent = unzip(fix_url(scrapedzip))
            
            itemlist.append( Item(channel=item.channel, title =item.title+"[COLOR red][B] [magnet][/B][/COLOR]" , url=scrapedtorrent,  action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.extra , folder=False) )


    #Vamos con el normal

    patron = '<h1 class="post-title entry-title">[^<]+</h1>.*?'
    patron+= 'href="(magnet[^"]+)".*?'


    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedmagnet in matches:
        if "Docus" in item.url :
            title_tag="[COLOR yellow][B]Ver--[/B][/COLOR]"
            from unshortenit import unshorten
            url =unshorten(scrapedtorrent)
            url = scrapertools.get_match(str(url),"u'([^']+)'")
            itemlist.append( Item(channel=item.channel, title =title_tag+item.title+"[COLOR red][B] [magnet][/B][/COLOR]" , url=url,  action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.fanart , folder=False) )
        else:
            if "Serie" in item.url:
              temp=scrapertools.get_match(item.fulltitle,'(\d+)x')
              epi=scrapertools.get_match(item.fulltitle,'x(\d+)')
              url_temp= "http://api.themoviedb.org/3/tv/"+item.show.split("|")[5]+"/season/"+temp+"/images?api_key="+api_key+""
              data = scrapertools.cachePage( url_temp )
              data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
              patron = '{"id".*?"file_path":"(.*?)","height"'
              matches = re.compile(patron,re.DOTALL).findall(data)
              if len(matches) == 0:
                 thumbnail= item.thumbnail
              for thumtemp in matches:
                  thumbnail= "https://image.tmdb.org/t/p/original"+ thumtemp
                  title = item.show.split("|")[3]+ " " + temp+"x"+epi
                  title_tag="[COLOR yellow][B]Ver--[/B][/COLOR]"
                  from unshortenit import unshorten
                  url =unshorten(scrapedtorrent)
                  url = scrapertools.get_match(str(url),"u'([^']+)'")
                  itemlist.append( Item(channel=item.channel, title =title_tag+title+"[COLOR red][B] [magnet][/B][/COLOR]" , url=url,  action="play", server="torrent", thumbnail=item.show.split("|")[4], fanart=item.show.split("|")[0] , folder=False) )
              title_info ="    Info"
              title_info = "[COLOR gold]"+title_info+"[/COLOR]"
              itemlist.append( Item(channel=item.channel, action="info_capitulos" , title=title_info , url=item.url, thumbnail=thumbnail, fanart=item.show.split("|")[1], extra =extra,show=item.show,category=item.category, folder=False ))
            else:
                
                 title_tag="[COLOR yellow][B]Ver--[/B][/COLOR]"
                 itemlist.append( Item(channel=item.channel, title =title_tag+item.title+"[COLOR red][B] [magnet][/B][/COLOR]" , url=url,  action="play", server="torrent", thumbnail=item.category, fanart=fanart , folder=False) )
    
    #nueva variacion
    if len(itemlist) == 0:
       patron = '<h1 class="post-title entry-title">[^<]+</h1>.*?<br><br>.*?'
       patron+= 'href="([^"]+)".*?'
       
       matches = re.compile(patron,re.DOTALL).findall(data)
    
       for scrapedtorrent in matches:
           if "Docus" in item.url :
            from unshortenit import unshorten
            url =unshorten(scrapedtorrent)
            url = scrapertools.get_match(str(url),"u'([^']+)'")
            title_tag="[COLOR yellow][B]Ver--[/B][/COLOR]"
            itemlist.append( Item(channel=item.channel, title =title_tag+item.title+"[COLOR red][B] [magnet][/B][/COLOR]" , url=url,  action="play", server="torrent", thumbnail=item.thumbnail, fanart=item.fanart , folder=False) )
           elif "Serie" in item.url:
              temp=scrapertools.get_match(item.fulltitle,'(\d+)x')
              epi=scrapertools.get_match(item.fulltitle,'x(\d+)')
              url_temp= "http://api.themoviedb.org/3/tv/"+item.show.split("|")[5]+"/season/"+temp+"/images?api_key="+api_key+""
              data = scrapertools.cachePage( url_temp )
              data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
              patron = '{"id".*?"file_path":"(.*?)","height"'
              matches = re.compile(patron,re.DOTALL).findall(data)
              if len(matches) == 0 :
                 thumbnail= item.thumbnail
              for thumtemp in matches:
                  thumbnail= "https://image.tmdb.org/t/p/original"+ thumtemp
              title = "[COLOR floralwhite]"+item.show.split("|")[3]+"[/COLOR]"+ " " +"[COLOR snow]"+ temp+"x"+epi+"[/COLOR]"
              title_tag="[COLOR yellow][B]Ver--[/B][/COLOR]"
              from unshortenit import unshorten
              url =unshorten(scrapedtorrent)
              url = scrapertools.get_match(str(url),"u'([^']+)'")
              itemlist.append( Item(channel=item.channel, title =title_tag+title+"[COLOR red][B] [magnet][/B][/COLOR]" , url=url,  action="play", server="torrent", thumbnail=item.show.split("|")[4], fanart=item.show.split("|")[0] , folder=False) )
                  
              extra = item.extra+"|"+temp+"|"+epi
              title_info ="    Info"
              title_info = "[COLOR gold]"+title_info+"[/COLOR]"
              itemlist.append( Item(channel=item.channel, action="info_capitulos" , title=title_info , url=item.url, thumbnail=thumbnail, fanart=item.show.split("|")[1], extra =extra,show=item.show,category=item.category, folder=False ))
           else:
               
               from unshortenit import unshorten
               url =unshorten(scrapedtorrent)
               url = scrapertools.get_match(str(url),"u'([^']+)'")
               title_tag="[COLOR yellow][B]Ver--[/B][/COLOR]"
               itemlist.append( Item(channel=item.channel, title =title_tag+item.title+"[COLOR red][B] [magnet][/B][/COLOR]" , url=url,  action="play", server="torrent", thumbnail=item.category, fanart=item.show.split("|")[0] , folder=False) )
    
    return itemlist


def fix_url(url):
    if url.startswith("/"):
        url = url[1:]
        if not url.startswith("http://"):
            url = host+url
    return url

def unzip(url):
    import zipfile
    itemlist=   []
    # Path para guardar el zip como tem.zip los .torrent extraidos del zip
    torrents_path = config.get_library_path()+'/torrents'
    
    if not os.path.exists(torrents_path):
        os.mkdir(torrents_path)

    ## http://stackoverflow.com/questions/4028697/how-do-i-download-a-zip-file-in-python-using-urllib2
    # Open the url
    try:
        f = urllib2.urlopen(url)
        with open( torrents_path+"/temp.zip", "wb") as local_file:
            local_file.write(f.read())
        
        # Open our local file for writing
        fh = open(torrents_path+"/temp.zip", 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            z.extract(name, torrents_path)
        fh.close()

    #handle errors
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
    try:
       torrent = "file:///"+torrents_path+"/"+name
    except:
        import xbmc, time
        xbmc.executebuiltin( "XBMC.Action(back)" )
        xbmc.sleep(100)
        xbmc.executebuiltin('Notification([COLOR yellow][B]Torrent temporalmente[/B][/COLOR], [COLOR green][B]'+'no disponible'.upper()+'[/B][/COLOR],5000,"http://s6.postimg.org/kta7oe8y9/aquitorrentlogo.png")')

    if not torrents_path.startswith("/"):
        torrents_path = "/"+torrents_path
    try:
       torrent = "file://"+torrents_path+"/"+name

       return torrent
    except:
       return itemlist


def info(item):
    logger.info()
    itemlist = []
    url=item.url
    id = item.extra
    if "Serie" in item.url:
     try:
        rating_tmdba_tvdb=item.extra.split("|")[6]
        if item.extra.split("|")[6]== "":
            rating_tmdba_tvdb= "Sin puntuación"
     except:
          rating_tmdba_tvdb= "Sin puntuación"
    else:
        rating_tmdba_tvdb=item.extra.split("|")[3]
    rating_filma=item.extra.split("|")[4]
    print "eztoquee"
    print rating_filma
    print rating_tmdba_tvdb

    filma="http://s6.postimg.org/6yhe5fgy9/filma.png"

    try:
      if "Series" in item.url:
          title= item.extra.split("|")[8]
      
      else:
         title= item.extra.split("|")[6]
      title = title.replace("%20"," ")
      title = "[COLOR yellow][B]"+title+"[/B][/COLOR]"
    except:
      title = item.title

    try:
       if "." in rating_tmdba_tvdb:
          check_rat_tmdba= scrapertools.get_match(rating_tmdba_tvdb,'(\d+).')
       else:
          check_rat_tmdba=rating_tmdba_tvdb
       if int(check_rat_tmdba) >= 5 and int(check_rat_tmdba) < 8:
          rating = "[COLOR springgreen][B]"+rating_tmdba_tvdb+"[/B][/COLOR]"
       elif int(check_rat_tmdba) >= 8 or rating_tmdba_tvdb == 10:
            rating = "[COLOR yellow][B]"+rating_tmdba_tvdb+"[/B][/COLOR]"
       else:
           rating = "[COLOR crimson][B]"+rating_tmdba_tvdb+"[/B][/COLOR]"
           print "lolaymaue"
    except:
        rating = "[COLOR crimson][B]"+rating_tmdba_tvdb+"[/B][/COLOR]"
    if "10." in rating:
        rating = re.sub(r'10\.\d+','10',rating)
    try:
       check_rat_filma= scrapertools.get_match(rating_filma,'(\d)')
       print "paco"
       print check_rat_filma
       if int(check_rat_filma) >= 5 and int(check_rat_filma) < 8:
          print "dios"
          print check_rat_filma
          rating_filma = "[COLOR springgreen][B]"+rating_filma+"[/B][/COLOR]"
       elif int(check_rat_filma) >=8:
          
          print check_rat_filma
          rating_filma = "[COLOR yellow][B]"+rating_filma+"[/B][/COLOR]"
       else:
          rating_filma = "[COLOR crimson][B]"+rating_filma+"[/B][/COLOR]"
          print "rojo??"
          print check_rat_filma
    except:
          rating_filma = "[COLOR crimson][B]"+rating_filma+"[/B][/COLOR]"



    try:
      if not "Series" in item.url:
        url_plot = "http://api.themoviedb.org/3/movie/"+item.extra.split("|")[1]+"?api_key="+api_key+"&append_to_response=credits&language=es"
        data_plot= scrapertools.cache_page( url_plot )
        plot,tagline = scrapertools.find_single_match(data_plot, '"overview":"(.*?)",.*?"tagline":(".*?")')
        if plot== "":
            plot = item.show.split("|")[2]
        
        plot = "[COLOR moccasin][B]"+plot+"[/B][/COLOR]"
        plot= re.sub(r"\\","",plot)

      else:
        plot = item.show.split("|")[2]
        plot= re.sub(r"\\|<br />|<br/>|:|<script>|</script>","",plot)
        plot = "[COLOR moccasin][B]"+plot+"[/B][/COLOR]"
        
        
        if item.extra.split("|")[7] != "":
           tagline = item.extra.split("|")[7]
           #tagline= re.sub(r',','.',tagline)
        else:
           tagline = ""
    except:
        title = "[COLOR red][B]LO SENTIMOS...[/B][/COLOR]"
        plot = "Esta pelicula no tiene informacion..."
        plot = plot.replace(plot,"[COLOR yellow][B]"+plot+"[/B][/COLOR]")
        photo="http://s6.postimg.org/nm3gk1xox/noinfosup2.png"
        foto ="http://s6.postimg.org/ub7pb76c1/noinfo.png"
        info =""
        
        



    if "Series" in item.url:
        check2="serie"
        icon ="http://s6.postimg.org/hzcjag975/tvdb.png"
        foto= item.show.split("|")[1]
        if foto== item.thumbnail:
            foto = ""
        if item.extra.split("|")[5] !="":
           critica =item.extra.split("|")[5]
        else:
           critica= "Esta serie no tiene críticas..."

        photo= item.extra.split("|")[0].replace(" ","%20")
        if not ".png" in photo:
           photo = ""
        try:
         tagline = "[COLOR aquamarine][B]"+tagline+"[/B][/COLOR]"
        except:
         tagline = ""

    else:
        critica =item.extra.split("|")[5]
        if "%20" in critica:
            critica= "No hay críticas"
        icon ="http://imgur.com/SenkyxF.png"
        
        photo= item.extra.split("|")[0].replace(" ","%20")
        if not ".png" in photo:
           photo = ""
        foto = item.show.split("|")[1]
        if foto== item.thumbnail:
           foto = ""
        try:
         if tagline == "\"\"":
            tagline = " "
        except:
            tagline= " "
        tagline = "[COLOR aquamarine][B]"+tagline+"[/B][/COLOR]"
        check2= "pelicula"
    #Tambien te puede interesar
    peliculas = []
    if "Series" in item.url:
      
      
      url_tpi="http://api.themoviedb.org/3/tv/"+item.show.split("|")[5]+"/recommendations?api_key="+api_key+"&language=es"
      data_tpi=scrapertools.cachePage(url_tpi)
      tpi=scrapertools.find_multiple_matches(data_tpi,'id":(.*?),.*?"original_name":"(.*?)",.*?"poster_path":(.*?),"popularity"')

    else:
      url_tpi="http://api.themoviedb.org/3/movie/"+item.extra.split("|")[1]+"/recommendations?api_key="+api_key+"&language=es"
      data_tpi=scrapertools.cachePage(url_tpi)
      tpi=scrapertools.find_multiple_matches(data_tpi,'id":(.*?),.*?"original_title":"(.*?)",.*?"poster_path":(.*?),"popularity"')

            
    for idp,peli,thumb in tpi:
            
        thumb =re.sub(r'"|}','',thumb)
        if "null" in thumb:
            thumb = "http://s6.postimg.org/tw1vhymj5/noposter.png"
        else:
            thumb ="https://image.tmdb.org/t/p/original"+thumb
        peliculas.append([idp,peli,thumb])
    


    check2 = check2.replace("pelicula", "movie").replace("serie", "tvshow")
    infoLabels = {'title': title, 'plot': plot, 'thumbnail': photo, 'fanart': foto, 'tagline': tagline, 'rating': rating}
    item_info = item.clone(info=infoLabels, icon=icon, extra=id, rating=rating, rating_filma=rating_filma, critica=critica, contentType=check2, thumb_busqueda="http://imgur.com/j7fZpvK.png")
    from channels import infoplus
    infoplus.start(item_info, peliculas)

def info_capitulos(item):
    logger.info()
    
    url= "https://api.themoviedb.org/3/tv/"+item.show.split("|")[5]+"/season/"+item.extra.split("|")[2]+"/episode/"+item.extra.split("|")[3]+"?api_key="+api_key+"&language=es"

    if "/0" in url:
        url = url.replace("/0","/")

    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    patron = '],"name":"(.*?)","overview":"(.*?)".*?"still_path":(.*?),"vote_average":(\d+\.\d).*?,"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    

    if len(matches)==0:

      url="http://thetvdb.com/api/1D62F2F90030C444/series/"+item.category+"/default/"+item.extra.split("|")[2]+"/"+item.extra.split("|")[3]+"/es.xml"
      if "/0" in url:
         url = url.replace("/0","/")
      data = scrapertools.cachePage(url)
      data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
      patron = '<Data>.*?<EpisodeName>([^<]+)</EpisodeName>.*?<Overview>(.*?)</Overview>.*?<Rating>(.*?)</Rating>'
        
      matches = re.compile(patron,re.DOTALL).findall(data)
      
      if len(matches)==0 :
          
          
        title = "[COLOR red][B]LO SENTIMOS...[/B][/COLOR]"
        plot = "Este capitulo no tiene informacion..."
        plot = "[COLOR yellow][B]"+plot+"[/B][/COLOR]"
        image="http://s6.postimg.org/ub7pb76c1/noinfo.png"
        foto="http://s6.postimg.org/nm3gk1xox/noinfosup2.png"
        rating = ""

        
      else:
    
          for name_epi, info,rating in matches:
               if "<filename>episodes" in data:
                   foto = scrapertools.get_match(data,'<Data>.*?<filename>(.*?)</filename>')
                   fanart = "http://thetvdb.com/banners/" + foto
               else:
                   fanart=item.extra.split("|")[1]
               plot = info
               plot = "[COLOR peachpuff][B]"+plot+"[/B][/COLOR]"
               title = name_epi.upper()
               title = "[COLOR bisque][B]"+title+"[/B][/COLOR]"
               image=fanart
               foto= item.extra.split("|")[0]
               if not ".png" in foto:
                  foto="http://imgur.com/yG4hdFe.png"
               foto =re.sub(r'\(.*?\)|" "|" "','',foto)
               foto=re.sub(r' ','',foto)
               try:
           
                  check_rating= scrapertools.get_match(rating,'(\d+).')
           
                  if int(check_rating) >= 5 and int(check_rating) < 8:
                     rating = "Puntuación "+"[COLOR springgreen][B]"+rating+"[/B][/COLOR]"
                  elif int(check_rating) >= 8 and int(check_rating)< 10:
                     rating =  "Puntuación "+"[COLOR yellow][B]"+rating+"[/B][/COLOR]"
                  elif int(check_rating) == 10:
                      rating = "Puntuación "+ "[COLOR orangered][B]"+rating+"[/B][/COLOR]"
                  else:
                      rating = "Puntuación "+ "[COLOR crimson][B]"+rating+"[/B][/COLOR]"

               except:
                     rating = "Puntuación "+ "[COLOR crimson][B]"+rating+"[/B][/COLOR]"
               if "10." in rating:
                    rating = re.sub(r'10\.\d+','10',rating)
    else:
     for name_epi,info,fanart,rating in matches:
        if info =="" or info =="\\":
           info = "Sin informacion del capítulo aún..."
        plot = info
        plot = re.sub(r'/n','',plot)
        plot = "[COLOR peachpuff][B]"+plot+"[/B][/COLOR]"
        title = name_epi.upper()
        title = "[COLOR bisque][B]"+title+"[/B][/COLOR]"
        image=fanart
        image = re.sub(r'"|}','',image)
        if "null" in image:
            image = "http://imgur.com/ZiEAVOD.png"
        else:
            image ="https://image.tmdb.org/t/p/original"+image
        foto= item.extra.split("|")[0]
        if not ".png" in foto:
           foto="http://imgur.com/yG4hdFe.png"
        foto =re.sub(r'\(.*?\)|" "|" "','',foto)
        foto=re.sub(r' ','',foto)
        try:
           
            check_rating= scrapertools.get_match(rating,'(\d+).')
           
            if int(check_rating) >= 5 and int(check_rating) < 8:
               rating = "Puntuación "+"[COLOR springgreen][B]"+rating+"[/B][/COLOR]"
            elif int(check_rating) >= 8 and int(check_rating)< 10:
               rating =  "Puntuación "+"[COLOR yellow][B]"+rating+"[/B][/COLOR]"
            elif int(check_rating) == 10:
               rating = "Puntuación "+ "[COLOR orangered][B]"+rating+"[/B][/COLOR]"
            else:
               rating = "Puntuación "+ "[COLOR crimson][B]"+rating+"[/B][/COLOR]"

        except:
           rating = "Puntuación "+ "[COLOR crimson][B]"+rating+"[/B][/COLOR]"
        if "10." in rating:
              rating = re.sub(r'10\.\d+','10',rating)
    ventana = TextBox2(title=title, plot=plot, thumbnail=image, fanart=foto, rating=rating)
    ventana.doModal()


class TextBox2( xbmcgui.WindowDialog ):
        """ Create a skinned textbox window """
        def __init__( self, *args, **kwargs):
            self.getTitle = kwargs.get('title')
            self.getPlot = kwargs.get('plot')
            self.getThumbnail = kwargs.get('thumbnail')
            self.getFanart = kwargs.get('fanart')
            self.getRating = kwargs.get('rating')
            
            self.background = xbmcgui.ControlImage( 70, 20, 1150, 630, 'http://imgur.com/JbRim10.jpg')
            self.title = xbmcgui.ControlTextBox(120, 60, 430, 50)
            self.rating = xbmcgui.ControlTextBox(145, 112, 1030, 45)
            self.plot = xbmcgui.ControlTextBox( 120, 150, 1056, 100 )
            self.thumbnail = xbmcgui.ControlImage( 120, 300, 1056, 300, self.getThumbnail )
            self.fanart = xbmcgui.ControlImage( 780, 43, 390, 100, self.getFanart )

            self.addControl(self.background)
            self.background.setAnimations([('conditional', 'effect=slide start=1000% end=0% time=2500 condition=true tween=bounce', ),('WindowClose','effect=slide delay=800 start=0% end=1000%  time=800 condition=true',)])
            self.addControl(self.thumbnail)
            self.thumbnail.setAnimations([('conditional', 'effect=zoom  start=0% end=100% delay=2700 time=1500 condition=true tween=elastic easing=inout', ),('WindowClose','effect=slide end=0,700%   time=300 condition=true',)])
            self.addControl(self.plot)
            self.plot.setAnimations([('conditional','effect=zoom delay=2000 center=auto start=0 end=100  time=800  condition=true  ',),('conditional','effect=rotate  delay=2000 center=auto aceleration=6000 start=0% end=360%  time=800  condition=true',),('WindowClose','effect=zoom center=auto start=100% end=-0%  time=600 condition=true',)])
            self.addControl(self.fanart)
            self.fanart.setAnimations([('WindowOpen','effect=slide start=0,-700 delay=1000 time=2500 tween=bounce condition=true',), ('conditional','effect=rotate center=auto  start=0% end=360% delay=3000 time=2500 tween=bounce condition=true',),('WindowClose','effect=slide end=0,-700%  time=1000 condition=true',)])
            self.addControl(self.title)
            self.title.setText( self.getTitle )
            self.title.setAnimations([('conditional', 'effect=slide start=-1500% end=0%  delay=1000 time=2000 condition=true tween=elastic', ),('WindowClose','effect=slide start=0% end=-1500%  time=800 condition=true',)])
            self.addControl(self.rating)
            self.rating.setText( self.getRating )
            self.rating.setAnimations([('conditional','effect=fade start=0% end=100% delay=3000 time=1500 condition=true', ),('WindowClose','effect=slide end=0,-700%  time=600 condition=true',)])
            xbmc.sleep(200)
            
            
            

            try:
                self.plot.autoScroll(7000,6000,30000)
            except:
                
                xbmc.executebuiltin('Notification([COLOR red][B]Actualiza Kodi a su última versión[/B][/COLOR], [COLOR skyblue]para mejor info[/COLOR],8000,"https://raw.githubusercontent.com/linuxserver/docker-templates/master/linuxserver.io/img/kodi-icon.png")')
            self.plot.setText(  self.getPlot )
        
        def get(self):
            self.show()
            
        def onAction(self, action):
            if action == ACTION_PREVIOUS_MENU or action.getId() == ACTION_GESTURE_SWIPE_LEFT or action == 110 or action == 92:
               self.close()
def test():
    return True

#Para la busqueda en bing evitando baneos

def browser(url):
    import mechanize
    
    # Utilizamos Browser mechanize para saltar problemas con la busqueda en bing
    br = mechanize.Browser()
    # Browser options
    br.set_handle_equiv(False)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(False)
    br.set_handle_robots(False)
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    # Want debugging messages?
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)
    
    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16')]
    #br.addheaders =[('Cookie','SRCHD=AF=QBRE; domain=.bing.com; expires=25 de febrero de 2018 13:00:28 GMT+1; MUIDB=3B942052D204686335322894D3086911; domain=www.bing.com;expires=24 de febrero de 2018 13:00:28 GMT+1')]
    # Open some site, let's pick a random one, the first that pops in mind
    r = br.open(url)
    response = r.read()
    print response
    if "img,divreturn" in response:
        r = br.open("http://ssl-proxy.my-addr.org/myaddrproxy.php/"+url)
        print "prooooxy"
        response = r.read()
    
    return response