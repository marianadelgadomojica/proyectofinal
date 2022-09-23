#!/usr/bin/env python3
# coding: utf-8

#------------------------------------------------------------------------------
# LoRaWAN modem (RHF3M076) module for Fukuoka City LoRaWAN
#     by Kaho Musen Holdings Co.,Ltd.
#
#     Created: 2017.11.03
#      Author: k.nagase (a) gooday.co.jp
#------------------------------------------------------------------------------

import serial
import re
import time
from logging import getLogger

# Class for RHF3M076
class RHF3M076:

    # Constructor
    def __init__(self, port='COM3', baud=9600, timeout=0.1):
        self._port = port
        self._baud = baud
        self._timeout = timeout
        self._crlf = '\r\n'
        self._ptnDevAddr = r'\+ID: DevAddr, (([0-9A-Fa-f]{2}[:-]){3}[0-9A-Fa-f]{2})'
        self._ptnDevEui = r'\+ID: DevEui, (([0-9A-Fa-f]{2}[:-]){7}[0-9A-Fa-f]{2})'
        self._ptnAppEui = r'\+ID: AppEui, (([0-9A-Fa-f]{2}[:-]){7}[0-9A-Fa-f]{2})'
        self._ptnKeyErr = r'\+KEY: ERROR\((.*)\)'
        self._logger = getLogger(type(self).__name__)

        self._open()

    # Open the serial port
    def _open(self):
        self._modem = serial.Serial()
        self._modem.port = self._port
        self._modem.baudrate = self._baud
        self._modem.timeout = self._timeout

        try:
            self._modem.open()
            self._modem.reset_input_buffer()
            return()
        except Exception as e:
            self._logger.error('Serial port open failed.')
            raise(e)

    # Send key type and key value
    def _setKey(self, KeyType, KeyValue):
        try:
            if KeyValue:
                cmd = 'AT+KEY=' + KeyType + ',"' + KeyValue + '"'
                ret = self._write(cmd)
                self._waitResponse()
                line = self._read()
                ret = re.match(self._ptnKeyErr, line)
                if ret:
                    raise Exception(KeyType + ' is invalid. (' + ret.group(1) + ')')
            else:
                raise Exception(KeyType + ' is empty.')
            return()
        except Exception as e:
            self._logger.error(e)

    # Send to serial port
    def _write(self, cmd):
        try:
            self._logger.info('SEND:' + cmd)
            cmd = cmd + self._crlf
            ret = self._modem.write(cmd.encode())
            return(ret)
        except Exception as e:
            print('ERROR: Send to serial port failed.')
            raise(e)

    # Receive from serial port
    def _read(self):
        len = self._waitResponse()
        ret = self._modem.readline().decode().replace(self._crlf, '')
        self._logger.info('RECV:' + ret)
        return(ret)

    def _waitResponse(self):
        while self._modem.inWaiting() == 0:
            time.sleep(0.1)
        return(self._modem.inWaiting())

    # Send payload
    def sendPayload(self, Payload):
        cmd = 'AT+CMSGHEX="' + Payload + '"'
        self._write(cmd)
        #time.sleep(2)
        len = self._waitResponse()
        ack = False
        while True:
            line = self._read()
            if line == '+CMSGHEX: Done': break
            if line == '+CMSGHEX: ACK Received':
                ack = True
        return(ack)

    @property
    def DevAddr(self):
        return(self._DevAddr)

    @property
    def DevEui(self):
        return(self._DevEui)

    @property
    def AppEui(self):
        return(self._AppEui)

    @property
    def NwksKey(self):
        return(self._NwksKey)

    @property
    def AppsKey(self):
        return(self._AppsKey)

    @property
    def AppKey(self):
        return(self._AppKey)

    @property
    def ADR(self):
        return(self._ADR)

    @NwksKey.setter
    def NwksKey(self, NwksKey):
        self._NwksKey = NwksKey
        self._setKey('NWKSKEY', self._NwksKey)

    @AppsKey.setter
    def AppsKey(self, AppsKey):
        self._AppsKey = AppsKey
        self._setKey('APPSKEY', self._AppsKey)

    @AppKey.setter
    def AppKey(self, AppKey):
        self._AppKey = AppKey
        self._setKey('APPKEY', self._AppKey)

    @ADR.setter
    def ADR(self, state):
        self._ADR = state
        strState = 'ON' if self._ADR else 'OFF'
        cmd = 'AT+ADR=' + strState
        ret = self._write(cmd)
        len = self._waitResponse()
        self._read()

    # Destructor
    def __del__(self):
        self._modem.close()