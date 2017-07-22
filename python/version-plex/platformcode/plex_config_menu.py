# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de vídeos descargados
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# venta de configuración por canales para PLEX


import os
import re
from core import logger
from core import config
from core.item import Item
from core import jsontools as json
from core import channeltools
import inspect

__channel__ ="platformcode.plex_config_menu"

params = {}
    
def isGeneric():
    return True 


def show_channel_settings(list_controls=None, dict_values=None, caption="", callback=None,item=None, custom_button= None, channelpath= None, kwargs=None, ch_type=None):
    ''' Funcion que permite utilizar cuadros de configuracion personalizados.
    
    show_channel_settings(listado_controles, dict_values, caption, callback, item)
            Parametros:
                listado_controles: (list) Lista de controles a incluir en la ventana, segun el siguiente esquema:
                    (opcional)list_controls= [
                                {'id': "nameControl1",
                                  'type': "bool",                       # bool, text, list, label 
                                  'label': "Control 1: tipo RadioButton",
                                  'color': '0xFFee66CC',                # color del texto en formato ARGB hexadecimal
                                  'default': True,
                                  'enabled': True,
                                  'visible': True
                                },
                                {'id': "nameControl2",
                                  'type': "text",                       # bool, text, list, label 
                                  'label': "Control 2: tipo Cuadro de texto",
                                  'color': '0xFFee66CC',
                                  'default': "Valor por defecto",
                                  'hidden': False,                      # only for type = text Indica si hay que ocultar el texto (para passwords)
                                  'enabled': True,
                                  'visible': True
                                },
                                {'id': "nameControl3",
                                  'type': "list",                       # bool, text, list, label 
                                  'label': "Control 3: tipo Lista",
                                  'color': '0xFFee66CC',
                                  'default': 0,                         # Indice del valor por defecto en lvalues 
                                  'enabled': True,
                                  'visible': True,
                                  'lvalues':["item1", "item2", "item3", "item4"],  # only for type = list
                                },
                                {'id': "nameControl4",
                                  'type': "label",                       # bool, text, list, label 
                                  'label': "Control 4: tipo Etiqueta",
                                  'color': '0xFFee66CC',               
                                  'enabled': True,
                                  'visible': True
                                }]
                    Si no se incluye el listado_controles, se intenta obtener del xml del canal desde donde se hace la llamada. 
                    El formato de los controles en el xml es:
                        <?xml version="1.0" encoding="UTF-8" ?>
                        <channel>
                            ...
                            ...
                            <settings>
                                <id>nameControl1</id>
                                <type>bool</type>
                                <label>Control 1: tipo RadioButton</label>
                                <default>false</default>
                                <enabled>true</enabled>
                                <visible>true</visible>
                                <color>0xFFee66CC</color>
                            </settings>
                            <settings>
                                <id>nameControl2</id>
                                <type>text</type>
                                <label>Control 2: tipo Cuadro de texto</label>
                                <default>Valor por defecto</default>
                                <hidden>true</hidden>
                                <enabled>true</enabled>
                                <visible>true</visible>
                                <color>0xFFee66CC</color>
                            </settings>
                            <settings>
                                <id>nameControl3</id>
                                <type>list</type>
                                <label>Control 3: tipo Lista</label>
                                <default>0</default>
                                <enabled>true</enabled>
                                <color>0xFFee66CC</color>
                                <visible>true</visible>
                                <lvalues>item1</lvalues>
                                <lvalues>item2</lvalues>
                                <lvalues>item3</lvalues>
                                <lvalues>item4</lvalues>
                            </settings>
                            <settings>
                                <id>nameControl4</id>
                                <type>label</type>
                                <label>Control 4: tipo Etiqueta</label>
                                <enabled>true</enabled>
                                <visible>true</visible>
                                <color>0xFFee66CC</color>
                            </settings>
                            ...
                        </channel>  
                    
                    
                    Los campos 'label', 'default' y 'lvalues' pueden ser un numero precedido de '@'. En cuyo caso se buscara el literal en el archivo string.xml del idioma seleccionado.
                    Los campos 'enabled' y 'visible' admiten los comparadores eq(), gt() e it() y su funcionamiento se describe en: http://kodi.wiki/view/Add-on_settings#Different_types
                    Por el momento en PLEX, tanto si quedan disabled, como no visible, los ocultamos (quitandolos del itemlist)
                    Los campos hidden y color no tienen utilidad en PLEX
                    
                (opcional)dict_values: (dict) Diccionario que representa el par (id: valor) de los controles de la lista.
                    Si algun control de la lista no esta incluido en este diccionario se le asignara el valor por defecto.
                        dict_values={"nameControl1": False,
                                     "nameControl2": "Esto es un ejemplo"}
                
                (opcional) caption: (str) Titulo de la ventana de configuracion. Se puede localizar mediante un numero precedido de '@'
                (opcional) callback (str) Nombre de la funcion, del canal desde el que se realiza la llamada, que sera invocada al pulsar 
                    el boton aceptar de la ventana. A esta funcion se le pasara como parametros el objeto 'item' y el dicionario 'dict_values'
            Retorno: Si se especifica 'callback' se devolvera lo que devuelva esta funcion. Si no devolvera None     
    
    Ejemplos de uso:
        platformtools.show_channel_settings(): Así tal cual, sin pasar ningún argumento, la ventana detecta de que canal se ha hecho la llamada, 
            y lee los ajustes del XML y carga los controles, cuando le das a Aceptar los vuelve a guardar.
        
        return platformtools.show_channel_settings(list_controls=list_controls, dict_values=dict_values, callback='cb', ítem=ítem):
            Así abre la ventana con los controles pasados y los valores de dict_values, si no se pasa dict_values, carga los valores por defecto de los controles, 
            cuando le das a aceptar, llama a la función 'cb' del canal desde donde se ha llamado, pasando como parámetros, el ítem y el dict_values    
    
    '''
    logger.info()
    global params
    itemlist = []

    #Cuando venimos de hacer click en un control de la ventana, channelname ya se pasa como argumento, si no lo tenemos, detectamos de donde venimos
    if not channelpath:
        channelpath = inspect.currentframe().f_back.f_back.f_code.co_filename
    channelname = os.path.basename(channelpath).replace(".py", "")
    ch_type = os.path.basename(os.path.dirname(channelpath))
    kwargs = {}

    #Si no tenemos list_controls, hay que sacarlos del xml del canal
    if not list_controls:

        #Si la ruta del canal esta en la carpeta "channels", obtenemos los controles y valores mediante chaneltools
        if os.path.join(config.get_runtime_path(), "channels") in channelpath:

            # La llamada se hace desde un canal
            list_controls, default_values = channeltools.get_channel_controls_settings(channelname)
            kwargs = {"channel": channelname}
          
        #Si la ruta del canal esta en la carpeta "servers", obtenemos los controles y valores mediante servertools
        elif os.path.join(config.get_runtime_path(), "servers") in channelpath:
            # La llamada se hace desde un server
            list_controls, default_values = servertools.get_server_controls_settings(channelname)
            kwargs = {"server": channelname}

        #En caso contrario salimos
        else:
            return itemlist

    #Si no se pasan dict_values, creamos un dict en blanco
    if  dict_values == None:
        dict_values = {}

    if type(custom_button) == dict:
        custom_button = {"label"    : custom_button.get("label", ""),
                         "function" : custom_button.get("function", ""),
                         "visible"  : bool(custom_button.get("visible", True)),
                         "close"    : bool(custom_button.get("close", False))}

    else:
        custom_button = None

    #Ponemos el titulo
    if caption =="":
        caption = str(config.get_localized_string("30100")) + " -- " + channelname.capitalize()
    elif caption.startswith('@') and unicode(caption[1:]).isnumeric():
        caption = config.get_localized_string(int(caption[1:]))


    # Añadir controles
    for c in list_controls:

        #Obtenemos el valor
        if not c["id"] in dict_values:
            if not callback:
                dict_values[c["id"]]= config.get_setting(c["id"], **kwargs)
            else:
                if not 'default' in c: c["default"] = ''
                dict_values[c["id"]] = c["default"]


        # Translation
        if c['label'].startswith('@') and unicode(c['label'][1:]).isnumeric():
            c['label'] = str(config.get_localized_string(c['label'][1:]))
        if c["label"].endswith (":"): c["label"] = c["label"][:-1]

        if c['type'] == 'list':
            lvalues=[]
            for li in c['lvalues']:
                if li.startswith('@') and unicode(li[1:]).isnumeric():
                    lvalues.append(str(config.get_localized_string(li[1:])))
                else:
                    lvalues.append(li)
            c['lvalues'] = lvalues


        #Tipos de controles
        if c['type'] == 'label':
            titulo = c["label"]
            itemlist.append(Item(channel=__channel__, action="control_label_click", title=titulo, extra=list_controls.index(c)))

        if c['type'] == 'bool':
            titulo = c["label"] + ":" + (' ' * 5) + ("[X]" if dict_values[c["id"]] else "[  ]")
            itemlist.append(Item(channel=__channel__, action="control_bool_click", title=titulo, extra=list_controls.index(c)))

        elif c['type'] == 'list':
            titulo = c["label"] + ":" + (' ' * 5) + str(c["lvalues"][dict_values[c["id"]]])
            itemlist.append(Item(channel=__channel__, action="control_list_click", title=titulo, extra=list_controls.index(c)))

        elif c['type'] == 'text':
            titulo = c["label"] + ":" + (' ' * 5) + str(dict_values[c["id"]])
            item= Item(channel=__channel__, action="control_text_click", title=titulo, extra=list_controls.index(c))
            item.type = "input"
            item.value = dict_values[c["id"]]
            itemlist.append(item)



    params = {"list_controls":list_controls, "dict_values":dict_values, "caption":caption, "channelpath":channelpath, "callback":callback, "item":item, "custom_button": custom_button, "kwargs": kwargs, "ch_type": ch_type}
    if itemlist:

        #Creamos un itemlist nuevo añadiendo solo los items que han pasado la evaluacion
        evaluated = []
        for x in range(len(list_controls)):
            #por el momento en PLEX, tanto si quedan disabled, como no visible, los ocultamos (quitandolos del itemlist)
            visible = evaluate(x, list_controls[x]["enabled"]) and evaluate(x, list_controls[x]["visible"])
            if visible:
                evaluated.append(itemlist[x])

        # Añadir Titulo
        evaluated.insert(0,Item(channel=__channel__, action="control_label_click", title=caption))
        # Añadir item aceptar y cancelar
        evaluated.append(Item(channel=__channel__, action="ok_Button_click", title="Aceptar"))
        evaluated.append(Item(channel=channelname, action="mainlist", title="Cancelar"))

        if custom_button is None:
            evaluated.append(Item(channel=__channel__, action="default_Button_click", title="Por defecto"))
        else:
            if custom_button['visible'] == True:
                evaluated.append(Item(channel=__channel__, action="default_Button_click", title=custom_button["label"]))


    return evaluated

