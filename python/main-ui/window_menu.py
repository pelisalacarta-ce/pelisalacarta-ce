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
import urlparse,urllib,urllib2

import xbmc
import xbmcgui
import xbmcaddon

from windowtools import *

import plugintools
import navigation
from core.item import Item

class MenuWindow(xbmcgui.WindowXML):

    def __init__(self, xml_name, fallback_path):
        plugintools.log("MenuWindow.__init__ xml_name="+xml_name+" fallback_path="+fallback_path)

        if self.getResolution()>0:
            self.setCoordinateResolution(0)

        self.first_time = False
        self.itemlist = None

    def setParentItem(self,item):
        self.parent_item = item

    def setItemlist(self,itemlist):
        plugintools.log("MenuWindow.setItemlist")

        self.itemlist = []

        for item in itemlist:
            plugintools.log("MenuWindow.setItemlist item="+item.tostring())
            self.itemlist.append(item)

    def onInit( self ):
        plugintools.log("MenuWindow.onInit")

        if self.first_time == True:
            return
        
        self.first_time = True
                   
        self.control_list = self.getControl(100)

        if self.itemlist is None:
            next_items = navigation.get_next_items( self.parent_item )
            self.setItemlist(next_items)

        if len(self.itemlist)>0:
            item = self.itemlist[0]
            self.setContentDetailsFields(item)

        for item in self.itemlist:

            list_item = xbmcgui.ListItem( item.title , iconImage=item.thumbnail, thumbnailImage=item.thumbnail)

            info_labels = { "Title" : item.title, "FileName" : item.title, "Plot" : item.plot }
            list_item.setInfo( "video", info_labels )

            if item.fanart!="":
                list_item.setProperty('fanart_image',item.fanart)

            self.control_list.addItem(list_item)

        self.getControl(300).setLabel(self.parent_item.channel)
        self.setFocusId(100)

        self.loader = self.getControl(400)
        self.loader.setVisible(False)

    def setContentDetailsFields(self, item):

        nthumbnail = ""
        ntitle = ""
        nplot = ""
        
        if item.thumbnail!="" and not "thumb_error" in item.thumbnail and not "thumb_folder" in item.thumbnail and not "thumb_nofolder" in item.thumbnail:
            nthumbnail = item.thumbnail
            ntitle=item.title
            nplot=item.plot

        if item.hasContentDetails==True:

            if item.contentThumbnail and item.contentThumbnail!="":
                nthumbnail = item.contentThumbnail

            if item.contentTitle and item.contentTitle!="":
                ntitle=item.contentTitle

            if item.contentPlot and item.contentPlot!="":
                nplot=item.contentPlot

        self.getControl(301).setImage(nthumbnail)
        self.getControl(302).setText(ntitle)
        self.getControl(303).setText(nplot)

    def onAction(self, action):
        plugintools.log("MenuWindow.onAction action.id="+repr(action.getId())+" action.buttonCode="+repr(action.getButtonCode()))

        pos = self.control_list.getSelectedPosition()

        try:
            item = self.itemlist[pos]
            self.setContentDetailsFields(item)
        except:
            import traceback
            plugintools.log(traceback.format_exc())
            self.close()

        if action == ACTION_PARENT_DIR or action==ACTION_PREVIOUS_MENU or action==ACTION_PREVIOUS_MENU2:
            self.close()

        if action == ACTION_SELECT_ITEM or action == ACTION_MOUSE_LEFT_CLICK:

            #loader_image = os.path.join( plugintools.get_runtime_path(), 'resources', 'skins', 'Default', 'media', 'loader.gif')
            #loader = xbmcgui.ControlImage(1200, 19, 40, 40, loader_image)
            #self.addControl(loader)
            #loader = self.getControl(400)
            #self.loader.setVisible(True)

            pos = self.control_list.getSelectedPosition()
            item = self.itemlist[pos]

            #next_items = navigation.get_next_items( item )
            self.loader.setVisible(False)

            if item.action=="play":
                navigation.play_item(item)
            else:
                # Si no hay nada, no muestra la pantalla vacía
                #if len(next_items)>0:
                next_window = navigation.get_window_for_item( item )
                #next_window.setItemlist(next_items)
                next_window.setParentItem(item)

                next_window.doModal()
                del next_window

    def on_playback_stopped( self ):
        plugintools.log("DetailWindow.on_playback_stopped currentTime="+str(self.custom_player.get_current_time())+", totalTime="+str(self.custom_player.get_total_time()))
        plugintools.log("DetailWindow.on_playback_stopped parent_item="+self.parent_item.tostring())

    def onFocus( self, control_id ):
        plugintools.log("MenuWindow.onFocus "+repr(control_id))
        pass

    def onClick( self, control_id ):
        plugintools.log("MenuWindow.onClick "+repr(control_id))
        pass

    def onControl(self, control):
        plugintools.log("MenuWindow.onClick "+repr(control))
        pass
