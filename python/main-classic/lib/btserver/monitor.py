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
from threading import Thread, Lock, Event


class Monitor(Thread):
        def __init__(self, client):
            Thread.__init__(self)
            self.daemon=True
            self.listeners=[]
            self.lock = Lock()
            self.wait_event= Event()
            self.running=True
            self.client=client
            self.ses=None
            self.client=client

        def stop(self):
            self.running=False
            self.wait_event.set()

        def add_listener(self, cb):
            with self.lock:
                if not cb in self.listeners:
                    self.listeners.append(cb)
        def remove_listener(self,cb):
            with self.lock:
                try:
                    self.listeners.remove(cb)
                except ValueError:
                    pass

        def remove_all_listeners(self):
            with self.lock:
                self.listeners=[]

        def run(self):
            while (self.running):
                with self.lock:
                    for cb in self.listeners:
                        cb()

                self.wait_event.wait(1.0)