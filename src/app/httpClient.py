import asyncio
import http
import config
import json
import queue
import time
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClientError

from multiprocessing import Process, JoinableQueue
from src.models.procs.event import HttpEvent, HttpResponseEvent, ProcessEvent, LogEvent

__all__ = ['HttpClient', 'RequestClient']

class HttpClient(Process):
    '''
        HttpClient is a Process that handles HTTP requests for the bot.
        It listens for HTTPEvent objects on the httpQueue and processes them asynchronously.

        Spawns a child process that runs the RequestClient, which is a Tornado AsyncHTTPClient, to handle the actual sending of requests.
        It was done this way to avoid issues with asyncio event loops in a multiprocessing environment, as well as to allow
        for Tornado to be used for asynchronous HTTP requests. Tornado also uses Asyncio under the hood, so the eventloop it would use clashes with
        the main event loop used for the GatewayClient connection.

        Attributes:
            botQueue (JoinableQueue): Queue for communication with the main bot process.
            logQueue (JoinableQueue): Queue for logging events.
            httpQueue (JoinableQueue): Queue for HTTP events.
            requestQueue (JoinableQueue): Queue for HTTP requests to be processed asynchronously.
            requestClient (RequestClient): Client that handles asynchronous HTTP requests.

        Methods:
            run() -> None: The main loop that processes HTTP events and manages the request client.
            checkRequestProcess(proc) -> Process: Checks if the request process is alive and restarts it if necessary.
 
    '''

    __slots__ = ('botQueue', 'logQueue', 'httpQueue', 'requestQueue', 'requestClient')

    def __init__(self, name, botQueue, logQueue, httpQueue, httpResponseQueue):
        super().__init__(name=name)
        self.botQueue: JoinableQueue = botQueue
        self.logQueue: JoinableQueue = logQueue
        self.httpQueue: JoinableQueue = httpQueue
        self.requestQueue: JoinableQueue = JoinableQueue()
        self.requestClient = RequestClient(self.requestQueue, httpResponseQueue, self.logQueue)

    #-------------------------------------------------------------------------------------------
    def run(self) -> None:
        '''
            The object retrieved off of the http queue will be an HttpEvent OR HTTPRequest object.
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
            if isinstance(evnt, HttpEvent) and evnt.action == "STOP":
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
            else:
                #-----------------------------------------------
                # Send the GatewayEvent object to the
                # botListeners to check for any actions
                # that need to be taken.
                #-----------------------------------------------
                self.requestQueue.put_nowait(evnt)
            
        #-------------------------------------------------------
        # Send a process event to the botQueue to let it know
        # that the http client has stopped.
        #-------------------------------------------------------
        self.botQueue.put_nowait(ProcessEvent("HTTP", "STOPPED"))
    
    #-------------------------------------------------------------------------------------------
    def checkRequestProcess(self, proc) -> Process:
        '''
            Check if the request process is alive.
            If it is not alive, terminate it and start a new one.
            Returns the new process if it was restarted, otherwise returns None.
        '''
 
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


        Purely a means of sending HTTP requests asynchronously while making use of multiprocessing and asyncio.
        It will not handle any events or responses, just send the requests and log any errors that occur.
    '''
    __slots__ = ('requestQueue', 'logQueue', 'httpResponseQueue')

    def __init__(self, requestQueue, responseQueue, logQueue):
        self.requestQueue: JoinableQueue = requestQueue
        self.httpResponseQueue: JoinableQueue = responseQueue
        self.logQueue: JoinableQueue = logQueue

    #-------------------------------------------------------------------------------------------
    def asyncRunner(self):
        asyncio.run(self.asyncRequest(self.requestQueue, self.httpResponseQueue))

    #-------------------------------------------------------------------------------------------
    async def asyncRequest(self, requestQueue, httpResponseQueue):
        '''
            request -> HTTPRequest object that will be sent to the server.
        '''
        while True:
            try:
                reqObj = self.requestQueue.get_nowait()
                print(type(reqObj))

                self.requestQueue.task_done()
                self.logQueue.put_nowait(LogEvent(component="HTTP", action="LOG", level="DEBUG", message=f"[RequestClient] HTTP: method --> {reqObj.data.method}   url --->  {reqObj.data.url}"))

            except queue.Empty:
                time.sleep(0.01)
                continue

            #---------------------------------------------------
            # If the request object is None, then we are done.
            # This is used to signal that the request client
            # should stop processing requests.
            #---------------------------------------------------
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
                    response = await AsyncHTTPClient().fetch(reqObj.data)
                    self.logQueue.put_nowait(LogEvent(component="HTTP", action="LOG", level="INFO", message=f"[RequestClient] HTTP: method --> {reqObj.data.method}   url --->  {reqObj.data.url}  response-->{response.body.decode('utf-8')}  response code --> {response.code}"))

                except HTTPClientError as e:
                    #------------------------------------------------
                    #   Check if the error is a rate limit error
                    #   If it is, wait a bit and try again.
                    #------------------------------------------------
                    if e.code == 429:
                        counter += 1
                        time.sleep(0.3)
                        continue
                    else:
                        self.logQueue.put_nowait(LogEvent(component="HTTP", action="LOG", level="ERROR", message=f"[RequestClient] HTTP: method --> {reqObj.data.method}   url --->  {reqObj.data.url}   body ---> {reqObj.data.body}   message-->{e.message}"))
                        if reqObj.response:
                            errorObj = {'error': e.message, 'code': e.code, 'url': reqObj.data.url}
                            self.httpResponseQueue.put_nowait(HttpResponseEvent(id=reqObj.id, data=errorObj))
                        break

                else:
                    if reqObj.response:
                        responseEvent = HttpResponseEvent(id=reqObj.id, data=response)
                        self.httpResponseQueue.put_nowait(responseEvent)
                    break