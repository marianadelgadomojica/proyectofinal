#!/usr/bin/env python3
# coding: utf-8

from multiprocessing.connection import wait
from setup import RHF3M076
import time

def main():
    modem = RHF3M076()

    print('DevAddr: ' + modem.DevAddr)
    print('DevEui: ' + modem.DevEui)
    print('AppEui: ' + modem.AppEui)

    print('Hey loco que pasa vale mia')
    writee = modem._write("AT+MSGHEX=334455")
    readd = modem._read()
    print(writee,readd)



    #for i in range(5):
        #esperar 3min
        #readd = modem._read()
        #si la lectura tiene Done:
            #break
        


    #EXPRESIONES REGULARES

    modem = None
  
    return()

if __name__ == '__main__':
    main()