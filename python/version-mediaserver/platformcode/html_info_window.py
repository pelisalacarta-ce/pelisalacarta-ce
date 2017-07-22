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

import inspect
import os
import re
from core.tmdb import Tmdb
from core.item import Item, InfoLabels
from core import logger


class InfoWindow(object):
    otmdb = None
    item_title = ""
    item_serie = ""
    item_temporada = 0
    item_episodio = 0
    result = {}

    @staticmethod
    def get_language(lng):
        # Cambiamos el formato del Idioma
        languages = {
            'aa': 'Afar', 'ab': 'Abkhazian', 'af': 'Afrikaans', 'ak': 'Akan', 'sq': 'Albanian', 'am': 'Amharic',
            'ar': 'Arabic', 'an': 'Aragonese', 'as': 'Assamese', 'av': 'Avaric', 'ae': 'Avestan',
            'ay': 'Aymara', 'az': 'Azerbaijani', 'ba': 'Bashkir', 'bm': 'Bambara', 'eu': 'Basque',
            'be': 'Belarusian', 'bn': 'Bengali', 'bh': 'Bihari languages', 'bi': 'Bislama',
            'bo': 'Tibetan', 'bs': 'Bosnian', 'br': 'Breton', 'bg': 'Bulgarian', 'my': 'Burmese',
            'ca': 'Catalan; Valencian', 'cs': 'Czech', 'ch': 'Chamorro', 'ce': 'Chechen', 'zh': 'Chinese',
            'cu': 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic',
            'cv': 'Chuvash', 'kw': 'Cornish', 'co': 'Corsican', 'cr': 'Cree', 'cy': 'Welsh',
            'da': 'Danish', 'de': 'German', 'dv': 'Divehi; Dhivehi; Maldivian', 'nl': 'Dutch; Flemish',
            'dz': 'Dzongkha', 'en': 'English', 'eo': 'Esperanto',
            'et': 'Estonian', 'ee': 'Ewe', 'fo': 'Faroese', 'fa': 'Persian', 'fj': 'Fijian',
            'fi': 'Finnish', 'fr': 'French', 'fy': 'Western Frisian', 'ff': 'Fulah',
            'Ga': 'Georgian', 'gd': 'Gaelic; Scottish Gaelic', 'ga': 'Irish', 'gl': 'Galician',
            'gv': 'Manx', 'el': 'Greek, Modern (1453-)', 'gn': 'Guarani', 'gu': 'Gujarati',
            'ht': 'Haitian; Haitian Creole', 'ha': 'Hausa', 'he': 'Hebrew', 'hz': 'Herero', 'hi': 'Hindi',
            'ho': 'Hiri Motu', 'hr': 'Croatian', 'hu': 'Hungarian', 'hy': 'Armenian', 'ig': 'Igbo',
            'is': 'Icelandic', 'io': 'Ido', 'ii': 'Sichuan Yi; Nuosu', 'iu': 'Inuktitut',
            'ie': 'Interlingue; Occidental', 'ia': 'Interlingua (International Auxiliary Language Association)',
            'id': 'Indonesian', 'ik': 'Inupiaq', 'it': 'Italian', 'jv': 'Javanese',
            'ja': 'Japanese', 'kl': 'Kalaallisut; Greenlandic', 'kn': 'Kannada', 'ks': 'Kashmiri',
            'ka': 'Georgian', 'kr': 'Kanuri', 'kk': 'Kazakh', 'km': 'Central Khmer', 'ki': 'Kikuyu; Gikuyu',
            'rw': 'Kinyarwanda', 'ky': 'Kirghiz; Kyrgyz', 'kv': 'Komi', 'kg': 'Kongo', 'ko': 'Korean',
            'kj': 'Kuanyama; Kwanyama', 'ku': 'Kurdish', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
            'li': 'Limburgan; Limburger; Limburgish', 'ln': 'Lingala', 'lt': 'Lithuanian',
            'lb': 'Luxembourgish; Letzeburgesch', 'lu': 'Luba-Katanga', 'lg': 'Ganda', 'mk': 'Macedonian',
            'mh': 'Marshallese', 'ml': 'Malayalam', 'mi': 'Maori', 'mr': 'Marathi', 'ms': 'Malay', 'Mi': 'Micmac',
            'mg': 'Malagasy', 'mt': 'Maltese', 'mn': 'Mongolian', 'na': 'Nauru',
            'nv': 'Navajo; Navaho', 'nr': 'Ndebele, South; South Ndebele', 'nd': 'Ndebele, North; North Ndebele',
            'ng': 'Ndonga', 'ne': 'Nepali', 'nn': 'Norwegian Nynorsk; Nynorsk, Norwegian',
            'nb': 'Bokmål, Norwegian; Norwegian Bokmål', 'no': 'Norwegian', 'oc': 'Occitan (post 1500)',
            'oj': 'Ojibwa', 'or': 'Oriya', 'om': 'Oromo', 'os': 'Ossetian; Ossetic', 'pa': 'Panjabi; Punjabi',
            'pi': 'Pali', 'pl': 'Polish', 'pt': 'Portuguese', 'ps': 'Pushto; Pashto', 'qu': 'Quechua',
            'ro': 'Romanian; Moldavian; Moldovan', 'rn': 'Rundi', 'ru': 'Russian', 'sg': 'Sango', 'rm': 'Romansh',
            'sa': 'Sanskrit', 'si': 'Sinhala; Sinhalese', 'sk': 'Slovak', 'sl': 'Slovenian', 'se': 'Northern Sami',
            'sm': 'Samoan', 'sn': 'Shona', 'sd': 'Sindhi', 'so': 'Somali', 'st': 'Sotho, Southern', 'es': 'Spanish',
            'sc': 'Sardinian', 'sr': 'Serbian', 'ss': 'Swati', 'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish',
            'ty': 'Tahitian', 'ta': 'Tamil', 'tt': 'Tatar', 'te': 'Telugu', 'tg': 'Tajik', 'tl': 'Tagalog',
            'th': 'Thai', 'ti': 'Tigrinya', 'to': 'Tonga (Tonga Islands)', 'tn': 'Tswana', 'ts': 'Tsonga',
            'tk': 'Turkmen', 'tr': 'Turkish', 'tw': 'Twi', 'ug': 'Uighur; Uyghur', 'uk': 'Ukrainian',
            'ur': 'Urdu', 'uz': 'Uzbek', 've': 'Venda', 'vi': 'Vietnamese', 'vo': 'Volapük',
            'wa': 'Walloon', 'wo': 'Wolof', 'xh': 'Xhosa', 'yi': 'Yiddish', 'yo': 'Yoruba', 'za': 'Zhuang; Chuang',
            'zu': 'Zulu'}

        return languages.get(lng, lng)


    def get_scraper_data(self, data_in):
        self.otmdb = None
        # logger.debug(str(data_in))

        if self.listData:
            # Datos comunes a todos los listados
            infoLabels = self.scraper().get_infoLabels(origen=data_in)

            if "original_language" in infoLabels:
                infoLabels["language"] = self.get_language(infoLabels["original_language"])
            if "vote_average" in data_in and "vote_count" in data_in:
                infoLabels["puntuacion"] = str(data_in["vote_average"]) + "/10 (" + str(data_in["vote_count"]) + ")"

            self.result = infoLabels

    def Start(self, handler, data, caption="Información del vídeo", item=None, scraper=Tmdb):
        # Capturamos los parametros
        self.caption = caption
        self.item = item
        self.indexList = -1
        self.listData = []
        self.handler = handler
        self.scraper = scraper

        logger.debug(data)
        if type(data) == list:
            self.listData = data
            self.indexList = 0
            data = self.listData[self.indexList]

        self.get_scraper_data(data)

        ID = self.update_window()
        
        return self.onClick(ID)
        
    def update_window(self):
          JsonData = {}
          JsonData["action"]="OpenInfo"   
          JsonData["data"]={}
          JsonData["data"]["buttons"] = len(self.listData) > 0
          JsonData["data"]["previous"] = self.indexList > 0
          JsonData["data"]["next"] = self.indexList + 1 < len(self.listData)
          JsonData["data"]["count"] = "(%s/%s)" %(self.indexList + 1, len(self.listData))
          JsonData["data"]["title"]= self.caption
          JsonData["data"]["fanart"] = self.result.get("fanart", "")
          JsonData["data"]["thumbnail"] = self.result.get("thumbnail", "")
        
          JsonData["data"]["lines"]=[]
          
          if self.result.get("mediatype", "movie") == "movie":
            JsonData["data"]["lines"].append({"title": "Título:","text": self.result.get("title", "N/A")})
            JsonData["data"]["lines"].append({"title": "Título Original:","text": self.result.get("originaltitle", "N/A")})
            JsonData["data"]["lines"].append({"title": "Idioma Original:","text": self.result.get("language", "N/A")})
            JsonData["data"]["lines"].append({"title": "Puntuación:","text": self.result.get("puntuacion", "N/A")})
            JsonData["data"]["lines"].append({"title": "Lanzamiento:","text": self.result.get("release_date", "N/A")})
            JsonData["data"]["lines"].append({"title": "Generos:","text": self.result.get("genre", "N/A")})
            JsonData["data"]["lines"].append({"title": "","text": ""})
            
            
          else:
            JsonData["data"]["lines"].append({"title": "Serie:","text": self.result.get("title", "N/A")})
            JsonData["data"]["lines"].append({"title": "Idioma Original:","text": self.result.get("language", "N/A")})
            JsonData["data"]["lines"].append({"title": "Puntuación:","text": self.result.get("puntuacion", "N/A")})
            JsonData["data"]["lines"].append({"title": "Generos:","text": self.result.get("genre", "N/A")})
            
            if self.result.get("season"):
              JsonData["data"]["lines"].append({"title": "Titulo temporada:","text": self.result.get("temporada_nombre", "N/A")})
              JsonData["data"]["lines"].append({"title": "Temporada:","text": self.result.get("season", "N/A") + " de " + self.result.get("seasons", "N/A")})
              JsonData["data"]["lines"].append({"title": "","text": ""})
            

            if self.result.get("episode"):
              JsonData["data"]["lines"].append({"title": "Titulo:","text": self.result.get("episode_title", "N/A")})
              JsonData["data"]["lines"].append({"title": "Episodio:","text": self.result.get("episode", "N/A") + " de " + self.result.get("episodes", "N/A")})
              JsonData["data"]["lines"].append({"title": "Emisión:","text": self.result.get("date", "N/A")})  
            
            
          if self.result.get("plot"):
            JsonData["data"]["lines"].append({"title": "Sinopsis:","text": self.result["plot"]})
          else:
            JsonData["data"]["lines"].append({"title": "","text": ""})
            
          ID = self.handler.send_message(JsonData)
          return ID
                  
    def onClick(self, ID):
        while True:
          response = self.handler.get_data(ID)

          if response == "ok":
            return self.listData[self.indexList]
            
          elif response == "close":
            return None
            
          elif response == "next" and self.indexList < len(self.listData) - 1:
            self.indexList += 1
            self.get_scraper_data(self.listData[self.indexList])
            ID = self.update_window()
            
            
          elif response == "previous" and self.indexList > 0:
            self.indexList -= 1
            self.get_scraper_data(self.listData[self.indexList])
            ID = self.update_window()
