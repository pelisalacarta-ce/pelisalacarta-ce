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

#------------------------------------------------------------
# Script for downloading full series from most channels of pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#-------------------------------------------------------------------------------
# Example call:
#
# python download_serie.py --channel seriesflv --title="Outlander" --url="http://www.seriesflv.net/serie/outlander.html" --preferred_server=streamcloud --first_episode=1x01 --filter_language=es
#
# Where
#
#  - channel: Name of the pelisalacarta channel
#  - title: Name of the serie (will be included in filename, example "Outlander 1x01.mp4")
#  - url: Name of the page whith the episodes
#  - preferred_server: Preferred server for download
#  - first_episode: Where to start downloading
#  - filter_language (optional): Language for downloading
#
# Notes
#   If the episode file is present on the folder, it won't be downloaded again. 
#   This way you can call this script once per week to have the download
#   an ongoing serie up to date.
#-------------------------------------------------------------------------------

import re,urllib,urllib2,sys
sys.path.append ("lib")

from core import config
config.set_setting("debug", True)
config.set_setting("cache.mode", 2)

from core import scrapertools
from core.item import Item
from servers import servertools

def download_all_episodes(channel_name,action,title,url,preferred_server,first_episode,filter_language):
    exec "from channels import "+channel_name+" as channel"
    item = Item(show=title, extra=action, url=url)
    from core import downloadtools
    downloadtools.download_all_episodes(item,channel,first_episode=first_episode,preferred_server=preferred_server,filter_language=filter_language)

if __name__ == "__main__":
    import getopt
    options, arguments = getopt.getopt(sys.argv[1:], "", ["channel=","action=","title=","url=","preferred_server=","first_episode=","filter_language="])

    print options,arguments

    channel = "seriespepito"
    action = "episodios"
    title = ""
    url = ""
    preferred_server = "vidspot"
    first_episode = "1x01"
    filter_language = ""

    for option, argument in options:
        print option,argument
        if option == "--channel":
            channel = argument
        elif option == "--action":
            action = argument
        elif option == "--title":
            title = argument
        elif option == "--url":
            url = argument
        elif option == "--preferred_server":
            preferred_server = argument
        elif option == "--first_episode":
            first_episode = argument
        elif option == "--filter_language":
            filter_language = argument

    download_all_episodes(channel,action,title,url,preferred_server,first_episode,filter_language)

