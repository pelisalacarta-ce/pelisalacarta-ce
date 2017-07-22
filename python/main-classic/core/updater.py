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
# Updater process
# --------------------------------------------------------------------------------

import os
import time

import config
import logger
import scrapertools
import versiontools

def update(item):
    logger.info()

def update_channel(channel_name):
    logger.info(channel_name)
    
    import channeltools
    remote_channel_url , remote_version_url = channeltools.get_channel_remote_url(channel_name)
    local_channel_path , local_version_path , local_compiled_path = channeltools.get_channel_local_path(channel_name)
    
    # Version remota
    try:
        data = scrapertools.cachePage( remote_version_url )
        logger.info("remote_data="+data)
        remote_version = int( scrapertools.find_single_match(data,'<version>([^<]+)</version>') )
        addon_condition = int(scrapertools.find_single_match(data, "<addon_version>([^<]*)</addon_version>")
                              .replace(".", "").ljust(len(str(versiontools.get_current_plugin_version())), '0'))
    except:
        remote_version = 0
        addon_condition = 0

    logger.info("remote_version=%d" % remote_version)

    # Version local
    if os.path.exists( local_version_path ):
        infile = open( local_version_path )
        data = infile.read()
        infile.close()
        #logger.info("pelisalacarta.core.updater local_data="+data)

        local_version = int( scrapertools.find_single_match(data,'<version>([^<]+)</version>') )
    else:
        local_version = 0

    logger.info("local_version=%d" % local_version)

    # Comprueba si ha cambiado
    updated = (remote_version > local_version) and (versiontools.get_current_plugin_version() >= addon_condition)

    if updated:
        logger.info("downloading...")
        download_channel(channel_name)

    return updated

def download_channel(channel_name):
    logger.info(channel_name)

    import channeltools
    remote_channel_url , remote_version_url = channeltools.get_channel_remote_url(channel_name)
    local_channel_path , local_version_path , local_compiled_path = channeltools.get_channel_local_path(channel_name)

    # Descarga el canal
    try:
        updated_channel_data = scrapertools.cachePage( remote_channel_url )
        outfile = open(local_channel_path,"wb")
        outfile.write(updated_channel_data)
        outfile.flush()
        outfile.close()
        logger.info("Grabado a " + local_channel_path)
    except:
        import traceback
        logger.error(traceback.format_exc())

    # Descarga la version (puede no estar)
    try:
        updated_version_data = scrapertools.cachePage( remote_version_url )
        outfile = open(local_version_path,"w")
        outfile.write(updated_version_data)
        outfile.flush()
        outfile.close()
        logger.info("Grabado a " + local_version_path)
    except:
        import traceback
        logger.error(traceback.format_exc())

    if os.path.exists(local_compiled_path):
        os.remove(local_compiled_path)

    from platformcode import platformtools
    platformtools.dialog_notification(channel_name+" actualizado", "Se ha descargado una nueva versión")

