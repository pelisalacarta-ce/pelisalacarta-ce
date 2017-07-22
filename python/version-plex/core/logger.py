# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Logger
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import bridge

def encode_log(message=""):
    # Unicode to utf8
    if type(message) == unicode:
        message = message.encode("utf8")

    # All encodings to utf8
    elif type(message) == str:
        message = unicode(message, "utf8", errors="replace").encode("utf8")

    # Objects to string
    else:
        message = str(message)

    return message

def get_caller(message=None):
    import inspect
    module = "pelisalacarta."  + inspect.getmodule(inspect.currentframe().f_back.f_back).__name__
    #function = inspect.currentframe().f_code.co_name
    function = inspect.currentframe().f_back.f_back.f_code.co_name
    #bridge.log_info(module)
    if message:
        message = encode_log(message)
        if module not in message:
            if function == "<module>":
                return module + " " + message
            else:
                return module + " [" + function + "] " + message
        else:
            return message

    else:
        if function == "<module>":
            return module
        else:
            return module + "." + function


def info(texto=""):
    try:
        bridge.log_info(get_caller(texto))
    except:
        pass
    
def debug(texto=""):
    try:
        bridge.log_info("######## DEBUG #########",'Debug')
        bridge.log_info(get_caller(texto),'Debug')
    except:
        pass

def error(texto=""):
    try:
        bridge.log_info("######## ERROR #########",'Error')
        bridge.log_info(get_caller(texto),'Error')
    except:
        pass
