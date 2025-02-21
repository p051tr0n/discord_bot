import config
import json
from tornado.httpclient import HTTPRequest


class RequestObject(object):
    '''
        Object to hold the data for an HTTP request.
    '''
    __slots__ = ('url', 'uri', 'method', 'headers', 'body')

    def __init__(self):
        self.url = "https://discord.com/api/v10"
        self.uri = ""
        self.method = ""
        self.headers = {"Authorization": f"Bot {config.OPTS['botToken']}"}
        self.body = ""

    #-------------------------------------------------------------------------------------------
    def _to_dict(self):
        '''
            Convert the object to a dictionary.
        '''
        return {
            "url": self.url,
            "uri": self.uri,
            "method": self.method,
            "headers": self.headers,
            "body": self.body
        }

    #-------------------------------------------------------------------------------------------
    def __str__(self):
        '''
            String representation of the object.
        '''
        return f"URL: {self.url}\nMETHOD: {self.method}\nHEADERS: {self.headers}\nDATA: {self.data}"

    #-------------------------------------------------------------------------------------------
    def _to_request(self):
        '''
            Convert the object to a request object.
        '''
        return HTTPRequest(url=f"{self.url}{self.uri}",
                            method=self.method,
                            headers=self.headers,
                            body=self.body)