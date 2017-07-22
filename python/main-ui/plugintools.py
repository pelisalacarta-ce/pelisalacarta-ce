# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Plugin Tools
# Copyright 2015 tvalacarta@gmail.com
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
#------------------------------------------------------------
# This file is part of Plugin Tools.
#
# Plugin Tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelisalacarta 4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pelisalacarta 4.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------
# Plugin Tools v1.1.1
#---------------------------------------------------------------------------
# Based on code from youtube, parsedom and pelisalacarta addons
# Author: 
# Jesús (tvalacarta@gmail.com)
# http://www.mimediacenter.info/plugintools
#---------------------------------------------------------------------------
# Changelog:
# 1.0.0
# - First release
# 1.0.1
# - If find_single_match can't find anything, it returns an empty string
# - Remove addon id from this module, so it remains clean
# 1.0.2
# - Added parameter on "add_item" to say that item is playable
# 1.0.3
# - Added direct play
# - Fixed bug when video isPlayable=True
# 1.0.4
# - Added get_temp_path, get_runtime_path, get_data_path
# - Added get_setting, set_setting, open_settings_dialog and get_localized_string
# - Added keyboard_input
# - Added message
# 1.0.5
# - Added read_body_and_headers for advanced http handling
# - Added show_picture for picture addons support
# - Added optional parameters "title" and "hidden" to keyboard_input
# 1.0.6
# - Added fanart, show, episode and infolabels to add_item
# 1.0.7
# - Added set_view function
# 1.0.8
# - Added selector
# 1.0.9
# - Added unescape and htmlclean functions
# - Added as comments different view modes used in different skins
# - Fix small problem in add_item, fanart were not passed as parameter to next action
# - Added flag for disable application logs
# 1.1.0
# - Add slugify
# - Add context menu options to add_item
# - Add download function
# - Add application log control
# 1.1.1
# - Added show_notification
# - Bug fixes
# 1.1.2
# - Added readfile
#---------------------------------------------------------------------------

import xbmc
import xbmcplugin
import xbmcaddon
import xbmcgui

import urllib
import urllib2
import re
import sys
import os
import time
import socket
from StringIO import StringIO
import gzip

application_log_enabled = False
module_log_enabled = False
http_debug_log_enabled = False

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
OTHER = "other"

'''
Known codes

    Confluence

        Normal
            CommonRootView: 50 # List
            ThumbnailView: 500 # Thumbnail
            WideIconView: 505
            FullWidthList: 51 # Big list

        Biblioteca
            PosterWrapView: 501 # Poster Wrap
            PosterWrapView2_Fanart: 508 # Fanart
            MediaListView2: 504 # Media info
            MediaListView3: 503 # Media info 2
            MediaListView4: 515 # Media info 3
'''

# Suggested view codes for each type from different skins (initial list thanks to xbmcswift2 library)
ALL_VIEW_CODES = {
    'list': {
        'skin.confluence': 50, # List
        'skin.aeon.nox': 50, # List
        'skin.droid': 50, # List
        'skin.quartz': 50, # List
        'skin.re-touched': 50, # List
    },
    'thumbnail': {
        'skin.confluence': 500, # Thumbnail
        'skin.aeon.nox': 500, # Wall
        'skin.droid': 51, # Big icons
        'skin.quartz': 51, # Big icons
        'skin.re-touched': 500, #Thumbnail
    },
    'movies': {
        'skin.confluence': 515, # 500 Thumbnail # 515 Media Info 3
        'skin.aeon.nox': 500, # Wall
        'skin.droid': 51, # Big icons
        'skin.quartz': 52, # Media info
        'skin.re-touched': 500, #Thumbnail
    },
    'tvshows': {
        'skin.confluence': 515, # 500 Thumbnail # 515 Media Info 3
        'skin.aeon.nox': 500, # Wall
        'skin.droid': 51, # Big icons
        'skin.quartz': 52, # Media info
        'skin.re-touched': 500, #Thumbnail
    },
    'seasons': {
        'skin.confluence': 50, # List
        'skin.aeon.nox': 50, # List
        'skin.droid': 50, # List
        'skin.quartz': 52, # Media info
        'skin.re-touched': 50, # List
    },
    'episodes': {
        'skin.confluence': 504, # Media Info
        'skin.aeon.nox': 518, # Infopanel
        'skin.droid': 50, # List
        'skin.quartz': 52, # Media info
        'skin.re-touched': 550, # Wide
    },
}

