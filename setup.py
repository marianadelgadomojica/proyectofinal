#RHF3M076.py
#!/usr/bin/env python3
# coding: utf-8

import serial
import re


# Class of LoRaWAN Modem
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

        self._open()
        self._getId()

    # Open serial port
    def _open(self):
        self._modem = serial.Serial(
            port=self._port,
            baudrate=self._baud,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=self._timeout,
            xonxoff=False,
            rtscts=False,
            write_timeout=None,
            dsrdtr=False,
            inter_byte_timeout=None
        )
        print('$$$$$$$$$$$ open')

        return()

    # Get IDs
    def _getId(self):
        cmd = 'AT+ID'
        self._write(cmd)

        lines = self._read()
        print(lines)
        for line in lines:
            res = re.match(self._ptnDevAddr, line)
            if res:
                self._DevAddr = res.group(1)
                continue
            res = re.match(self._ptnDevEui, line)
            if res:
                self._DevEui = res.group(1)
                continue
            res = re.match(self._ptnAppEui, line)
            if res:
                self._AppEui = res.group(1)

    # Send to serial port
    def _write(self, cmd):
        cmd = cmd + self._crlf
        ret = self._modem.write(cmd.encode())
        return(ret)

    # Receive from serial port
    def _read(self):
        result = []
        lines = self._modem.readlines()
        for line in lines:
            result.append(line.decode().replace(self._crlf, ''))
        return(result)

    @property
    def DevAddr(self):
        return(self._DevAddr)

    @property
    def DevEui(self):
        return(self._DevEui)

    @property
    def AppEui(self):
        return(self._AppEui)

    # Destructor
    def __del__(self):
        self._modem.close()