# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# ayuda - Videos de ayuda y tutoriales para pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ----------------------------------------------------------------------
import os

from channels import youtube_channel
from core import config
from core import logger
from core.item import Item
from platformcode import platformtools

if config.is_xbmc():
    import xbmc

    import xbmcgui

    class TextBox(xbmcgui.WindowXMLDialog):
        """ Create a skinned textbox window """
        def __init__(self, *args, **kwargs):
            self.title = kwargs.get('title')
            self.text = kwargs.get('text')
            self.doModal()

        def onInit(self):
            try:
                self.getControl(5).setText(self.text)
                self.getControl(1).setLabel(self.title)
            except:
                pass

        def onClick(self, control_id):
            pass

        def onFocus(self, control_id):
            pass

        def onAction(self, action):
            # self.close()
            if action in [xbmcgui.ACTION_PREVIOUS_MENU, xbmcgui.ACTION_NAV_BACK]:
                self.close()


def mainlist(item):
    logger.info()
    itemlist = []

    if config.is_xbmc():
        itemlist.append(Item(channel=item.channel, action="", title="FAQ:",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False))
        itemlist.append(Item(channel=item.channel, action="faq",
                             title="    - ¿Se pueden filtrar los enlaces?",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False, extra="filtrar_enlaces"))
        itemlist.append(Item(channel=item.channel, action="faq",
                             title="    - ¿Se pueden activar/desactivar los canales?",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False, extra="onoff_canales"))
        itemlist.append(Item(channel=item.channel, action="faq",
                             title="    - ¿Es posible la sincronización automática con Trakt?",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False, extra="trakt_sync"))
        itemlist.append(Item(channel=item.channel, action="faq",
                             title="    - ¿Es posible mostrar todos los resultados juntos en el buscador global?",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False, extra="buscador_juntos"))
        itemlist.append(Item(channel=item.channel, action="faq",
                             title="    - Los enlaces tardan en aparecer.",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False, extra="tiempo_enlaces"))
        itemlist.append(Item(channel=item.channel, action="faq",
                             title="    - La búsqueda de contenido no se hace correctamente.",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False, extra="prob_busquedacont"))
        itemlist.append(Item(channel=item.channel, action="faq",
                             title="    - Algún canal no funciona correctamente.",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False, extra="canal_fallo"))
        itemlist.append(Item(channel=item.channel, action="faq",
                             title="    - Los enlaces Torrent no funcionan.",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False, extra="prob_torrent"))
        itemlist.append(Item(channel=item.channel, action="faq",
                             title="    - No se actualiza correctamente la biblioteca.",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=True, extra="prob_bib"))
        itemlist.append(Item(channel="ayuda", action="faq",
                             title="    - Aparece un error al pulsar sobre un episodio.",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=True, extra="prob_bib"))
        itemlist.append(Item(channel="ayuda", action="faq",
                             title="    - Otros",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False, extra=""))

    itemlist.append(Item(channel=item.channel, title="Videotutoriales:",
                         thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                         folder=False, action=""))
    itemlist.extend(tutoriales(item))

    if config.is_xbmc():
        itemlist.append(Item(channel=item.channel,
                             action="force_creation_advancedsettings",
                             title="Optimizar fichero advancedsettings.xml",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False))
        itemlist.append(Item(channel=item.channel,
                             action="recover_advancedsettings",
                             title="Restaurar advancedsettings.xml del backup",
                             thumbnail=get_thumbnail_path("thumb_ayuda.png"),
                             folder=False))

    if not config.is_xbmc():
        from core import channeltools
        title = "Activar cuenta real-debrid (No activada)"
        action = "realdebrid"
        token_auth = config.get_setting("token", server="realdebrid")
        if not config.get_setting("premium", server="realdebrid"):
            title = "Activar cuenta real-debrid (Marca la casilla en la ventana de configuración de pelisalacarta para continuar)"
            action = ""
        elif token_auth:
            title = "Activar cuenta real-debrid (Activada correctamente)"
        itemlist.append(Item(channel="ayuda", action=action, title=title))

    return itemlist