# Write something on XBMC log
def log(message):
    if application_log_enabled:
        xbmc.log(message, xbmc.LOGNOTICE)

# Write this module messages on XBMC log
def _log(message):
    if module_log_enabled:
        xbmc.log("plugintools."+message, xbmc.LOGNOTICE)

# Parse XBMC params - based on script.module.parsedom addon    
def get_params():
    _log("get_params")
    
    param_string = sys.argv[2]
    
    _log("get_params "+str(param_string))
    
    commands = {}

    if param_string:
        split_commands = param_string[param_string.find('?') + 1:].split('&')
    
        for command in split_commands:
            _log("get_params command="+str(command))
            if len(command) > 0:
                if "=" in command:
                    split_command = command.split('=')
                    key = split_command[0]
                    value = urllib.unquote_plus(split_command[1])
                    commands[key] = value
                else:
                    commands[command] = ""
    
    _log("get_params "+repr(commands))
    return commands

# Fetch text content from an URL
def read(url):
    _log("read "+url)

    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    
    return data

def readfile(path):
    _log("readfile "+path)

    f = open(path)
    data = f.read()
    f.close()
    
    return data

def read_body_and_headers(url, post=None, headers=[], follow_redirects=False, timeout=30):
    _log("read_body_and_headers "+url)

    if post is not None:
        _log("read_body_and_headers post="+post)

    if len(headers)==0:
        headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0"])

    # Start cookie lib
    ficherocookies = os.path.join( get_data_path(), 'cookies.dat' )
    _log("read_body_and_headers cookies_file="+ficherocookies)

    cj = None
    ClientCookie = None
    cookielib = None

    # Let's see if cookielib is available
    try:
        _log("read_body_and_headers importing cookielib")
        import cookielib
    except ImportError:
        _log("read_body_and_headers cookielib no disponible")
        # If importing cookielib fails
        # let's try ClientCookie
        try:
            _log("read_body_and_headers importing ClientCookie")
            import ClientCookie
        except ImportError:
            _log("read_body_and_headers ClientCookie not available")
            # ClientCookie isn't available either
            urlopen = urllib2.urlopen
            Request = urllib2.Request
        else:
            _log("read_body_and_headers ClientCookie available")
            # imported ClientCookie
            urlopen = ClientCookie.urlopen
            Request = ClientCookie.Request
            cj = ClientCookie.MozillaCookieJar()

    else:
        _log("read_body_and_headers cookielib available")
        # importing cookielib worked
        urlopen = urllib2.urlopen
        Request = urllib2.Request
        cj = cookielib.MozillaCookieJar()
        # This is a subclass of FileCookieJar
        # that has useful load and save methods

    if cj is not None:
    # we successfully imported
    # one of the two cookie handling modules
        _log("read_body_and_headers Cookies enabled")

        if os.path.isfile(ficherocookies):
            _log("read_body_and_headers Reading cookie file")
            # if we have a cookie file already saved
            # then load the cookies into the Cookie Jar
            try:
                cj.load(ficherocookies, ignore_discard=True)
            except:
                _log("read_body_and_headers Wrong cookie file, deleting...")
                os.remove(ficherocookies)

        # Now we need to get our Cookie Jar
        # installed in the opener;
        # for fetching URLs
        if cookielib is not None:
            _log("read_body_and_headers opener using urllib2 (cookielib)")
            # if we use cookielib
            # then we get the HTTPCookieProcessor
            # and install the opener in urllib2
            if not follow_redirects:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=http_debug_log_enabled),urllib2.HTTPCookieProcessor(cj),NoRedirectHandler())
            else:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=http_debug_log_enabled),urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)

        else:
            _log("read_body_and_headers opener using ClientCookie")
            # if we use ClientCookie
            # then we get the HTTPCookieProcessor
            # and install the opener in ClientCookie
            opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
            ClientCookie.install_opener(opener)

    # -------------------------------------------------
    # Cookies instaladas, lanza la petición
    # -------------------------------------------------

    # Contador
    inicio = time.clock()

    # Diccionario para las cabeceras
    txheaders = {}

    # Construye el request
    if post is None:
        _log("read_body_and_headers GET request")
    else:
        _log("read_body_and_headers POST request")
    
    # Añade las cabeceras
    _log("read_body_and_headers ---------------------------")
    for header in headers:
        _log("read_body_and_headers header %s=%s" % (str(header[0]),str(header[1])) )
        txheaders[header[0]]=header[1]
    _log("read_body_and_headers ---------------------------")

    req = Request(url, post, txheaders)
    if timeout is None:
        handle=urlopen(req)
    else:        
        #Disponible en python 2.6 en adelante --> handle = urlopen(req, timeout=timeout)
        #Para todas las versiones:
        try:
            import socket
            deftimeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout)
            handle=urlopen(req)            
            socket.setdefaulttimeout(deftimeout)
        except:
            import sys
            for line in sys.exc_info():
                _log( "%s" % line )
    
    # Actualiza el almacén de cookies
    cj.save(ficherocookies, ignore_discard=True)

    # Lee los datos y cierra
    if handle.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( handle.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data=handle.read()

    info = handle.info()
    _log("read_body_and_headers Response")

    returnheaders=[]
    _log("read_body_and_headers ---------------------------")
    for header in info:
        _log("read_body_and_headers "+header+"="+info[header])
        returnheaders.append([header,info[header]])
    handle.close()
    _log("read_body_and_headers ---------------------------")

    '''
    # Lanza la petición
    try:
        response = urllib2.urlopen(req)
    # Si falla la repite sustituyendo caracteres especiales
    except:
        req = urllib2.Request(url.replace(" ","%20"))
    
        # Añade las cabeceras
        for header in headers:
            req.add_header(header[0],header[1])

        response = urllib2.urlopen(req)
    '''
    
    # Tiempo transcurrido
    fin = time.clock()
    _log("read_body_and_headers Downloaded in %d seconds " % (fin-inicio+1))
    _log("read_body_and_headers body="+data)

    return data,returnheaders

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

# Parse string and extracts multiple matches using regular expressions
def find_multiple_matches(text,pattern):
    _log("find_multiple_matches pattern="+pattern)
    
    matches = re.findall(pattern,text,re.DOTALL)

    return matches

# Parse string and extracts first match as a string
def find_single_match(text,pattern):
    _log("find_single_match pattern="+pattern)

    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result

def add_item( action="" , title="" , plot="" , url="" , thumbnail="" , fanart="" , show="" , episode="" , extra="", category="", page="", info_labels = None, context_menu_items = [] , isPlayable = False , folder=True ):
    _log("add_item action=["+action+"] title=["+title+"] url=["+url+"] thumbnail=["+thumbnail+"] fanart=["+fanart+"] show=["+show+"] episode=["+episode+"] extra=["+extra+"] category=["+category+"] page=["+page+"] isPlayable=["+str(isPlayable)+"] folder=["+str(folder)+"]")

    listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
    if info_labels is None:
        info_labels = { "Title" : title, "FileName" : title, "Plot" : plot }
    listitem.setInfo( "video", info_labels )

    if len(context_menu_items)>0:
        listitem.addContextMenuItems ( context_menu_items, replaceItems=False)

    if fanart!="":
        listitem.setProperty('fanart_image',fanart)
        xbmcplugin.setPluginFanart(int(sys.argv[1]), fanart)
    
    if url.startswith("plugin://"):
        itemurl = url
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
    elif isPlayable:
        listitem.setProperty("Video", "true")
        listitem.setProperty('IsPlayable', 'true')
        itemurl = '%s?action=%s&title=%s&url=%s&thumbnail=%s&fanart=%s&plot=%s&extra=%s&category=%s&page=%s' % ( sys.argv[ 0 ] , action , urllib.quote_plus( title ) , urllib.quote_plus(url) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( fanart ) , urllib.quote_plus( plot ) , urllib.quote_plus( extra ) , urllib.quote_plus( category ) , urllib.quote_plus( page ))
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
    else:
        itemurl = '%s?action=%s&title=%s&url=%s&thumbnail=%s&fanart=%s&plot=%s&extra=%s&category=%s&page=%s' % ( sys.argv[ 0 ] , action , urllib.quote_plus( title ) , urllib.quote_plus(url) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( fanart ) , urllib.quote_plus( plot ) , urllib.quote_plus( extra ) , urllib.quote_plus( category ) , urllib.quote_plus( page ))
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)

