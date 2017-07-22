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

ACTION_MOVE_LEFT       =  1 #Dpad Left
ACTION_MOVE_RIGHT      =  2 #Dpad Right
ACTION_MOVE_UP         =  3 #Dpad Up
ACTION_MOVE_DOWN       =  4 #Dpad Down
ACTION_PAGE_UP         =  5 #Left trigger
ACTION_PAGE_DOWN       =  6 #Right trigger
ACTION_SELECT_ITEM     =  7 #'A'
ACTION_HIGHLIGHT_ITEM  =  8
ACTION_PARENT_DIR      =  9 #'B'
ACTION_PREVIOUS_MENU   = 10 #'Back'
ACTION_SHOW_INFO       = 11
ACTION_PAUSE           = 12
ACTION_STOP            = 13 #'Start'
ACTION_NEXT_ITEM       = 14
ACTION_PREV_ITEM       = 15
ACTION_XBUTTON         = 18 #'X'
ACTION_YBUTTON         = 34 #'Y'
ACTION_MOUSEMOVE       = 90 # Mouse has moved
ACTION_MOUSEMOVE2      = 107 # Mouse has moved
ACTION_MOUSE_LEFT_CLICK = 100
ACTION_PREVIOUS_MENU2  = 92 #'Back'
ACTION_CONTEXT_MENU    = 117 # pops up the context menu
ACTION_CONTEXT_MENU2   = 229 # pops up the context menu (remote control "title" button)
ACTION_TOUCH_TAP = 401
ACTION_NOOP = 999

import plugintools
import os
import xbmc

# TODO: Definir fuentes small, medium, large etc por su tamaño y que busque la más apropiada (probar primero si se puede cambiar fuente en caliente en el skin)
def get_fonts():
    plugintools.log("get_fonts")

    skin = xbmc.getSkinDir()
    plugintools.log("get_fonts skin="+skin)

    try:
        skin_file = os.path.join(xbmc.translatePath('special://skin/1080i'), 'Font.xml')
        plugintools.log("skin_file="+skin_file)
        available_fonts = plugintools.read( skin_file, "r")
    except:
        try:
            skin_file = os.path.join(xbmc.translatePath('special://skin/720p'), 'Font.xml')
            plugintools.log("skin_file="+skin_file)
            available_fonts = plugintools.read( skin_file, "r")
        except:
            available_fonts = ""

    plugintools.log("get_fonts available_fonts="+repr(available_fonts))


    if "confluence" in skin or "estuary" in skin or "refocus" in skin:
        return {"10": "font10", "12": "font12", "16": "font16", "24": "font24_title", "30": "font30"}
    elif "aeonmq" in skin:
        return {"10": "font_14", "12": "font_16", "16": "font_20", "24": "font_24", "30": "font_30"}
    elif "madnox" in skin:
        return {"10": "Font_Reg22", "12": "Font_Reg26", "16": "Font_Reg32", "24": "Font_Reg38", "30": "Font_ShowcaseMainLabel2_Caps"}

    '''
    elif available_fonts:
        fuentes = plugintools.find_multiple_matches(data_font, "<name>([^<]+)<\/name>(?:<![^<]+>|)\s*<filename>[^<]+<\/filename>\s*<size>(\d+)<\/size>")
        sizes = []
        try:
            for name, size in fuentes:
                size = int(size)
                sizes.append([size, name])
            sizes.sort()
            fonts["10"] = sizes[0][1].lower()
            check = False
            if not 12 in sizes:
                for size, name in sizes:
                    if size != fonts["10"]:
                        fonts["12"] = name.lower()
                        check = True
                        break
            for size, name in sizes:
                if size == 12 and not check:
                    fonts["12"] = name.lower()
                elif size == 16:
                    fonts["16"] = name.lower()
                elif size == 24:
                    fonts["24"] = name.lower()
                elif size == 30:
                    fonts["30"] = name.lower()
                    break
                elif size > 30 and size <= 33:
                    fonts["30"] = name.lower()
                    break
        except:
            pass
    '''

    return {"10": "font10", "12": "font12", "16": "font16", "24": "font24", "30": "font30"}
