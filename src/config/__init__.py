import yaml
from yaml import Loader
from models.bot.res_codes import ResponseCodes

# on import this file is executed, so the RESPONSE_CODES object is created and populated
OPTS = {
                'appId': int,
                'permissionInteger': int,
                'botToken': str,
                'commandPrefix': str,
                'logFile': str,
                'logLevel': str,
                'logMaxBytes': int
            }

RESPONSE_CODES = ResponseCodes()
MESSAGE_TYPES = dict()
CHANNEL_TYPES = dict()
GATEWAY_EVENTS = dict()


def _prepare_config():
    #-----------------------------------------------------------
    #   Load main config file
    #-----------------------------------------------------------
    with open('/etc/squirrel_bot/config.yaml','r+') as c_file:
        config_opts = yaml.load(c_file, Loader=Loader)

        if isinstance(config_opts, dict):
            for conf_key,conf_val in config_opts.items():
                if conf_key in OPTS.keys():
                    OPTS[conf_key] = conf_val
                else:
                    continue
        else:
            print("Invalid config file: ../conf.yaml")
            return
    
    #-----------------------------------------------------------
    #   Load MessageTypes
    #-----------------------------------------------------------
    with open('config/messageTypes.yaml', 'r+') as m_file:
        msgTypes = yaml.load(m_file, Loader=Loader)

        for mType in msgTypes:
            MESSAGE_TYPES[mType['type']] = {
                'value': mType['value'],
                'deleteable': mType['deleteable']
            }

    #-----------------------------------------------------------
    #   Load ChannelTypes
    #-----------------------------------------------------------
    with open('config/channelTypes.yaml', 'r+') as c_file:
        chanTypes = yaml.load(c_file, Loader=Loader)

        for cType in chanTypes:
            CHANNEL_TYPES[cType['value']] = {
                'type': cType['type'],
                'description': cType['description']
            }

    #-----------------------------------------------------------
    #   Load Gateway Events
    #-----------------------------------------------------------
    with open('config/events.yaml', 'r+') as g_file:
        events = yaml.load(g_file, Loader=Loader)

        for event in events:
            GATEWAY_EVENTS[event['type']] = {
                'handler': event['handler']
            }