def faq(item):

    if item.extra == "filtrar_enlaces":
        respuesta = platformtools.dialog_yesno("pelisalacarta",
                                               "Puedes configurar el filtro en 'Configuración'>Preferencias'>'Otros'.",
                                               "RECOMENDACIÓN: Pon los nombres en minúsculas, "
                                               "sin tildes y separados por una coma y un espacio.",
                                               "¿Deseas abrir las Preferencias ahora?")
        if respuesta == 1:
            from channels import configuracion
            configuracion.settings("")

    elif item.extra == "onoff_canales":
        respuesta = platformtools.dialog_yesno("pelisalacarta",
                                               "Esto se puede hacer en 'Configuración'>'Activar/Desactivar canales'. "
                                               "Puedes activar/desactivar los canales uno por uno o todos a la vez. ",
                                               "¿Deseas gestionar ahora los canales?")
        if respuesta == 1:
            from channels import configuracion
            configuracion.conf_tools(Item(extra='channels_onoff'))

    elif item.extra == "trakt_sync":
        respuesta = platformtools.dialog_yesno("pelisalacarta",
                                               "Actualmente se puede activar la sincronización (silenciosa) "
                                               "tras marcar como visto un episodio (esto se hace automáticamente). "
                                               "Esta opción se puede activar en 'Configuración'>'Ajustes "
                                               "de la biblioteca'.",
                                               "¿Deseas acceder a dichos ajustes?")
        if respuesta == 1:
            from channels import biblioteca
            biblioteca.channel_config(Item(channel='biblioteca'))

    elif item.extra == "tiempo_enlaces":
        respuesta = platformtools.dialog_yesno("pelisalacarta",
                                               "Esto puede mejorarse limitando el número máximo de "
                                               "enlaces o mostrandolos en una ventana emergente. "
                                               "Estas opciones se encuentran en 'Configuración'>'Ajustes "
                                               "de la biblioteca'.",
                                               "¿Deseas acceder a dichos ajustes?")
        if respuesta == 1:
            from channels import biblioteca
            biblioteca.channel_config(Item(channel='biblioteca'))

    elif item.extra == "prob_busquedacont":
        title = "pelisalacarta - FAQ - %s" % item.title[6:]
        text = ("Puede que no hayas escrito la ruta de la librería correctamente en "
                "'Configuración'>'Preferencias'.\n"
                "La ruta a específicada debe ser exactamente la misma de la 'fuente' "
                "introducida en 'Archivos' de la biblioteca de Kodi.\n"
                "AVANZADO: Esta ruta también se encuentra en 'sources.xml'.\n"
                "También puedes estar experimentando problemas por estar "
                "usando algun fork de Kodi y rutas con 'special://'. "
                "SPMC, por ejemplo, tiene problemas con esto, y no parece tener solución, "
                "ya que es un problema ajeno a pelisalacarta que existe desde hace mucho.\n"
                "Puedes intentar subsanar estos problemas en 'Configuración'>'Ajustes de "
                "la biblioteca', cambiando el ajuste 'Realizar búsqueda de contenido en' "
                "de 'La carpeta de cada serie' a 'Toda la biblioteca'."
                "También puedes acudir a 'mimediacenter.info/foro/' en busca de ayuda.")

        return TextBox("DialogTextViewer.xml", os.getcwd(), "Default", title=title, text=text)

    elif item.extra == "canal_fallo":
        title = "pelisalacarta - FAQ - %s" % item.title[6:]
        text = ("Puede ser que la página web del canal no funcione. "
                "En caso de que funcione la página web puede que no seas el primero"
                " en haberlo visto y que el canal este arreglado. "
                "Puedes mirar en 'mimediacenter.info/foro/' o en el "
                "repositorio de GitHub (github.com/pelisalacarta-ce/pelisalacarta-ce). "
                "Si no encuentras el canal arreglado puedes reportar un "
                "problema en el foro.")

        return TextBox("DialogTextViewer.xml", os.getcwd(), "Default", title=title, text=text)

    elif item.extra == "prob_bib":
        platformtools.dialog_ok("pelisalacarta",
                                "Puede ser que hayas actualizado el plugin recientemente "
                                "y que las actualizaciones no se hayan aplicado del todo "
                                "bien. Puedes probar en 'Configuración'>'Otras herramientas', "
                                "comprobando los archivos *_data.json o "
                                "volviendo a añadir toda la biblioteca.")

        respuesta = platformtools.dialog_yesno("pelisalacarta",
                                               "¿Deseas acceder ahora a esa seccion?")
        if respuesta == 1:
            itemlist = []
            from channels import configuracion
            new_item = Item(channel="configuracion", action="submenu_tools", folder=True)
            itemlist.extend(configuracion.submenu_tools(new_item))
            return itemlist

    elif item.extra == "prob_torrent":
        title = "pelisalacarta - FAQ - %s" % item.title[6:]
        text = ("Puedes probar descargando el modulo 'libtorrent' de Kodi o "
                "instalando algun addon como 'Quasar' o 'Torrenter', "
                "los cuales apareceran entre las opciones de la ventana emergente "
                "que aparece al pulsar sobre un enlace torrent. "
                "'Torrenter' es más complejo pero también más completo "
                "y siempre funciona.")

        return TextBox("DialogTextViewer.xml", os.getcwd(), "Default", title=title, text=text)

    elif item.extra == "buscador_juntos":
        respuesta = platformtools.dialog_yesno("pelisalacarta",
                                               "Si. La opcion de mostrar los resultados juntos "
                                               "o divididos por canales se encuentra en "
                                               "'Configuracion'>'Ajustes del buscador global'>"
                                               "'Otros ajustes'.",
                                               "¿Deseas acceder a ahora dichos ajustes?")
        if respuesta == 1:
            from channels import buscador
            buscador.settings("")

    else:
        platformtools.dialog_ok("pelisalacarta",
                                "Tu problema/duda parece no tener una respuesta sencilla. "
                                "")


