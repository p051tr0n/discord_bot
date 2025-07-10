import logging
import logging.handlers
import config
from multiprocessing import Process, JoinableQueue
from src.models.procs.event import ProcessEvent

#config._prepare_config()

class LoggerClient(Process):
    '''
        LoggerClient is a Process that writes logs to a file.

        logQueue -> Accepts LogEvent objects to write to the log file.
    '''
    
    __slots__ = ('killLoggerClient', 'logQueue', 'botQueue', 'logger')

    def __init__(self, botQueue, logQueue):
        super().__init__()

        self.killLoggerClient: bool = False
        self.logQueue: JoinableQueue = logQueue
        self.botQueue: JoinableQueue = botQueue
        self.logger = None

    #-------------------------------------------------------------------------------------------
    def run(self):
        self.create_logger()

        while True:
            log = self.logQueue.get()

            self.logQueue.task_done()

            if log.action == "STOP":
                self.killLoggerClient = True
                break
            
            if log.action == "LOG":
                self.writeLog(log)

        procEvent = ProcessEvent("LOGGER", "STOPPED")
        self.botQueue.put_nowait(procEvent)

    #-------------------------------------------------------------------------------------------
    def create_logger(self):
        '''
        
        '''
        self.logger = logging.getLogger('squirrel_bot')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(filename=config.OPTS['logFile'],
                                                        encoding='utf-8', 
                                                        mode='a', 
                                                        maxBytes=1024000, 
                                                        backupCount=4)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

    #-------------------------------------------------------------------------------------------
    def writeLog(self, log):
        '''
            Write the log message to the logger based on the log level.
            log -> LogEvent object containing the log message and level.
        '''
        if log.level == "DEBUG":
            self.logger.debug(log.message)
        elif log.level == "INFO":
            self.logger.info(log.message)
        elif log.level == "WARNING":
            self.logger.warning(log.message)
        elif log.level == "ERROR":
            self.logger.error(log.message)
        elif log.level == "CRITICAL":
            self.logger.critical(log.message)
        else:
            self.logger.info(log.message)