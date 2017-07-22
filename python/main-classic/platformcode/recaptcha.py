# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta 4
# Copyright 2015 tvalacarta@gmail.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
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
# ------------------------------------------------------------
import xbmcgui
from core import httptools
from core import scrapertools
from core import config
from core import logger
from platformcode import platformtools

class Recaptcha(xbmcgui.WindowXMLDialog):
    def Start(self, key, referer):
        self.referer = referer
        self.key = key
        self.headers = {'Referer': self.referer}
        
        api_js = httptools.downloadpage("http://www.google.com/recaptcha/api.js?hl=es").data
        version = scrapertools.find_single_match(api_js, 'po.src = \'(.*?)\';').split("/")[5]
        self.url = "http://www.google.com/recaptcha/api/fallback?k=%s&hl=es&v=%s&t=2&ff=true" % (self.key, version)
        self.doModal()
        #Reload
        if self.result == {}:
            self.result = Recaptcha("Recaptcha.xml", config.get_runtime_path()).Start(self.key, self.referer)
            
        return self.result
                
    def update_window(self):
        data = httptools.downloadpage(self.url, headers=self.headers).data
        self.message = scrapertools.find_single_match(data, '<div class="rc-imageselect-desc-no-canonical">(.*?)(?:</label>|</div>)').replace("<strong>", "[B]").replace("</strong>","[/B]")
        self.token = scrapertools.find_single_match(data, 'name="c" value="([^"]+)"')
        self.image = "http://www.google.com/recaptcha/api2/payload?k=%s&c=%s" % (self.key, self.token)
        self.result = {}
        self.getControl(10020).setImage(self.image)
        self.getControl(10000).setText(self.message)
        self.setFocusId(10005)
        
    
    def __init__(self, *args, **kwargs):
        self.mensaje = kwargs.get("mensaje")
        self.imagen = kwargs.get("imagen")

    def onInit(self):
        self.setCoordinateResolution(2)
        self.update_window()

        
    def onClick(self, control):
        if control == 10003:
            self.result = None
            self.close()
            
        elif control == 10004:
            self.result = {}
            self.close()
            
        elif control == 10002:
            self.result = [int(k) for k in range(9) if self.result.get(k, False) == True]
            post = "c=%s" % self.token

            for r in self.result:
                post += "&response=%s" % r

            data = httptools.downloadpage(self.url, post, headers=self.headers).data
            self.result = scrapertools.find_single_match(data, '<div class="fbc-verification-token">.*?>([^<]+)<')
            if self.result:
                platformtools.dialog_notification("Captcha Correcto", "La verificación ha concluido")
                self.close()
            else:
                self.result = {}
                self.close()
        else:
            self.result[control - 10005] = not self.result.get(control - 10005, False)

