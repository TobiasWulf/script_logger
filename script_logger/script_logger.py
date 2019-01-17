#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides attributes, functions and classes which makes it easier to
implement a logging enviroment for any application. It although reimports
several useful objects, function or classes to maintain the logging enviroment
and cleanup after logging works is done.

.. module:: script_logger
   :platform: Unix, Windows
   :synopsis: Tools to implement a logging enviroment.
              
.. moduleauthor:: Tobias Wulf <46107549+TobiasWulf@users.noreply.github.com>
   :version: 1.2
   :status: production


:Attributes:
    
    :param: STDOUT: Stream for console output. Imported from :mod:`sys`.
    :type: STDOUT: ipykernel.iostream.OutStream.
    :param: NOTSET: Logger level (0). Imported from :mod:`logging`.
    :type: NOTSET: int.
    :param: DEBUG: Logger level (10). Imported from :mod:`logging`.
    :type: DEBUG: int.
    :param: INFO: Logger level (20). Imported from :mod:`logging`.
    :type: INFO: int.
    :param: WARNING: Logger level (30). Imported from :mod:`logging`.
    :type: WARNING: int.
    :param: ERROR: Logger level (40). Imported from :mod:`logging`.
    :type: ERROR: int.
    :param: CRITICAL: Logger level (50). Imported from :mod:`logging`.
    :type: CRITICAL: int.
    :param: DATE_FMT: Date formatter for log records.
    :type: DATE_FMT: str.
    :param: STREAM_FMT: Formatter for log records to console output. Less in detail.
                        Format style '%'.
    :type: STREAM_FMT: str.
    :param: FILE_FMT: Formatter for log records to logfile output. Very in detail.
                      Format style '%'.
    :type: FILE_FMT: str.

:Functions:
    
    :func:`script_logger.rmall`
    
:Classes:
    
    :class:`script_logger.ScriptLogger`
   
.. seealso:: Other imported functions and classes:
   :func:`os.getcwd`, :func:`os.mkdir`, :func:`os.path.splitext`,
   :func:`os.path.basename`, :func:`os.path.isfile`, :func:`os.path.isdir`,
   :func:`os.path.join`, :func:`sys.exit`, :func:`glob.glob`,
   :class:`datetime.datetime`, :class:`logging.Formatter`,
   :class:`logging.StreamHandler`, :class:`logging.Logger`,
   :class:`logging.handlers.TimedRotatingFileHandler`

:Example:
    
    >>> from script_logger import script_logger as sl
    >>> logger = sl.ScriptLogger(__name__, level=sl.DEBUG, stream_fmt=sl.STREAM_FMT,
    >>>                          file_fmt=sl.FILE_FMT, datefmt=sl.DATE_FMT,
    >>>                          stream=sl.STDOUT, filename='myLog.log')
    >>> logger.debug('debug message')
    >>> logger.info('info message')
    >>> logger.warning('warning message')
    >>> logger.error('error message')
    >>> logger.critical('critical message')
    >>> try:
    >>>     raise Exception('exception message')
    >>> except Exception:
    >>>     logging.exception('here comes the raise')
    >>> sl.shutdown()
    >>> del(logger)
    2018-12-06 12:43:53 - <__name__> - DEBUG    - debug message
    ...
