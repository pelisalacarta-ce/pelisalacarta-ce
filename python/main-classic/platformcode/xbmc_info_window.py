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
from core import logger
from core.tmdb import Tmdb

ID_BUTTON_CLOSE = 10003
ID_BUTTON_PREVIOUS = 10025
ID_BUTTON_NEXT = 10026
ID_BUTTON_CANCEL = 10027
ID_BUTTON_OK = 10028


class InfoWindow(xbmcgui.WindowXMLDialog):
    otmdb = None

    item_title = ""
    item_serie = ""
    item_temporada = 0
    item_episodio = 0
    result = {}

    # PARA TMDB
    @staticmethod
    def get_language(lng):
        # Cambiamos el formato del Idioma
        languages = {
            'aa': 'Afar', 'ab': 'Abkhazian', 'af': 'Afrikaans', 'ak': 'Akan', 'sq': 'Albanian', 'am': 'Amharic',
            'ar': 'Arabic', 'an': 'Aragonese', 'as': 'Assamese', 'av': 'Avaric', 'ae': 'Avestan', 'ay': 'Aymara',
            'az': 'Azerbaijani', 'ba': 'Bashkir', 'bm': 'Bambara', 'eu': 'Basque', 'be': 'Belarusian', 'bn': 'Bengali',
            'bh': 'Bihari languages', 'bi': 'Bislama', 'bo': 'Tibetan', 'bs': 'Bosnian', 'br': 'Breton',
            'bg': 'Bulgarian', 'my': 'Burmese', 'ca': 'Catalan; Valencian', 'cs': 'Czech', 'ch': 'Chamorro',
            'ce': 'Chechen', 'zh': 'Chinese',
            'cu': 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic', 'cv': 'Chuvash',
            'kw': 'Cornish', 'co': 'Corsican', 'cr': 'Cree', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German',
            'dv': 'Divehi; Dhivehi; Maldivian', 'nl': 'Dutch; Flemish', 'dz': 'Dzongkha', 'en': 'English',
            'eo': 'Esperanto', 'et': 'Estonian', 'ee': 'Ewe', 'fo': 'Faroese', 'fa': 'Persian', 'fj': 'Fijian',
            'fi': 'Finnish', 'fr': 'French', 'fy': 'Western Frisian', 'ff': 'Fulah', 'Ga': 'Georgian',
            'gd': 'Gaelic; Scottish Gaelic', 'ga': 'Irish', 'gl': 'Galician', 'gv': 'Manx',
            'el': 'Greek, Modern (1453-)', 'gn': 'Guarani', 'gu': 'Gujarati', 'ht': 'Haitian; Haitian Creole',
            'ha': 'Hausa', 'he': 'Hebrew', 'hz': 'Herero', 'hi': 'Hindi', 'ho': 'Hiri Motu', 'hr': 'Croatian',
            'hu': 'Hungarian', 'hy': 'Armenian', 'ig': 'Igbo', 'is': 'Icelandic', 'io': 'Ido',
            'ii': 'Sichuan Yi; Nuosu', 'iu': 'Inuktitut', 'ie': 'Interlingue; Occidental',
            'ia': 'Interlingua (International Auxiliary Language Association)', 'id': 'Indonesian', 'ik': 'Inupiaq',
            'it': 'Italian', 'jv': 'Javanese', 'ja': 'Japanese', 'kl': 'Kalaallisut; Greenlandic', 'kn': 'Kannada',
            'ks': 'Kashmiri', 'ka': 'Georgian', 'kr': 'Kanuri', 'kk': 'Kazakh', 'km': 'Central Khmer',
            'ki': 'Kikuyu; Gikuyu', 'rw': 'Kinyarwanda', 'ky': 'Kirghiz; Kyrgyz', 'kv': 'Komi', 'kg': 'Kongo',
            'ko': 'Korean', 'kj': 'Kuanyama; Kwanyama', 'ku': 'Kurdish', 'lo': 'Lao', 'la': 'Latin', 'lv': 'Latvian',
            'li': 'Limburgan; Limburger; Limburgish', 'ln': 'Lingala', 'lt': 'Lithuanian',
            'lb': 'Luxembourgish; Letzeburgesch', 'lu': 'Luba-Katanga', 'lg': 'Ganda', 'mk': 'Macedonian',
            'mh': 'Marshallese', 'ml': 'Malayalam', 'mi': 'Maori', 'mr': 'Marathi', 'ms': 'Malay', 'Mi': 'Micmac',
            'mg': 'Malagasy', 'mt': 'Maltese', 'mn': 'Mongolian', 'na': 'Nauru', 'nv': 'Navajo; Navaho',
            'nr': 'Ndebele, South; South Ndebele', 'nd': 'Ndebele, North; North Ndebele', 'ng': 'Ndonga',
            'ne': 'Nepali', 'nn': 'Norwegian Nynorsk; Nynorsk, Norwegian', 'nb': 'Bokmål, Norwegian; Norwegian Bokmål',
            'no': 'Norwegian', 'oc': 'Occitan (post 1500)', 'oj': 'Ojibwa', 'or': 'Oriya', 'om': 'Oromo',
            'os': 'Ossetian; Ossetic', 'pa': 'Panjabi; Punjabi', 'pi': 'Pali', 'pl': 'Polish', 'pt': 'Portuguese',
            'ps': 'Pushto; Pashto', 'qu': 'Quechua', 'ro': 'Romanian; Moldavian; Moldovan', 'rn': 'Rundi',
            'ru': 'Russian', 'sg': 'Sango', 'rm': 'Romansh', 'sa': 'Sanskrit', 'si': 'Sinhala; Sinhalese',
            'sk': 'Slovak', 'sl': 'Slovenian', 'se': 'Northern Sami', 'sm': 'Samoan', 'sn': 'Shona', 'sd': 'Sindhi',
            'so': 'Somali', 'st': 'Sotho, Southern', 'es': 'Spanish', 'sc': 'Sardinian', 'sr': 'Serbian', 'ss': 'Swati',
            'su': 'Sundanese', 'sw': 'Swahili', 'sv': 'Swedish', 'ty': 'Tahitian', 'ta': 'Tamil', 'tt': 'Tatar',
            'te': 'Telugu', 'tg': 'Tajik', 'tl': 'Tagalog', 'th': 'Thai', 'ti': 'Tigrinya',
            'to': 'Tonga (Tonga Islands)', 'tn': 'Tswana', 'ts': 'Tsonga', 'tk': 'Turkmen', 'tr': 'Turkish',
            'tw': 'Twi', 'ug': 'Uighur; Uyghur', 'uk': 'Ukrainian', 'ur': 'Urdu', 'uz': 'Uzbek', 've': 'Venda',
            'vi': 'Vietnamese', 'vo': 'Volapük', 'wa': 'Walloon', 'wo': 'Wolof', 'xh': 'Xhosa', 'yi': 'Yiddish',
            'yo': 'Yoruba', 'za': 'Zhuang; Chuang', 'zu': 'Zulu'}

        return languages.get(lng, lng)

    def get_scraper_data(self, data_in):
        self.otmdb = None
        # logger.debug(str(data_in))

        if self.listData:
            # Datos comunes a todos los listados
            infoLabels = self.scraper().get_infoLabels(origen=data_in)

            if "original_language" in infoLabels:
                infoLabels["language"] = self.get_language(infoLabels["original_language"])
            infoLabels["puntuacion"] = "%s/10 (%s)" % (infoLabels.get("rating", "?"), infoLabels.get("votes", "N/A"))

            self.result = infoLabels

    def Start(self, data, caption="Información del vídeo", item=None, scraper=Tmdb):
        # Capturamos los parametros
        self.caption = caption
        self.item = item
        self.indexList = -1
        self.listData = None
        self.return_value = None
        self.scraper = scraper

        logger.debug(data)
        if type(data) == list:
            self.listData = data
            self.indexList = 0
            data = self.listData[self.indexList]

        self.get_scraper_data(data)

        # Muestra la ventana
        self.doModal()
        return self.return_value

    def __init__(self, *args):
        self.caption = ""
        self.item = None
        self.listData = None
        self.indexList = 0
        self.return_value = None
        self.scraper = Tmdb

    def onInit(self):
        if xbmcgui.__version__ == "1.2":
            self.setCoordinateResolution(1)
        else:
            self.setCoordinateResolution(5)
          
        # Ponemos el título y las imagenes
        self.getControl(10002).setLabel(self.caption)
        self.getControl(10004).setImage(self.result.get("fanart", ""))
        self.getControl(10005).setImage(self.result.get("thumbnail", "images/img_no_disponible.png"))

        # Cargamos los datos para el formato pelicula
        if self.result.get("mediatype", "movie") == "movie":
            self.getControl(10006).setLabel("Título:")
            self.getControl(10007).setLabel(self.result.get("title", "N/A"))
            self.getControl(10008).setLabel("Título original:")
            self.getControl(10009).setLabel(self.result.get("originaltitle", "N/A"))
            self.getControl(100010).setLabel("Idioma original:")
            self.getControl(100011).setLabel(self.result.get("language", "N/A"))
            self.getControl(100012).setLabel("Puntuación:")
            self.getControl(100013).setLabel(self.result.get("puntuacion", "N/A"))
            self.getControl(100014).setLabel("Lanzamiento:")
            self.getControl(100015).setLabel(self.result.get("release_date", "N/A"))
            self.getControl(100016).setLabel("Géneros:")
            self.getControl(100017).setLabel(self.result.get("genre", "N/A"))

        # Cargamos los datos para el formato serie
        else:
            self.getControl(10006).setLabel("Serie:")
            self.getControl(10007).setLabel(self.result.get("title", "N/A"))
            self.getControl(10008).setLabel("Idioma original:")
            self.getControl(10009).setLabel(self.result.get("language", "N/A"))
            self.getControl(100010).setLabel("Puntuación:")
            self.getControl(100011).setLabel(self.result.get("puntuacion", "N/A"))
            self.getControl(100012).setLabel("Géneros:")
            self.getControl(100013).setLabel(self.result.get("genre", "N/A"))

            if self.result.get("season"):
                self.getControl(100014).setLabel("Título temporada:")
                self.getControl(100015).setLabel(self.result.get("temporada_nombre", "N/A"))
                self.getControl(100016).setLabel("Temporada:")
                self.getControl(100017).setLabel(self.result.get("season", "N/A") + " de " +
                                                 self.result.get("seasons", "N/A"))
            if self.result.get("episode"):
                self.getControl(100014).setLabel("Título:")
                self.getControl(100015).setLabel(self.result.get("episode_title", "N/A"))
                self.getControl(100018).setLabel("Episodio:")
                self.getControl(100019).setLabel(self.result.get("episode", "N/A") + " de " +
                                                 self.result.get("episodes", "N/A"))
                self.getControl(100020).setLabel("Emisión:")
                self.getControl(100021).setLabel(self.result.get("date", "N/A"))

        # Sinopsis
        if self.result['plot']:
            self.getControl(100022).setLabel("Sinopsis:")
            self.getControl(100023).setText(self.result.get("plot", "N/A"))
        else:
            self.getControl(100022).setLabel("")
            self.getControl(100023).setText("")

        # Cargamos los botones si es necesario
        self.getControl(10024).setVisible(self.indexList > -1)  # Grupo de botones
        self.getControl(ID_BUTTON_PREVIOUS).setEnabled(self.indexList > 0)  # Anterior

        if self.listData:
            m = len(self.listData)
        else:
            m = 1

        self.getControl(ID_BUTTON_NEXT).setEnabled(self.indexList + 1 != m)  # Siguiente
        self.getControl(100029).setLabel("(%s/%s)" % (self.indexList + 1, m))  # x/m

        # Ponemos el foco en el Grupo de botones, si estuviera desactivado "Anterior" iria el foco al boton "Siguiente"
        # si "Siguiente" tb estuviera desactivado pasara el foco al botón "Cancelar"
        self.setFocus(self.getControl(10024))

        return self.return_value

    def onClick(self, _id):
        logger.info("onClick id=" + repr(_id))
        if _id == ID_BUTTON_PREVIOUS and self.indexList > 0:
            self.indexList -= 1
            self.get_scraper_data(self.listData[self.indexList])
            self.onInit()

        elif _id == ID_BUTTON_NEXT and self.indexList < len(self.listData) - 1:
            self.indexList += 1
            self.get_scraper_data(self.listData[self.indexList])
            self.onInit()

        elif _id == ID_BUTTON_OK or _id == ID_BUTTON_CLOSE or _id == ID_BUTTON_CANCEL:
            self.close()

            if _id == ID_BUTTON_OK:
                self.return_value = self.listData[self.indexList]
            else:
                self.return_value = None

    def onAction(self, action):
        logger.info("action="+repr(action.getId()))
        action = action.getId()

        # Obtenemos el foco
        focus = self.getFocusId()

        # Accion 1: Flecha izquierda
        if action == 1:

            if focus == ID_BUTTON_OK:
                self.setFocus(self.getControl(ID_BUTTON_CANCEL))

            elif focus == ID_BUTTON_CANCEL:
                if self.indexList + 1 != len(self.listData):
                    # vamos al botón Siguiente
                    self.setFocus(self.getControl(ID_BUTTON_NEXT))
                elif self.indexList > 0:
                    # vamos al botón Anterior ya que Siguiente no está activo (estamos al final de la lista)
                    self.setFocus(self.getControl(ID_BUTTON_PREVIOUS))

            elif focus == ID_BUTTON_NEXT:
                if self.indexList > 0:
                    # vamos al botón Anterior
                    self.setFocus(self.getControl(ID_BUTTON_PREVIOUS))

        # Accion 2: Flecha derecha
        elif action == 2:

            if focus == ID_BUTTON_PREVIOUS:
                if self.indexList + 1 != len(self.listData):
                    # vamos al botón Siguiente
                    self.setFocus(self.getControl(ID_BUTTON_NEXT))
                else:
                    # vamos al botón Cancelar ya que Siguiente no está activo (estamos al final de la lista)
                    self.setFocus(self.getControl(ID_BUTTON_CANCEL))

            elif focus == ID_BUTTON_NEXT:
                self.setFocus(self.getControl(ID_BUTTON_CANCEL))

            elif focus == ID_BUTTON_CANCEL:
                self.setFocus(self.getControl(ID_BUTTON_OK))

        # Pulsa ESC o Atrás, simula click en boton cancelar
        if action in [10, 92]:
            self.onClick(ID_BUTTON_CANCEL)
