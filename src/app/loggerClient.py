import logging
import logging.handlers
import config
from multiprocessing import Process, JoinableQueue
from src.models.procs.event import ProcessEvent

#config._prepare_config()
LOGGING_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

class LoggerClient(Process):
    '''
        LoggerClient is a Process that writes logs to a file.

        Attributes:
            killLoggerClient (bool): Flag to indicate if the logger client should stop.
            logQueue (JoinableQueue): Accepts LogEvent objects to write to the log file.
            botQueue (JoinableQueue): Queue for communication with the main bot process.
            logger (logging.Logger): Logger instance that writes to a file.
    '''
    
    __slots__ = ('killLoggerClient', 'logQueue', 'botQueue', 'logger')

    def __init__(self, name, botQueue, logQueue):
        super().__init__(name=name)

        self.killLoggerClient: bool = False
        self.logQueue: JoinableQueue = logQueue
        self.botQueue: JoinableQueue = botQueue
        self.logger = {
            "DB": None,
            "GATEWAY": None,
            "HTTP": None,
            "LISTENERS": None,
            "COMMANDS": None,
            "HANDLER": None
        }

    #-------------------------------------------------------------------------------------------
    def run(self):
        '''
            The run method initializes the logger and starts processing log events.
            It listens for LogEvent objects on the logQueue and writes them to the log file.
        '''
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
            Initialize loggers for each component.
        '''
        loggerKeys = self.logger.keys()
        for key in loggerKeys:
            self.logger[key] = logging.getLogger(f'squirrel_bo_{key}')
            self.logger[key].setLevel(LOGGING_LEVELS[config.OPTS['logLevel']])
            handler = logging.handlers.RotatingFileHandler(filename=config.OPTS['logFile'][key],
                                                            encoding='utf-8',
                                                            mode='a',
                                                            maxBytes=config.OPTS['logMaxBytes'], 
                                                            backupCount=2)
            handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            self.logger[key].addHandler(handler)

    #-------------------------------------------------------------------------------------------
    def writeLog(self, log):
        '''
            Write the log message to the logger based on the log level.
            log -> LogEvent object containing the log message and level.
        '''
        if log.level == "DEBUG":
            self.logger[log.component].debug(log.message)
        elif log.level == "INFO":
            self.logger[log.component].info(log.message)
        elif log.level == "WARNING":
            self.logger[log.component].warning(log.message)
        elif log.level == "ERROR":
            self.logger[log.component].error(log.message)
        elif log.level == "CRITICAL":
            self.logger[log.component].critical(log.message)
        else:
            self.logger[log.component].info(log.message)