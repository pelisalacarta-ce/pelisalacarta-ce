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

import os
import sys
import re
import urlparse
import urllib
import urllib2
import time

import xbmc
import xbmcgui

import plugintools

class CustomPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        plugintools.log("CustomPlayer.__init__")
        xbmc.Player.__init__( self )
        self.current_time = 0
        self.total_time = 0
        self.listener = None
        self.seek_pos = 0

    def play_stream(self, url):  
        plugintools.log("CustomPlayer.play_stream url="+url)
        self.play(url)

    def play_item(self, item, pos=0):  
        plugintools.log("CustomPlayer.play_item pos="+repr(pos)+", item="+item.tostring())

        xbmc_listitem = xbmcgui.ListItem( label=item.title, iconImage=item.thumbnail, thumbnailImage=item.thumbnail, path=item.url)
        xbmc_listitem.setInfo( "video", { "Title": item.title , "Plot": item.plot } )
        xbmc_listitem.setProperty('fanart_image',item.fanart) 

        self.seek_pos = pos
        self.play(item.url,xbmc_listitem)

    def set_listener(self, listener):  
        plugintools.log("CustomPlayer.set_listener")

        self.listener = listener

    def onPlayBackStarted(self):
        plugintools.log("CustomPlayer.onPlayBackStarted")

        if self.seek_pos>0:
            self.seekTime(self.seek_pos)

        while self.isPlaying():
            self.current_time = self.getTime()
            self.total_time = self.getTotalTime()
            #plugintools.log("CustomPlayer.play_item current_time="+str(self.current_time)+" totaltime="+str(self.total_time))
            xbmc.sleep(2000)

    def onPlayBackEnded(self):
        plugintools.log("CustomPlayer.onPlayBackEnded")

    def onPlayBackStopped(self):
        plugintools.log("CustomPlayer.onPlayBackStopped")

        if self.listener is not None:
            self.listener.on_playback_stopped()

    def onPlayBackPaused(self):
        plugintools.log("CustomPlayer.onPlayBackPaused")

    def onPlayBackResumed(self):
        plugintools.log("CustomPlayer.onPlayBackResumed")

    def onPlayBackSeek(self,time,seekOffset):
        plugintools.log("CustomPlayer.onPlayBackSeek")

    def onPlayBackSeekChapter(self,seekChaper):
        plugintools.log("CustomPlayer.onPlayBackSeekChapter")

    def onPlayBackSpeedChanged(self,speed):
        plugintools.log("CustomPlayer.onPlayBackSpeedChanged")

    def onQueueNextItem(self):
        plugintools.log("CustomPlayer.onQueueNextItem")

    def get_current_time(self):
        return self.current_time

    def get_total_time(self):
        return self.total_time

def play(url):
    plugintools.log("custom_play ["+url+"]")

    player = CustomPlayer()
    player.PlayStream( url )

