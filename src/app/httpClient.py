import asyncio
import config
import json
import queue
import time
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClientError

from multiprocessing import Process, JoinableQueue
from models.procs.event import ProcessEvent, LogEvent
from functions.botListeners import BotListeners

__all__ = ['HttpClient', 'RequestClient']

class HttpClient(Process):

    __slots__ = ('botQueue', 'logQueue', 'httpQueue', 'requestQueue', 'requestClient', 'botListeners')

    def __init__(self, botQueue, logQueue, httpQueue):
        super().__init__()
        self.botQueue: JoinableQueue = botQueue
        self.logQueue: JoinableQueue = logQueue
        self.httpQueue: JoinableQueue = httpQueue
        self.requestQueue: JoinableQueue = JoinableQueue()
        self.requestClient = RequestClient(self.requestQueue, self.logQueue)
        self.botListeners = BotListeners()

    #-------------------------------------------------------------------------------------------
    def run(self) -> None:
        '''
            The object retrieved off of the http queue will be an HttpEvent object.

            HttpEvent.action = "HTTP"
            HttpEvent.name = Will be the 't' field of the GatewayEvent object
            HttpEvent.data = A BaseResource object created from the 'd' field of a Gateway Event object.
        '''
        requestProc = Process(target = self.requestClient.asyncRunner)
        requestProc.start()

        while True:
            #---------------------------------------------------
            # Get a HTTPEvent object off of the httpQueue
            #---------------------------------------------------
            try:
                evnt = self.httpQueue.get_nowait()
                self.httpQueue.task_done()
            
            except queue.Empty:
                procCheck = self.checkRequestProcess(requestProc)
                if procCheck is not None:
                    requestProc = procCheck
                time.sleep(0.01)
                continue

            #---------------------------------------------------
            # Check if the event is a stop event
            #---------------------------------------------------
            if evnt.action == "STOP":
                self.requestQueue.put_nowait(None)
                self.requestQueue.join()
                requestProc.terminate()
                requestProc.join()
                requestProc = None
                break

            #---------------------------------------------------
            # Check if the event is an HTTP event.
            # If it is, check through the botListeners to see
            # if there are any actions that need to be taken.
            #---------------------------------------------------
            elif evnt.action == "HTTP":
                #-----------------------------------------------
                # Send the GatewayEvent object to the
                # botListeners to check for any actions
                # that need to be taken.
                #-----------------------------------------------
                for action in self.botListeners.checkListeners(evnt):
                    self.requestQueue.put_nowait(action)

        #-------------------------------------------------------
        # Send a process event to the botQueue to let it know
        # that the http client has stopped.
        #-------------------------------------------------------
        self.botQueue.put_nowait(ProcessEvent("HTTP", "STOPPED"))
    
    #-------------------------------------------------------------------------------------------
    def checkRequestProcess(self, proc) -> Process:
        if proc.is_alive():
            return

        elif not proc.is_alive():
            proc.terminate()
            proc.join()
            proc = Process(target = self.requestClient.asyncRunner)
            proc.start()
            return proc

#-----------------------------------------------------------------------------------------------------------
class RequestClient():
    '''
        This class will be used to make requests to the discord API.

        Its sole purpose is to recieve HTTPRequest object from the requestQueue and send them asynchronously to the server.
    '''
    __slots__ = ('requestQueue', 'logQueue')

    def __init__(self, requestQueue, logQueue):
        self.requestQueue: JoinableQueue = requestQueue
        self.logQueue: JoinableQueue = logQueue
    
    #-------------------------------------------------------------------------------------------
    def asyncRunner(self):
        asyncio.run(self.asyncRequest(self.requestQueue))
        asyncio.close()

    #-------------------------------------------------------------------------------------------
    async def asyncRequest(self, requestQueue):
        '''
            request -> HTTPRequest object that will be sent to the server.
        '''
        while True:
            try:
                reqObj = requestQueue.get_nowait()
                requestQueue.task_done()

            except queue.Empty:
                time.sleep(0.01)
                continue

            if reqObj is None:
                return
            
            #---------------------------------------------------
            # Send the request to the server
            # Retry up to 5 times if a 429 error is returned
            # which means the rate limit has been exceeded.
            #---------------------------------------------------
            counter = 0

            while counter < 5:
                try:
                    response = await AsyncHTTPClient().fetch(reqObj)
                except HTTPClientError as e:
                    if e.code == 429:
                        counter += 1
                        time.sleep(0.3)
                        continue
                    else:
                        self.logQueue.put_nowait(LogEvent("HTTP", "ERROR", e))
                        break
                else:
                    break
