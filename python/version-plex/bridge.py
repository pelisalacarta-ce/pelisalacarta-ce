from core import servertools
from core import channeltools
from core.item import Item
# Passing log and config to an external library
# All credits to: https://gist.github.com/mikew/5011984

# Contents/Libraries/Shared/bridge.py
logger = None
config = None
localized_strings = None
dict_global = None

def init(log, pref, locale, d_global):
    global config,logger,localized_strings,dict_global
    config = pref
    logger = log
    localized_strings = locale
    dict_global = d_global

def log_info(texto, level='Info'):
    global logger
    if level.lower() == 'debug':
        logger.Debug(texto)
    elif level.lower() == 'error':
        logger.Error(texto)
    else:
        logger(texto)

def get_setting(name):
    global config, dict_global
    try:
        value = config[name]
    except:
        value = dict_global[name]

    return value if value else ""


def get_localized_string(code):
    return localized_strings.LocalString(code)

'''
Using:

# Contents/Libraries/Shared/library.py
import bridge
 
def test():
    # this will log to com.plexapp.plugin.foo.log
    bridge.config['Dict']['foo'] = 'bar'
    bridge.config['Log']('Dict[foo] is %s' % config['Dict']['foo'])
'''