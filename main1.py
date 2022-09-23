#!/usr/bin/env python3
# coding: utf-8

from setup1 import RHF3M076
from logging import basicConfig, getLogger, DEBUG

def main1():
    basicConfig(level=DEBUG)
    logger = getLogger(__name__)
    modem = RHF3M076()
    
    # writee = modem._write("AT+ID")
    # readd = modem._read()
    # print(writee,readd)
    a=12; 
    modem.ADR = True
    if not modem.sendPayload('a'):
        logger.error('Payload send failed.')
    modem = None
    return()

if __name__ == '__main__':
    main1()