def close_item_list():
    _log("close_item_list")

    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)

def play_resolved_url(url):
    _log("play_resolved_url ["+url+"]")

    listitem = xbmcgui.ListItem(path=url)
    listitem.setProperty('IsPlayable', 'true')
    return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def direct_play(url):
    _log("direct_play ["+url+"]")

    title = ""

    try:
        xlistitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", path=url)
    except:
        xlistitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", )
    xlistitem.setInfo( "video", { "Title": title } )

    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()
    playlist.add( url, xlistitem )

    player_type = xbmc.PLAYER_CORE_AUTO
    xbmcPlayer = xbmc.Player( player_type )
    xbmcPlayer.play(playlist)

def show_picture(url):

    local_folder = os.path.join(get_data_path(),"images")
    if not os.path.exists(local_folder):
        try:
            os.mkdir(local_folder)
        except:
            pass
    local_file = os.path.join(local_folder,"temp.jpg")

    # Download picture
    urllib.urlretrieve(url, local_file)
    
    # Show picture
    xbmc.executebuiltin( "SlideShow("+local_folder+")" )

def get_temp_path():
    _log("get_temp_path")

    dev = xbmc.translatePath( "special://temp/" )
    _log("get_temp_path ->'"+str(dev)+"'")

    return dev

def get_runtime_path():
    _log("get_runtime_path")

    dev = xbmc.translatePath( __settings__.getAddonInfo('Path') )
    _log("get_runtime_path ->'"+str(dev)+"'")

    return dev