def get_thumbnail_path(thumb_name):
    import urlparse
    web_path = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/squares/"
    return urlparse.urljoin(web_path, thumb_name)


def tutoriales(item):
    playlists = youtube_channel.playlists(item, "tvalacarta")

    itemlist = []

    for playlist in playlists:
        if playlist.title == "Tutoriales de pelisalacarta":
            itemlist = youtube_channel.videos(playlist)

    return itemlist


def force_creation_advancedsettings(item):
    logger.info()

    # Ruta del advancedsettings
    advancedsettings_kodi = xbmc.translatePath("special://profile/advancedsettings.xml")
    advancedsettings_pelisalacarta = os.path.join(config.get_runtime_path(), "resources",
                                                  "advancedsettings.xml")
    fichero_backup = os.path.join(config.get_data_path(), "original_advancedsettings_backup.xml")

    # Archivos temporales para la modificacion de advancedsettings.xml:
    advancedsettings_same = os.path.join(config.get_data_path(), "same.txt")
    advancedsettings_trans = os.path.join(config.get_data_path(), "trans.txt")

    if os.path.exists(advancedsettings_kodi):
        orig_size = os.path.getsize(advancedsettings_kodi)
    else:
        orig_size = 0

    indent_1 = "\t"
    indent_1_p = "    "
    indent_2 = "\t\t"

    if platformtools.dialog_yesno("AVISO",
                                  "No recomendable para equipos lentos y TV-BOX. Razon: ZeroCache",
                                  "¿Deseas continuar?") == 1:

        if os.path.exists(advancedsettings_kodi) and orig_size != 0:
            logger.info("La ruta de advanced settings del usuario existe!")

            if platformtools.dialog_yesno("pelisalacarta",
                                          "Esto modificará los ajustes avanzados de Kodi.",
                                          "¿Deseas continuar?") == 1:

                # Backup del advancedsettings existente, antes de modificarlo.
                f_origen = open(advancedsettings_kodi)

                if not os.path.exists(fichero_backup):
                    f_backup = open(fichero_backup, "w")

                    for line in f_origen:
                        f_backup.write(line)
                    f_backup.close()
                    platformtools.dialog_notification("pelisalacarta",
                                                      "Backup creado")

                else:
                    if platformtools.dialog_yesno("pelisalacarta",
                                                  "Backup anterior encontrado. ",
                                                  "¿Deseas sobreescribirlo?") == 1:
                        os.remove(fichero_backup)

                        f_backup = open(fichero_backup, "w")

                        for line in f_origen:
                            f_backup.write(line)

                        f_backup.close()

                        platformtools.dialog_notification("pelisalacarta",
                                                          "¡Backup terminado!")
                        logger.info("Backup terminado")
                    else:
                        platformtools.dialog_notification("pelisalacarta",
                                                          "Backup no modificado")
                        logger.info("Backup no modificado")

                f_origen.close()

                # Edicion de advancedsettings.xml
                f_mod = open(os.path.join(advancedsettings_pelisalacarta))
                f_trans = open(os.path.join(advancedsettings_trans), "w")
                f_same = open(os.path.join(advancedsettings_same), "w")
                f_orig = open(os.path.join(advancedsettings_kodi))

                lines_seen = set()
                special_lines_seen = set()
                for line_mod in f_mod:

                    if (line_mod.startswith(("<advancedsettings>",
                                             "</network>",
                                             "</advancedsettings>")) and line_mod
                            not in special_lines_seen):
                        f_same.write(line_mod)

                        if not line_mod.startswith("</network>"):
                            f_trans.write(line_mod)

                        special_lines_seen.add(line_mod)

                    for line_orig in f_orig:
                        # Se borra las indentaciones, ya sean puntos o tabulaciones
                        line_orig = line_orig.replace(indent_1, "").replace(indent_1_p, "")
                        if (line_orig.startswith(("<advancedsettings>",
                                                  "</advancedsettings>")) and line_orig
                                not in special_lines_seen and line_orig not in
                                lines_seen):
                            lines_seen.add(line_orig)

                        if (line_orig == line_mod and line_orig not in lines_seen and
                                line_orig not in special_lines_seen):
                            line_same = line_orig
                            f_same.write(line_same)
                            lines_seen.add(line_orig)

                        if (not line_orig.startswith(("<autodetectpingtime>",
                                                      "<curlclienttimeout>",
                                                      "<curllowspeedtime>",
                                                      "<curlretries>",
                                                      "<disableipv6>",
                                                      "<cachemembuffersize>")) and
                                line_orig not in lines_seen and line_orig not in
                                special_lines_seen):
                            line_trans = line_orig

                            if line_orig.startswith("<network>"):
                                f_same.write(line_orig)

                            f_trans.write(line_trans)
                            lines_seen.add(line_orig)

                f_orig.close()
                f_mod.close()
                f_trans.close()
                f_same.close()

                import filecmp
                if filecmp.cmp(advancedsettings_pelisalacarta, advancedsettings_same):
                    platformtools.dialog_ok("pelisalacarta",
                                            "¡'advancessettings.xml' estaba optimizado!",
                                            "(No sera editado)")
                else:
                    platformtools.dialog_notification("pelisalacarta",
                                                      "modificando advancedsettings.xml...")

                    # Se vacia el advancedsettings.xml del usuario
                    open(os.path.join(advancedsettings_kodi), "w").close

                    nospaces = False
                    f_mod = open(os.path.join(advancedsettings_pelisalacarta))
                    f_trans = open(os.path.join(advancedsettings_trans))
                    f_orig = open(os.path.join(advancedsettings_kodi), "w")

                    exclusion = ["advancedsettings", "/network"]

                    for line_trans in f_trans:
                        if line_trans.startswith("<network>"):
                            for line_mod in f_mod:
                                i = 0
                                for w in exclusion:
                                    if w in line_mod:
                                        i += 1
                                if i == 0:
                                    if "network" in line_mod:
                                        indent = indent_1
                                    else:
                                        indent = indent_2
                                    f_orig.write(indent + line_mod)
                                    logger.info(line_mod)
                        else:
                            if (line_trans.startswith("</advancedsettings>") or
                                    nospaces):
                                line_trans = os.linesep.join([s for s in
                                                             line_trans.splitlines()
                                                             if s])
                                # Se convierten puntos a tabulaciones
                                line_trans = line_trans.replace(indent_1_p, indent_1)
                                f_orig.write(line_trans)
                                nospaces = True
                            else:
                                if "network" in line_trans:
                                    indent = indent_1
                                else:
                                    indent = ""
                                f_orig.write(indent + line_trans)

                    if os.path.getsize(advancedsettings_trans) == 0:
                        for line_mod in f_mod:
                            if "advancedsettings" in line_mod:
                                indent = ""
                            elif "network" in line_mod:
                                indent = indent_1
                            else:
                                indent = indent_2
                            f_orig.write(indent + line_mod)

                    f_trans.close()
                    f_orig.close()

                    platformtools.dialog_notification("pelisalacarta",
                                                      "Modificacion completada")
                f_mod.close()

                if os.path.exists(advancedsettings_same):
                    os.remove(advancedsettings_same)
                if os.path.exists(advancedsettings_trans):
                    os.remove(advancedsettings_trans)
            else:
                platformtools.dialog_notification("pelisalacarta",
                                                  "Operacion cancelada")

        else:
            # Si no hay advancedsettings.xml se copia del directorio resources
            f_optimo = open(advancedsettings_pelisalacarta)
            f_original = open(advancedsettings_kodi, "w")

            for line in f_optimo:
                if "advancedsettings" in line:
                    indent = ""
                elif "network" in line:
                    indent = indent_1
                else:
                    indent = indent_2
                f_original.write(indent + line)

            f_optimo.close()
            f_original.close()

            platformtools.dialog_ok("pelisalacarta",
                                    "Se ha creado un fichero advancedsettings.xml",
                                    "con la configuración óptima para streaming")

        logger.info("Optimizacion finalizada")

    else:
        platformtools.dialog_notification("pelisalacarta",
                                          "Operacion abortada")


