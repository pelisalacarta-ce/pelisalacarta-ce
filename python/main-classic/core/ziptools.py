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
# --------------------------------------------------------------------------------
# Zip Tools
# --------------------------------------------------------------------------------

import os
import zipfile

import logger
import config


class ziptools:

    def extract(self, file, dir, folder_to_extract="", overwrite_question=False, backup=False):
        logger.info("file=%s" % file)
        logger.info("dir=%s" % dir)
        
        if not dir.endswith(':') and not os.path.exists(dir):
            os.mkdir(dir)

        zf = zipfile.ZipFile(file)
        if not folder_to_extract:
            self._createstructure(file, dir)
        num_files = len(zf.namelist())

        for name in zf.namelist():
            logger.info("name=%s" % name)
            if not name.endswith('/'):
                logger.info("no es un directorio")
                try:
                    (path,filename) = os.path.split(os.path.join(dir, name))
                    logger.info("path=%s" % path)
                    logger.info("name=%s" % name)
                    if folder_to_extract:
                        if path != os.path.join(dir, folder):
                            break
                    else:
                        os.makedirs( path )
                except:
                    pass
                if folder_to_extract:
                    outfilename = os.path.join(dir, filename)
                    
                else:
                    outfilename = os.path.join(dir, name)
                logger.info("outfilename=%s" % outfilename)
                try:
                    if os.path.exists(outfilename) and overwrite_question:
                        from platformcode import platformtools
                        dyesno = platformtools.dialog_yesno("El archivo ya existe",
                                                            "El archivo %s a descomprimir ya existe" \
                                                            ", ¿desea sobrescribirlo?" \
                                                            % os.path.basename(outfilename))
                        if not dyesno:
                            break
                        if backup:
                            import time
                            import shutil
                            hora_folder = "Copia seguridad [%s]" % time.strftime("%d-%m_%H-%M", time.localtime())
                            backup = os.path.join(config.get_data_path(), 'backups', hora_folder, folder_to_extract)
                            if not os.path.exists(backup):
                                os.makedirs(backup)
                            shutil.copy2(outfilename, os.path.join(backup, os.path.basename(outfilename)))
                        
                    outfile = open(outfilename, 'wb')
                    outfile.write(zf.read(name))
                except:
                    logger.error("Error en fichero "+name)

    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)

    def create_necessary_paths(filename):
        try:
            (path,name) = os.path.split(filename)
            os.makedirs( path)
        except:
            pass

    def _makedirs(self, directories, basedir):
        for dir in directories:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)

    def _listdirs(self, file):
        zf = zipfile.ZipFile(file)
        dirs = []
        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)

        dirs.sort()
        return dirs