def get_data_path():
    _log("get_data_path")

    dev = xbmc.translatePath( __settings__.getAddonInfo('Profile') )
    
    # Parche para XBMC4XBOX
    if not os.path.exists(dev):
        os.makedirs(dev)

    _log("get_data_path ->'"+str(dev)+"'")

    return dev

def get_setting(name):
    _log("get_setting name='"+name+"'")

    dev = __settings__.getSetting( name )

    _log("get_setting ->'"+str(dev)+"'")

    if dev == "true":
        return True
    elif dev == "false":
        return False
    else:
        try:
            dev = int(dev)
        except ValueError:
            pass

        return dev


def set_setting(name,value):
    _log("set_setting name='"+name+"','"+value+"'")

    if isinstance(value, bool):
        if value:
            value = "true"
        else:
            value = "false"
    elif isinstance(value, (int, long)):
        value = str(value)

    __settings__.setSetting( name,value )


def open_settings_dialog():
    _log("open_settings_dialog")

    __settings__.openSettings()

def get_localized_string(code):
    _log("get_localized_string code="+str(code))

    dev = __language__(code)

    try:
        dev = dev.encode("utf-8")
    except:
        pass

    _log("get_localized_string ->'"+dev+"'")

    return dev

def keyboard_input(default_text="", title="", hidden=False):
    _log("keyboard_input default_text='"+default_text+"'")

    keyboard = xbmc.Keyboard(default_text,title,hidden)
    keyboard.doModal()
    
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
    else:
        tecleado = ""

    _log("keyboard_input ->'"+tecleado+"'")

    return tecleado