#Funcion encargada de evaluar si un control tiene que estar oculto o no
def evaluate(index,cond):
    global params

    list_controls = params["list_controls"]
    dict_values = params["dict_values"]

    #Si la condicion es True o False, no hay mas que evaluar, ese es el valor
    if type(cond)== bool: return cond

    #Si la condicion es un str representando un boleano devolvemos el valor
    if cond.lower() == "true":
        return True
    elif cond.lower() == "false":
        return False

    #Obtenemos las condiciones
    conditions =  re.compile("(!?eq|!?gt|!?lt)?\(([^,]+),[\"|']?([^)|'|\"]*)['|\"]?\)[ ]*([+||])?").findall(cond)

    for operator, id, value, next in conditions:

        #El id tiene que ser un numero, sino, no es valido y devuelve False
        try:
            id = int(id)
        except:
            return False

        #El control sobre el que evaluar, tiene que estar dentro del rango, sino devuelve False
        if index + id < 0 or index + id >= len(list_controls):
            return False

        else:
            #Obtenemos el valor del control sobre el que se compara
            c =  list_controls[index + id]

            id = c["id"]
            control_value = dict_values[id]



        #Operaciones lt "menor que" y gt "mayor que", requieren que las comparaciones sean numeros, sino devuelve False
        if operator in ["lt","!lt","gt","!gt"]:
            try:
                value = int(value)
            except:
                return False

        #Operacion eq "igual a" puede comparar cualquier cosa, como el valor lo obtenemos mediante el xml no sabemos su tipo (todos son str) asi que
        #intentamos detectarlo
        if operator in ["eq","!eq"]:
            #valor int
            try:
                value = int(value)
            except:
                pass

            #valor bool
            if value.lower() == "true": value = True
            elif value.lower() == "false": value = False


        #operacion "eq" "igual a"
        if operator =="eq":
            if control_value == value:
                ok = True
            else:
                ok = False

        #operacion "!eq" "no igual a"
        if operator =="!eq":
            if not control_value == value:
                ok = True
            else:
                ok = False

        #operacion "gt" "mayor que"
        if operator =="gt":
            if control_value > value:
                ok = True
            else:
                ok = False

        #operacion "!gt" "no mayor que"
        if operator =="!gt":
            if not control_value > value:
                ok = True
            else:
                ok = False

                #operacion "lt" "menor que"
        if operator =="lt":
            if control_value < value:
                ok = True
            else:
                ok = False

        #operacion "!lt" "no menor que"
        if operator =="!lt":
            if not control_value < value:
                ok = True
            else:
                ok = False

        #Siguiente operación, si es "|" (or) y el resultado es True, no tiene sentido seguir, es True
        if next == "|" and ok ==True: break
        #Siguiente operación, si es "+" (and) y el resultado es False, no tiene sentido seguir, es False
        if next == "+" and ok ==False: break

        #Siguiente operación, si es "+" (and) y el resultado es True, Seguira, para comprobar el siguiente valor
        #Siguiente operación, si es "|" (or) y el resultado es False, Seguira, para comprobar el siguiente valor

    return ok


