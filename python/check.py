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
# Tester
# ------------------------------------------------------------
import fnmatch
import os
import re
if os.path.isfile("result.log"): os.remove("result.log")
lastfile = ""

def print_error(line, patern, file):
  global lastfile
  line +=1
  if not lastfile == file:
    lastfile = file
    open("result.log", "a+").write('\n{:55s} {:s}\n'.format(file, "-"*80 ) ) 
    open("result.log", "a+").write('{:55s} {:^5s} {:^5s}   {:^70s}\n'.format("", "Linea", "Tipo", "Contenido" ) ) 
    open("result.log", "a+").write('{:55s} {:s}\n'.format("", "-"*80 ) ) 

  open("result.log", "a+").write('{:55s} {:5d} {:5s}   {:s}\n'.format("", line, "ERROR", patern.strip() ) ) 


def compatibility_check(file):
  data = open(file, "rb").read()
  #if else en la misma linea
  p = re.compile("^[^\r\n#]*=[^\r\n]*if [^\r\n]* else[^\r\n]*", re.MULTILINE)
  for m in p.finditer(data):
    lines = data[:m.start()].splitlines()
    print_error(len(lines), m.group(), file)
  
  #Uso de .format{}  
  p = re.compile("^[^\r\n#]*=[^\r\n]*.format{[^\r\n]*", re.MULTILINE)
  for m in p.finditer(data):
    lines = data[:m.start()].splitlines()
    print_error(len(lines), m.group(), file)

  #Uso diccionario por compresion  
  p = re.compile("^[^\r\n#]*\{[^\r\n]* for [^\r\n]*\}[^\r\n]*", re.MULTILINE)
  for m in p.finditer(data):
    lines = data[:m.start()].splitlines()
    print_error(len(lines), m.group(), file)
      
  #with open(...) as f:
  p = re.compile("^[^\r\n#]*with [^\r\n]+ as [^\:\r\n]+\:[^\r\n]*", re.MULTILINE)
  for m in p.finditer(data):
    lines = data[:m.start()].splitlines()
    print_error(len(lines), m.group(), file)

  #Thread.is_alive() deve ser sustituido por Thread.isAlive() 
  p = re.compile("^[^\r\n#]*.is_alive()[^\r\n]*", re.MULTILINE)
  for m in p.finditer(data):
    lines = data[:m.start()].splitlines()
    print_error(len(lines), m.group(), file)

files = []
for root, dirnames, filenames in os.walk('main-classic'):
    for filename in fnmatch.filter(filenames, '*.py'):
        files.append(os.path.join(root, filename))



for file in files:
  print "Comprobando %s..." % file
  compatibility_check(file)


