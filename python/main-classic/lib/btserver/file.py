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
import os
from cursor import Cursor

class File(object):
    def __init__(self, path, base, index, size, fmap, piece_size, client):
        self._client = client
        self.path=path
        self.base=base
        self.index=index
        self.size=size

        self.piece_size=piece_size

        self.full_path= os.path.join(base,path)
        self.first_piece=fmap.piece
        self.offset=fmap.start
        self.last_piece=self.first_piece + max((size-1+fmap.start),0) // piece_size

        self.cursor = None

    def create_cursor(self, offset=None):
        self.cursor = Cursor(self)
        if offset:
            self.cursor.seek(offset)
        return self.cursor

    def map_piece(self, ofs):
        return self.first_piece+ (ofs+self.offset) // self.piece_size , (ofs+self.offset) % self.piece_size

    def update_piece(self, n, data):
        if self.cursor:
            self.cursor.update_piece(n,data)

    def __str__(self):
        return self.path