def recover_advancedsettings(item):
    logger.info()

    fichero_backup = os.path.join(config.get_data_path(),
                                  "original_advancedsettings_backup.xml")
    advancedsettings_kodi = xbmc.translatePath("special://profile/advancedsettings.xml")

    if platformtools.dialog_yesno("pelisalacarta",
                                  "¿Deseas restaurar el backup de advancedsettings.xml?") == 1:
        if os.path.exists(fichero_backup):
            logger.info("Existe un backup de advancedsettings.xml")

            f_backup = open(fichero_backup)
            open(os.path.join(advancedsettings_kodi), "w").close()
            f_original = open(os.path.join(advancedsettings_kodi), "w")

            for line in f_backup:
                if "</advancedsettings>" in line:
                    line = os.linesep.join([s for s in line.splitlines() if s])
                f_original.write(line)

            f_backup.close()
            f_original.close()

            platformtools.dialog_ok("pelislacarta",
                                    "Backup restaurado correctamente.")

        else:
            logger.info("No hay ningun backup disponible")
            if platformtools.dialog_yesno("pelisalacarta",
                                          "No hay ningun backup disponible. "
                                          "¿Deseas crearlo?") == 1:
                f_origen = open(advancedsettings_kodi)
                f_backup = open(fichero_backup, "w")
                for line in f_origen:
                    f_backup.write(line)
                f_origen.close()
                f_backup.close()

                platformtools.dialog_notification("pelisalacarta", "Backup completado")
            else:
                platformtools.dialog_notification("pelisalacarta", "Backup no creado")

    else:
        platformtools.dialog_notification("pelisalacarta",
                                          "Operacion cancelada por el usuario")
        logger.info("Restauracion de adavancedsettings.xml cancelada")


