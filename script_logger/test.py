#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script for ScriptLogger package."""

import os, re, sys, glob

if __name__ == "__main__":
    try:
        # import package
        import script_logger as sl
        print('Check package import:')
        print('\tModule imported as sl:\n\t', sl)
        print('\t\tVersion: ', sl.__version__)
        print('\t\tAuthor: ', sl.__author__)
        print('\t\tNamespace:')
        for n in sl.__all__:
            print('\t\t\tsl.{0}: {1}'.format(n, getattr(sl, n)))
        
        logger = sl.ScriptLogger('test', level=sl.DEBUG, stream_fmt=sl.STREAM_FMT,
                                 file_fmt=sl.FILE_FMT, date_fmt=sl.DATE_FMT,
                                 stream=sl.STDOUT, filename='test')
        
        print(logger.handlers)
        
        logger.info('test')
        
        raise ValueError('test23')
        
        
    except ValueError as e:
        logger.exception(str(e))
    except Exception as e:
        print(e)
        
    else:
        pass
    finally:
        sl.shutdown()
        del(logger)
#        sysexit()
        pass
