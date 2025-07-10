import os
import config
from src.models.bot.res_codes import ResponseCodes, HttpResponseCode, GatewayCloseCode, GatewayOpCode, VoiceCloseCode, VoiceOpCode, JsonCodes

#-------------------------------------------------------------------------------
#   Check for the configuration files to exist
#-------------------------------------------------------------------------------
def test_main_file_exists() -> None:
    '''
        Test that the main configuration file exists
    '''
    assert os.path.exists('config/conf.yaml')

def test_message_types_config_exists() -> None:
    '''
        Test that the message types configuration file exists
    '''
    assert os.path.exists('config/messageTypes.yaml')

def test_channel_types_config_exists() -> None:
    '''
        Test that the channel types configuration file exists
    '''
    assert os.path.exists('config/channelTypes.yaml')

def test_events_config_exists() -> None:
    '''
        Test that the events configuration file exists
    '''
    assert os.path.exists('config/events.yaml')

#-------------------------------------------------------------------------------
#       Check that the config object is populated correctly
#-------------------------------------------------------------------------------
# @pytest.fixture
# def 

def test_config_variables() -> None:
    '''
        Make sure the variables inside of the config object hold data that is of the correct types
    '''
    config._prepare_config()

    # Check that each variable is the expected type
    assert isinstance(config.RESPONSE_CODES, ResponseCodes)
    assert isinstance(config.MESSAGE_TYPES, dict)
    assert isinstance(config.CHANNEL_TYPES, dict)
    assert isinstance(config.GATEWAY_EVENTS, dict)
    assert isinstance(config.RESPONSE_CODES.http_codes, dict)
    assert isinstance(config.RESPONSE_CODES.http_codes[200], HttpResponseCode)
    assert isinstance(config.RESPONSE_CODES.gateway_op_codes, dict)
    assert isinstance(config.RESPONSE_CODES.gateway_op_codes[0], GatewayOpCode)
    assert isinstance(config.RESPONSE_CODES.gateway_close_codes, dict)
    assert isinstance(config.RESPONSE_CODES.gateway_close_codes[4000], GatewayCloseCode)
    assert isinstance(config.RESPONSE_CODES.voice_op_codes, dict)
    assert isinstance(config.RESPONSE_CODES.voice_op_codes[0], VoiceOpCode)
    assert isinstance(config.RESPONSE_CODES.voice_close_codes, dict)
    assert isinstance(config.RESPONSE_CODES.voice_close_codes[4001], VoiceCloseCode)
    assert isinstance(config.RESPONSE_CODES.json_codes, dict)
    assert isinstance(config.RESPONSE_CODES.json_codes[10001], JsonCodes)

    # Check that each variable holds data
    assert len(config.MESSAGE_TYPES) > 0
    assert len(config.CHANNEL_TYPES) > 0
    assert len(config.GATEWAY_EVENTS) > 0
    assert len(config.RESPONSE_CODES.http_codes) > 0
    assert len(config.RESPONSE_CODES.gateway_op_codes) > 0
    assert len(config.RESPONSE_CODES.gateway_close_codes) > 0
    assert len(config.RESPONSE_CODES.voice_op_codes) > 0
    assert len(config.RESPONSE_CODES.voice_close_codes) > 0
    assert len(config.RESPONSE_CODES.json_codes) > 0