def message(text1, text2="", text3=""):
    _log("message text1='"+text1+"', text2='"+text2+"', text3='"+text3+"'")

    if text3=="":
        xbmcgui.Dialog().ok( text1 , text2 )
    elif text2=="":
        xbmcgui.Dialog().ok( "" , text1 )
    else:
        xbmcgui.Dialog().ok( text1 , text2 , text3 )

def message_yes_no(text1, text2="", text3=""):
    _log("message_yes_no text1='"+text1+"', text2='"+text2+"', text3='"+text3+"'")

    if text3=="":
        yes_pressed = xbmcgui.Dialog().yesno( text1 , text2 )
    elif text2=="":
        yes_pressed = xbmcgui.Dialog().yesno( "" , text1 )
    else:
        yes_pressed = xbmcgui.Dialog().yesno( text1 , text2 , text3 )

    return yes_pressed

def selector(option_list,title="Select one"):
    _log("selector title='"+title+"', options="+repr(option_list))

    dia = xbmcgui.Dialog()
    selection = dia.select(title,option_list)

    return selection

def set_view(view_mode, view_code=0):
    _log("set_view view_mode='"+view_mode+"', view_code="+str(view_code))

    # Set the content for extended library views if needed
    if view_mode==MOVIES:
        _log("set_view content is movies")
        xbmcplugin.setContent( int(sys.argv[1]) ,"movies" )
    elif view_mode==TV_SHOWS:
        _log("set_view content is tvshows")
        xbmcplugin.setContent( int(sys.argv[1]) ,"tvshows" )
    elif view_mode==SEASONS:
        _log("set_view content is seasons")
        xbmcplugin.setContent( int(sys.argv[1]) ,"seasons" )
    elif view_mode==EPISODES:
        _log("set_view content is episodes")
        xbmcplugin.setContent( int(sys.argv[1]) ,"episodes" )

    # Reads skin name
    skin_name = xbmc.getSkinDir()
    _log("set_view skin_name='"+skin_name+"'")

    try:
        if view_code==0:
            _log("set_view view mode is "+view_mode)
            view_codes = ALL_VIEW_CODES.get(view_mode)
            view_code = view_codes.get(skin_name)
            _log("set_view view code for "+view_mode+" in "+skin_name+" is "+str(view_code))
            xbmc.executebuiltin("Container.SetViewMode("+str(view_code)+")")
        else:
            _log("set_view view code forced to "+str(view_code))
            xbmc.executebuiltin("Container.SetViewMode("+str(view_code)+")")
    except:
        _log("Unable to find view code for view mode "+str(view_mode)+" and skin "+skin_name)


