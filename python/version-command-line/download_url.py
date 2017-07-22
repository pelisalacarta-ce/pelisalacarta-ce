# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta 4
# Copyright 2015 tvalacarta@gmail.com
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
#------------------------------------------------------------
# This file is part of pelisalacarta 4.
#
# pelisalacarta 4 is free software: you can redistribute it and/or modify
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

#-------------------------------------------------------------------------
# Script for downloading files from any server supported on pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#-------------------------------------------------------------------------

import re,urllib,urllib2,sys,os
sys.path.append ("lib")

from core import config
config.set_setting("debug", True)

from core import scrapertools
from core import downloadtools
from core.item import Item
from core import servertools

def download_url(url,titulo,server):

    url = url.replace("\\","")

    print "Analizando enlace "+url

    # Averigua el servidor
    if server=="":
        itemlist = servertools.find_video_items(data=url)
        if len(itemlist)==0:
            print "No se puede identificar el enlace"
            return

        item = itemlist[0]
        print "Es un enlace en "+item.server
    else:
        item = Item()
        item.server = server

    # Obtiene las URL de descarga
    video_urls, puedes, motivo = servertools.resolve_video_urls_for_playing(item.server,url)
    if len(video_urls)==0:
        print "No se ha encontrado nada para descargar"
        return

    # Descarga el de mejor calidad, como hace pelisalacarta
    print "Descargando..."
    print video_urls
    devuelve = downloadtools.downloadbest(video_urls,titulo,continuar=True)

if __name__ == "__main__":
    url = sys.argv[1]
    title = sys.argv[2]

    if len(sys.argv)>=4:
        server = sys.argv[3]
    else:
        server = ""

    if title.startswith("http://") or title.startswith("https://"):
        url = sys.argv[2]
        title = sys.argv[1]

    download_url(url,title,server)

