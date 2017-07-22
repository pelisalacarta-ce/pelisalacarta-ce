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
from core import logger
from core import scrapertools
from core import httptools
from platformcode import platformtools

class recaptcha(object):
    def start(self, handler, key, referer):
        self.handler = handler
        self.referer = referer
        self.key = key
        self.headers = {'Referer': self.referer}
        
        api_js = httptools.downloadpage("http://www.google.com/recaptcha/api.js?hl=es").data
        version = scrapertools.find_single_match(api_js, 'po.src = \'(.*?)\';').split("/")[5]

        self.url = "https://www.google.com/recaptcha/api/fallback?k=%s&hl=es&v=%s&t=2&ff=true" % (self.key, version)
        
        ID = self.update_window()
        
        return self.onClick(ID)
        
    def update_window(self):
            data = httptools.downloadpage(self.url, headers=self.headers).data
            self.message = scrapertools.find_single_match(data, '<div class="rc-imageselect-desc-no-canonical">(.*?)(?:</label>|</div>)')
            self.token = scrapertools.find_single_match(data, 'name="c" value="([^"]+)"')
            self.image = "https://www.google.com/recaptcha/api2/payload?k=%s&c=%s" % (self.key, self.token)
            self.result = {}
            
            JsonData = {}
            JsonData["action"]="recaptcha"   
            JsonData["data"]={}
            JsonData["data"]["title"] = "reCaptcha"
            JsonData["data"]["image"] = self.image
            JsonData["data"]["message"] = self.message
            JsonData["data"]["selected"] = [int(k) for k in range(9) if self.result.get(k, False) == True]
            JsonData["data"]["unselected"] = [int(k) for k in range(9) if self.result.get(k, False) == False]
            ID = self.handler.send_message(JsonData)
            return ID
                  
    def onClick(self, ID):
        while True:
            response = self.handler.get_data(ID)

            if type(response) == int:
                self.result[response] = not self.result.get(response, False)
                JsonData = {}
                JsonData["action"]="recaptcha_select"   
                JsonData["data"]={}
                JsonData["data"]["selected"] = [int(k) for k in range(9) if self.result.get(k, False) == True]
                JsonData["data"]["unselected"] = [int(k) for k in range(9) if self.result.get(k, False) == False]
                self.handler.send_message(JsonData)

            elif response == "refresh":
                ID = self.update_window()
                continue

            elif response == True:
                post = "c=%s" % self.token
                for r in sorted([k for k,v in self.result.items() if v == True]):
                    post += "&response=%s" % r
                logger.info(post)
                logger.info(self.result)
                data = httptools.downloadpage(self.url, post, headers=self.headers).data
                result = scrapertools.find_single_match(data, '<div class="fbc-verification-token">.*?>([^<]+)<')

                if result: 
                    platformtools.dialog_notification("Captcha Correcto", "La verificación ha concluido")
                    JsonData = {}
                    JsonData["action"]="ShowLoading"   
                    self.handler.send_message(JsonData)
                    return result
                else: 
                    ID = self.update_window()

            else:
                return 