#Bool, invierte el valor
def control_bool_click(item):
    itemlist = []
    global params

    c = params["list_controls"][item.extra]
    params["dict_values"][c["id"]] = not params["dict_values"][c["id"]]

    return show_channel_settings(**params)


#Opciones del List, cambia el valor por el seleccionado    
def cambiar_valor(item):
    global params

    c = params["list_controls"][item.extra]
    params["dict_values"][c["id"]] = item.new_value

    return show_channel_settings(**params)


#Lists, Muestra las opciones disponibles                                
def control_list_click(item):
    itemlist = []
    global params

    c = params["list_controls"][item.extra]
    value = params["dict_values"][c["id"]]

    for i in c["lvalues"]:
        titulo = (' ' * 5) +str(i) if c["lvalues"].index(i) != value else "[X] " + str(i)
        itemlist.append(Item(channel=__channel__, title=titulo, action="cambiar_valor", extra= item.extra, new_value= c["lvalues"].index(i)))
    return itemlist


#Inputs, guarda el nuevo valor tecleado
def control_text_click(item, new_value=""):
    global params

    c = params["list_controls"][item.extra]
    params["dict_values"][c["id"]] = new_value
    return show_channel_settings(**params)


#Labels, al hacer click, recarga el listado de controles
def control_label_click (item):
    global params

    return show_channel_settings(**params)