"""
#%%
__all__ = ['STDOUT', 'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',
           'DATE_FMT', 'FILE_FMT', 'STREAM_FMT', 'getcwd', 'mkdir', 'splitext',
           'basename', 'isfile', 'isdir', 'join', 'sysexit', 'shutdown', 'rm',
           'rmdir', 'rmall', 'glob', 'datetime', 'Formatter',
           'StreamHandler', 'Logger', 'TimedRotatingFileHandler',
           'ScriptLogger']
__version__ = "1.2"
__status__ = "production"
__author__ = "Tobias Wulf <46107549+TobiasWulf@users.noreply.github.com>"
__docformat__ = "reStructedText"
#%%
# constants
from sys import stdout as STDOUT
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

# functions
from os import getcwd, mkdir
from os import remove as rm
from os import removedirs as rmdir
from os.path import splitext, basename, isfile, isdir, join
from sys import exit as sysexit
from logging import shutdown
from glob import glob

# classes
from datetime import datetime
from logging import Formatter, StreamHandler, Logger
from logging.handlers import TimedRotatingFileHandler
#%%
DATE_FMT = '%Y-%m-%d %H:%M:%S'
FILE_FMT = ('%(asctime)s - %(process)-6d - %(thread)-6d - %(module)s - ' + 
            '%(funcName)s - %(name)s - %(levelname)-8s - %(message)s')
STREAM_FMT = '%(asctime)s - %(name)s - %(levelname)-8s - %(message)s'
#%%
def rmall(*args, purge_tree=True):
    """
    Removes any given directories or files in args tuple. For directories
    it works recursive.
    
    :Attributes:
        
        :param: args: File or directory names to remove.
        :type: args: str.
        :param: purge_tree: Default True. If false the the tree will just be cleaned, else all will be removed.
        :type: purge_tree: bool.
        
    :raises: TypeError
    """
    for arg in args:
        if isfile(arg):
            rm(arg)
        elif isdir(arg):
            [rm(f) for f in glob(join(arg, '**'), recursive=True) if isfile(f)]
            if purge_tree:
                [rmdir(d) for d in glob(join(arg, '**'), recursive=True)[::-1] if isdir(d)]
        else:
            raise TypeError(str(arg) + " in *args is not a file or even a directory.")
                
#%%
class ScriptLogger(Logger):
    """
    ScriptLogger class inherits behavior from :class:`logging.Logger`. Its use
	supplies a high reuse for logging in projects. To setup the logger inheritance
	several side classes are needed. So it passes the attributes for the needed
	classes through __init()__. To not override the methods of :class:`logging.Logger`
	and get the class attributes single functional.
    
    :Attributes:
        
        :param: name: Logger name. See :class:`logging.Logger`.
        :type: name: str.
        :param: level: Logger level (defaufl DEBUG, set handlers too). See :class:`logging.Logger`.
        :type: level: int.
        :param: stream_fmt: Console formatter string. See :class:`logging.Formatter`.
        :type: stream_fmt: str.
        :param: file_fmt: File formatter string. See :class:`logging.Formatter`.
        :type: file_fmt: str.
        :param: date_fmt: Date formatter string. See :class:`logging.Formatter`.
        :type: date_fmt: str.
        :param: style: Formatter string style (default '%'). See :class:`logging.Formatter`.
        :type: style: str.
        :param: stream: Console stream. In std. cases use sys.stdout. See :class:`logging.StreamHandler`.
        :type: stream: ipykernel.iostream.OutStream.
        :param: filename: Full file path or simply filename for logfile.
        :type: filename: str.
        :param: when: Specifies the type of interval. See :class:`logging.handlers.TimedRotatingFileHandler`.
        :type: when: str.
        :param: interval: See :class:`logging.handlers.TimedRotatingFileHandler`.
        :type: interval: int.
        :param: backupCount: See :class:`logging.handlers.TimedRotatingFileHandler`.
        :type: backCount: int.
        :param: encoding: See :class:`logging.handlers.TimedRotatingFileHandler`.
        :type: encoding: bool.
        :param: delay: See :class:`logging.handlers.TimedRotatingFileHandler`.
        :type: delay: bool.
        :param: utc: See :class:`logging.handlers.TimedRotatingFileHandler`.
        :type: utc: bool.
    
    :properties: stream_formatter, stream_handler, filename, file_formatter, file_handler
    :raises: TypeError
    """
    def __init__(self, name, level=10, stream_fmt=None, file_fmt=None, date_fmt=None,
                 style='%', stream=None, filename=None, when='midnight', interval=1,
                 backupCount=0, encoding=None, delay=False, utc=False, atTime=None):

        Logger.__init__(self, name, level)
        self.stream_formatter = Formatter(stream_fmt, date_fmt, style)
        self.stream_handler = StreamHandler(stream)
        self.stream_handler.setFormatter(self.stream_formatter)
        self.stream_handler.setLevel(self.level)
        self.addHandler(self.stream_handler)
        self.filename = filename
        if self.filename is not None:
            self.file_formatter = Formatter(file_fmt, date_fmt, style)
            self.file_handler = TimedRotatingFileHandler(self.filename, when=when,
                                                         interval=interval,
                                                         backupCount=backupCount,
                                                         encoding=encoding,
                                                         delay=delay, utc=utc,
                                                         atTime=atTime)
            self.file_handler.setFormatter(self.file_formatter)
            self.file_handler.setLevel(self.level)
            self.addHandler(self.file_handler)
    
    # attribute getters
    @property
    def stream_formatter(self):
        """:class:`logging.Formatter` formatter for stream handler."""
        return self.__stream_formatter
    
    @property
    def stream_handler(self):
        """:class:`logging.StreamHandler` logger handler for console output."""
        return self.__stream_handler
    
    @property
    def filename(self):
        """
        Full filename of logfile. The filename will be set and checked if it
        is a directory or valid textfile of type log. If it is not the right one
        the extension will be changed to log. If it is just a string the result
        will be ./logs/<filename>.log.
        """
        return self.__filename
    
    @property
    def file_formatter(self):
        """:class:`logging.Formatter` formatter for file handler."""
        return self.__file_formatter

    @property
    def file_handler(self):
        """
        :class:`logging.handlers.TimedRotatingFileHandler` logger handler 
        for logfile output.
        """
        return self.__file_handler
    
    # attribute setters
    @stream_formatter.setter
    def stream_formatter(self, formatter):
        if type(formatter) is Formatter:
            self.__stream_formatter = formatter
        else:
            raise TypeError("stream_formatter must be type of logging.Formatter")
    
    @stream_handler.setter
    def stream_handler(self, handler):
        if type(handler) is StreamHandler:
            self.__stream_handler = handler
        else:
            raise TypeError("stream_handler must be type of logging.StreamHandler")
            
    @filename.setter
    def filename(self, filename):
        if filename is None:
            self.__filename = filename
        elif type(filename) is str:
            try:
                if isfile(filename):
                    fext = splitext(filename)[1]
                    if fext != '.log':
                        raise TypeError("file type must be type of .log")
                elif isdir(filename):
                    fname = splitext(basename(self.name))[0] + '.log'
                    filename = join(filename, fname)
                else:
                    fpath = join(getcwd(), 'logs')
                    fname = splitext(basename(filename))[0] + '.log'
                    if isdir(fpath) is not True:
                        mkdir(fpath)
                    filename = join(fpath, fname)
            except Exception:
                raise
            else:
                self.__filename = filename
        else:
            raise TypeError("filename must be type of string or None for no file logging")

    @file_formatter.setter
    def file_formatter(self, formatter):
        if type(formatter) is Formatter:
            self.__file_formatter = formatter
        else:
            raise TypeError("file_formatter must be type of logging.Formatter")

    @file_handler.setter
    def file_handler(self, handler):
        if type(handler) is TimedRotatingFileHandler:
            self.__file_handler = handler
        else:
            raise TypeError("file_handler must be type of TimedRotatingFileHandler")
