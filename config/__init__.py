import yaml
from yaml import Loader
from src.models.bot.res_codes import ResponseCodes

# on import this file is executed, so the RESPONSE_CODES object is created and populated
OPTS = {
            'appId': int,
            'permissionInteger': int,
            'botToken': str,
            'commandPrefix': str,
            'logFile': dict,
            'logLevel': str,
            'logMaxBytes': int,
            'database': dict
        }

RESPONSE_CODES = ResponseCodes()
MESSAGE_TYPES = dict()
CHANNEL_TYPES = dict()
GATEWAY_EVENTS = dict()


def _prepare_config():
    #-----------------------------------------------------------
    #   Load main config file
    #-----------------------------------------------------------
    with open('config/conf.yaml','r+') as c_file:
        config_opts = yaml.load(c_file, Loader=Loader)

        if isinstance(config_opts, dict):
            for conf_key,conf_val in config_opts.items():
                if conf_key in OPTS.keys():
                    OPTS[conf_key] = conf_val
                else:
                    continue
            if not isinstance(OPTS['database'], dict):
                OPTS['database'] = None
        else:
            print("Invalid config file: config/conf.yaml")
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
            if event['handler'] == "DB" and OPTS['database'] is None:
                print(f"Skipping event {event['type']} as it requires a database but none is configured.")
                continue

            GATEWAY_EVENTS[event['type']] = {
                'handler': event['handler']
            }