#Boton Aceptar, llama a la funcion callback o cb_validate_config si existen, con el item como primer argumento
# y dict_values como segundo. Si no existen guarda los valores de dict_values.
def ok_Button_click(item):
    global params
    itemlist = []

    list_controls = params["list_controls"]
    dict_values = params["dict_values"]
    channel = os.path.basename(params["channelpath"]).replace(".py", "")
    callback = params["callback"]
    ch_type = params["ch_type"]
    item = params["item"]

    if callback and '.' in callback:
        package, callback = callback.rsplit('.', 1)
    else:
        package = '%s.%s' % (ch_type, channel)

    cb_channel = None
    try:
        cb_channel = __import__(package, None, None, [package])
    except ImportError:
        logger.error('Imposible importar %s' % package)

    if callback:
        # Si existe una funcion callback la invocamos ...
        itemlist = getattr(cb_channel, callback)(item, dict_values)
    else:
        # si no, probamos si en el canal existe una funcion 'cb_validate_config' ...
        try:
            itemlist = getattr(cb_channel, 'cb_validate_config')(item, dict_values)
        except AttributeError:
            # ... si tampoco existe 'cb_validate_config'...
            for v in dict_values:
                config.set_setting(v, dict_values[v], **kwargs)

    if not itemlist:
        itemlist = getattr(cb_channel, 'mainlist')(item)

    return itemlist

#Para restablecer los controles al valor por defecto     
def default_Button_click(item):
    global params

    list_controls = params["list_controls"]
    dict_values = params["dict_values"]
    custom_button = params["custom_button"]
    item = params["item"]
    channel = os.path.basename(params["channelpath"]).replace(".py", "")
    ch_type = params["ch_type"]
    callback = params["callback"]
    
    if custom_button is not None:
        if callback and '.' in callback:
            package, callback = callback.rsplit('.', 1)
        else:
            package = '%s.%s' % (ch_type, channel)
        try:
            cb_channel = __import__(package, None, None, [package])
        except ImportError:
            logger.error('Imposible importar %s' % channel)
        else:
            return_value =  getattr(cb_channel, custom_button['function'])(item, dict_values)

            if custom_button["close"] == True:
                if not type(return_value)== list:
                    return_value = getattr(cb_channel, "mainlist")(item)
                return return_value

            else:
                if isinstance(return_value, dict) and return_value.has_key("label"):
                    custom_button["label"]= return_value['label']
                return show_channel_settings(**params)

    else:

        for c in list_controls:
            if not 'default' in c: c["default"] = ''
            dict_values[c["id"]] = c["default"]

        return show_channel_settings(**params)
    