def unescape(text):
    """Removes HTML or XML character references 
       and entities from a text string.
       keep &amp;, &gt;, &lt; in the source code.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":   
                    return unichr(int(text[3:-1], 16)).encode("utf-8")
                else:
                    return unichr(int(text[2:-1])).encode("utf-8")
                  
            except ValueError:
                logger.info("error de valor")
                pass
        else:
            # named entity
            try:
                '''
                if text[1:-1] == "amp":
                    text = "&amp;amp;"
                elif text[1:-1] == "gt":
                    text = "&amp;gt;"
                elif text[1:-1] == "lt":
                    text = "&amp;lt;"
                else:
                    print text[1:-1]
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode("utf-8")
                '''
                import htmlentitydefs
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode("utf-8")
            except KeyError:
                logger.info("keyerror")
                pass
            except:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def htmlclean(cadena):
    cadena = cadena.replace("<center>","")
    cadena = cadena.replace("</center>","")
    cadena = cadena.replace("<cite>","")
    cadena = cadena.replace("</cite>","")
    cadena = cadena.replace("<em>","")
    cadena = cadena.replace("</em>","")
    cadena = cadena.replace("<b>","")
    cadena = cadena.replace("</b>","")
    cadena = cadena.replace("<u>","")
    cadena = cadena.replace("</u>","")
    cadena = cadena.replace("<li>","")
    cadena = cadena.replace("</li>","")
    cadena = cadena.replace("<tbody>","")
    cadena = cadena.replace("</tbody>","")
    cadena = cadena.replace("<tr>","")
    cadena = cadena.replace("</tr>","")
    cadena = cadena.replace("<![CDATA[","")
    cadena = cadena.replace("<Br />","")
    cadena = cadena.replace("<BR />","")
    cadena = cadena.replace("<Br>","")

    cadena = re.compile("<script.*?</script>",re.DOTALL).sub("",cadena)

    cadena = re.compile("<option[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</option>","")

    cadena = re.compile("<i[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</iframe>","")
    cadena = cadena.replace("</i>","")
    
    cadena = re.compile("<table[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</table>","")
    
    cadena = re.compile("<td[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</td>","")
    
    cadena = re.compile("<div[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</div>","")
    
    cadena = re.compile("<dd[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</dd>","")

    cadena = re.compile("<font[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</font>","")
    
    cadena = re.compile("<strong[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</strong>","")

    cadena = re.compile("<small[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</small>","")

    cadena = re.compile("<span[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</span>","")

    cadena = re.compile("<a[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</a>","")
    
    cadena = re.compile("<p[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</p>","")

    cadena = re.compile("<ul[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</ul>","")
    
    cadena = re.compile("<h1[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h1>","")
    
    cadena = re.compile("<h2[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h2>","")

    cadena = re.compile("<h3[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h3>","")

    cadena = re.compile("<h4[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h4>","")

    cadena = re.compile("<!--[^-]+-->",re.DOTALL).sub("",cadena)
    
    cadena = re.compile("<img[^>]*>",re.DOTALL).sub("",cadena)
    
    cadena = re.compile("<br[^>]*>",re.DOTALL).sub("",cadena)

    cadena = re.compile("<object[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</object>","")
    cadena = re.compile("<param[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</param>","")
    cadena = re.compile("<embed[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</embed>","")

    cadena = re.compile("<title[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</title>","")

    cadena = re.compile("<link[^>]*>",re.DOTALL).sub("",cadena)

    cadena = cadena.replace("\t","")
    cadena = unescape(cadena)
    return cadena


def slugify(title):
    
    # Replace international chars
    title = title.replace("Á","a")
    title = title.replace("É","e")
    title = title.replace("Í","i")
    title = title.replace("Ó","o")
    title = title.replace("Ú","u")
    title = title.replace("á","a")
    title = title.replace("é","e")
    title = title.replace("í","i")
    title = title.replace("ó","o")
    title = title.replace("ú","u")
    title = title.replace("À","a")
    title = title.replace("È","e")
    title = title.replace("Ì","i")
    title = title.replace("Ò","o")
    title = title.replace("Ù","u")
    title = title.replace("à","a")
    title = title.replace("è","e")
    title = title.replace("ì","i")
    title = title.replace("ò","o")
    title = title.replace("ù","u")
    title = title.replace("ç","c")
    title = title.replace("Ç","C")
    title = title.replace("Ñ","n")
    title = title.replace("ñ","n")
    title = title.replace("/","-")
    title = title.replace("&amp;","&")

    # Lowercase
    title = title.lower().strip()

    # Remove invalid chards
    validchars = "abcdefghijklmnopqrstuvwxyz1234567890- "
    title = ''.join(c for c in title if c in validchars)

    # Replace redundant whitespaces
    title = re.compile("\s+",re.DOTALL).sub(" ",title)
    
    # Replace whitespaces for minus
    title = re.compile("\s",re.DOTALL).sub("-",title.strip())

    # Replace redundant minus
    title = re.compile("\-+",re.DOTALL).sub("-",title)
    
    # Fix some special cases
    if title.startswith("-"):
        title = title [1:]
    
    if title=="":
        title = "-"+str(time.time())

    return title

def download(url,filename,resume_download=True):
    _log("download url="+url+", filename="+filename)

    try:
        import xbmcgui
    
        # If file exists
        if os.path.exists(filename) and resume_download:
            f = open(filename, 'r+b')
            existSize = os.path.getsize(filename)
            
            _log("download File exists, size=%d, resume download" % existSize)
            downloaded = existSize
            f.seek(existSize)

        # File exists, skip download
        elif os.path.exists(filename) and not resume_download:
            _log("download File exists, skip download")
            return

        # File doesn't exists
        else:
            existSize = 0
            _log("download File doesn't exists")
            f = open(filename, 'wb')
            downloaded = 0
    
        # Progress dialog
        progress_dialog = xbmcgui.DialogProgress()
        progress_dialog.create( "plugin" , "Descargando..." , url , os.path.basename(filename) )

        # Timeout of socket to 60 secs
        socket.setdefaulttimeout(60)
    
        # URL con login y password
        if find_single_match(url,"http\://[a-z]+\:[a-z]+\@[a-z0-9\:\.]+/")!="":
            _log("download Basic auth")

            username = find_single_match(url,"http\://([a-z]+)\:[a-z]+\@[a-z0-9\:\.]+/")
            _log("download username="+username)
            password = find_single_match(url,"http\://[a-z]+\:([a-z]+)\@[a-z0-9\:\.]+/")
            _log("download password="+password)
            url = "http://"+find_single_match(url,"http\://[a-z]+\:[a-z]+\@(.*?)$")
            _log("download url="+url)
        else:
            username=""

        h = urllib2.HTTPHandler(debuglevel=0)

        request = urllib2.Request(url)
    
        if existSize > 0:
            request.add_header('Range', 'bytes=%d-' % (existSize, ))

        if username!="":

            user_and_pass = base64.b64encode(b""+username+":"+password+"").decode("ascii")
            _log("download Adding Authorization header") #: Basic "+user_and_pass)
            request.add_header('Authorization', 'Basic '+user_and_pass)

        opener = urllib2.build_opener(h)
        urllib2.install_opener(opener)
        try:
            connexion = opener.open(request)
        except urllib2.HTTPError,e:
            _log("download error %d (%s) al abrir la url %s" % (e.code,e.msg,url))
            f.close()
            progress_dialog.close()
            # Error 416 means range exceed file size => download is complete
            if e.code==416:
                return 0
            else:
                return -2
    
        try:
            total_size = int(connexion.headers["Content-Length"])
        except:
            total_size = 1
                
        if existSize > 0:
            total_size = total_size + existSize
    
        _log("download Content-Length=%s" % total_size)
    
        blocksize = 100*1024
    
        readed_block = connexion.read(blocksize)
        _log("download Starting download... (first block=%s bytes)" % len(readed_block))
    
        maxretries = 10
        
        while len(readed_block)>0:
            try:
                f.write(readed_block)
                downloaded = downloaded + len(readed_block)
                percent = int(float(downloaded)*100/float(total_size))
                totalmb = float(float(total_size)/(1024*1024))
                downloaded_mb = float(float(downloaded)/(1024*1024))
    
                # Read next block with retries
                retry_count = 0
                while retry_count <= maxretries:
                    try:
                        before = time.time()
                        readed_block = connexion.read(blocksize)
                        after = time.time()
                        if (after - before) > 0:
                            velocidad=len(readed_block)/((after - before))
                            falta=total_size-downloaded
                            if velocidad>0:
                                tiempofalta=falta/velocidad
                            else:
                                tiempofalta=0
                            #logger.info(sec_to_hms(tiempofalta))
                            #progress_dialog.update( percent , "Descargando %.2fMB de %.2fMB (%d%%)" % ( downloaded_mb , totalmb , percent),"Falta %s - Velocidad %.2f Kb/s" % ( sec_to_hms(tiempofalta) , velocidad/1024 ), os.path.basename(filename) )
                            progress_dialog.update( percent , "%.2fMB/%.2fMB (%d%%) %.2f Kb/s %s falta " % ( downloaded_mb , totalmb , percent , velocidad/1024 , sec_to_hms(tiempofalta)))
                        break

                        try:
                            if xbmc.abortRequested:
                                logger.error( "XBMC Abort requested 1" )
                                return -1
                        except:
                            pass

                    except:
                        try:
                            if xbmc.abortRequested:
                                logger.error( "XBMC Abort requested 2" )
                                return -1
                        except:
                            pass

                        retry_count = retry_count + 1
                        _log("download ERROR in block download, retry %d" % retry_count)
                        import traceback
                        _log("download "+traceback.format_exc())
                
                # Download cancelled
                try:
                    if progress_dialog.iscanceled():
                        _log("download Descarga del fichero cancelada")
                        f.close()
                        progress_dialog.close()
                        return -1
                except:
                    pass
    
                # Download error
                if retry_count > maxretries:
                    _log("download ERROR en la descarga del fichero")
                    f.close()
                    progress_dialog.close()
    
                    return -2
    
            except:
                import traceback
                _log("download "+traceback.format_exc() )

                f.close()
                progress_dialog.close()
                
                return -2

    except:
        import traceback
        _log("download "+traceback.format_exc())

    try:
        f.close()
    except:
        pass

    progress_dialog.close()

    _log("download Download complete")
    
def sec_to_hms(seconds):
    m,s = divmod(int(seconds), 60)
    h,m = divmod(m, 60)
    return ("%02d:%02d:%02d" % ( h , m ,s ))

def get_safe_filename( original_filename ):

    safe_filename = original_filename

    # Replace international chars
    safe_filename = safe_filename.replace("Á","A")
    safe_filename = safe_filename.replace("É","E")
    safe_filename = safe_filename.replace("Í","I")
    safe_filename = safe_filename.replace("Ó","O")
    safe_filename = safe_filename.replace("Ú","U")
    safe_filename = safe_filename.replace("á","a")
    safe_filename = safe_filename.replace("é","e")
    safe_filename = safe_filename.replace("í","i")
    safe_filename = safe_filename.replace("ó","o")
    safe_filename = safe_filename.replace("ú","u")
    safe_filename = safe_filename.replace("À","A")
    safe_filename = safe_filename.replace("È","E")
    safe_filename = safe_filename.replace("Ì","I")
    safe_filename = safe_filename.replace("Ò","O")
    safe_filename = safe_filename.replace("Ù","U")
    safe_filename = safe_filename.replace("à","a")
    safe_filename = safe_filename.replace("è","e")
    safe_filename = safe_filename.replace("ì","i")
    safe_filename = safe_filename.replace("ò","o")
    safe_filename = safe_filename.replace("ù","u")
    safe_filename = safe_filename.replace("ç","c")
    safe_filename = safe_filename.replace("Ç","C")
    safe_filename = safe_filename.replace("Ñ","N")
    safe_filename = safe_filename.replace("ñ","n")
    safe_filename = safe_filename.replace("/","-")
    safe_filename = safe_filename.replace("&amp;","&")

    # Remove invalid chards
    validchars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- "
    safe_filename = ''.join(c for c in safe_filename if c in validchars)

    # Replace redundant whitespaces
    safe_filename = re.compile("\s+",re.DOTALL).sub(" ",safe_filename)
    
    safe_filename = safe_filename.strip()
    
    if safe_filename=="":
        safe_filename = "invalid"

    return safe_filename

#get_filename_from_url(media_url)[-4:]
def get_filename_from_url(url):
    
    import urlparse
    parsed_url = urlparse.urlparse(url)
    try:
        filename = parsed_url.path
    except:
        # Si falla es porque la implementación de parsed_url no reconoce los atributos como "path"
        if len(parsed_url)>=4:
            filename = parsed_url[2]
        else:
            filename = ""

    if len(filename)>0:

        # Remove trailing slash
        if filename[-1:]=="/":
            filename = filename[:-1]
        
        if "/" in filename:
            filename = filename.split("/")[-1]

    return filename

def show_notification(title,message,icon=""):
    xbmc.executebuiltin((u'XBMC.Notification("'+title+'", "'+message+'", 2000, "'+icon+'")'))

f = open( os.path.join( os.path.dirname(__file__) , "addon.xml") )
data = f.read()
f.close()

addon_id = find_single_match(data,'id="([^"]+)"')
if addon_id=="":
    addon_id = find_single_match(data,"id='([^']+)'")

__settings__ = xbmcaddon.Addon(id=addon_id)
__language__ = __settings__.getLocalizedString