def realdebrid(item):
    logger.info()
    itemlist = []

    verify_url, user_code, device_code = request_access()

    itemlist.append(Item(channel=item.channel, action="", title="Pasos para realizar la autenticación (Estando logueado en tu cuenta real-debrid):"))
    itemlist.append(Item(channel=item.channel, action="", title="1. Abre el navegador y entra en esta página: %s" % verify_url))
    itemlist.append(Item(channel=item.channel, action="", title='2. Introduce este código y presiona "Allow": %s' % user_code))
    itemlist.append(Item(channel=item.channel, action="authentication", title="--> Pulsa aquí una vez introducido el código <---", extra=device_code))

    return itemlist


def request_access():
    logger.info()
    from core import jsontools
    from core import scrapertools
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    try:
        client_id = "YTWNFBIJEEBP6"

        # Se solicita url y código de verificación para conceder permiso a la app
        url = "http://api.real-debrid.com/oauth/v2/device/code?client_id=%s&new_credentials=yes" % (client_id)
        data = scrapertools.downloadpage(url, headers=headers.items())
        data = jsontools.load_json(data)
        verify_url = data["verification_url"]
        user_code = data["user_code"]
        device_code = data["device_code"]

        return verify_url, user_code, device_code
    except:
        import traceback
        logger.error(traceback.format_exc())
        return "", "", ""


def authentication(item):
    logger.info()
    import urllib
    from core import channeltools
    from core import jsontools
    from core import scrapertools

    itemlist = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    client_id = "YTWNFBIJEEBP6"
    device_code = item.extra
    token = ""
    try:
        url = "https://api.real-debrid.com/oauth/v2/device/credentials?client_id=%s&code=%s" \
              % (client_id, device_code)
        data = scrapertools.downloadpage(url, headers=headers.items())
        data = jsontools.load_json(data)

        debrid_id = data["client_id"]
        secret = data["client_secret"]

        # Se solicita el token de acceso y el de actualización para cuando el primero caduque
        post = urllib.urlencode({"client_id": debrid_id, "client_secret": secret, "code": device_code,
                                 "grant_type": "http://oauth.net/grant_type/device/1.0"})
        data = scrapertools.downloadpage("https://api.real-debrid.com/oauth/v2/token", post=post,
                                         headers=headers.items())
        data = jsontools.load_json(data)

        token = data["access_token"]
        refresh = data["refresh_token"]

        config.set_setting("id", debrid_id, server="realdebrid")
        config.set_setting("secret", secret, server="realdebrid")
        config.set_setting("token", token, server="realdebrid")
        config.set_setting("refresh", refresh, server="realdebrid")

    except:
        import traceback
        logger.error(traceback.format_exc())

    if token:
        itemlist.append(Item(channel=item.channel, action="", title="Cuenta activada correctamente"))
    else:
        itemlist.append(Item(channel=item.channel, action="", title="Error en el proceso de activación, vuelve a intentarlo"))

    return itemlist
