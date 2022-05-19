import RPi.GPIO as GPIO
from time import sleep
import serial

def sendComando(comand):
    device = serial.Serial('/dev/ttyAMA0', 9600,timeout=1)
    status = None
    if(comand=='openLock'):        
        while status == None:            
            Lock(device,comand)
            status = readStatus(device)
        device.close()    
        return True
    elif(comand=='readStatus'):   
        while status == None:        
            status = readStatus(device) 
            Lock(device,comand)
        if status:
            device.close()
            return True
        else:
            device.close()
            return False
    elif(comand=='openDoor'):
        openDoor()
        return True
    else:
        device.close()
        return None

def Lock(device,comand): 
    packet = {'openLock':[0x55, 0xAA, 0x01, 0x10, 0x30, 0x02, 0x21, 0x01, 0x9A, 0xFF],
           'readStatus':[0x55, 0xAA, 0x01, 0x10, 0x30, 0x01, 0x20, 0x01, 0x9C, 0xFF]}
    sleep(1)
    device.write(serial.to_bytes(packet.get(comand)))

def readStatus(device): 
    mesagge = device.read_until(expected="FF")
    package=[]
    if(mesagge.hex()!=''): 
        msg = list(str(mesagge.hex()))        
        for i in range(0,20,2):
            package.append("0x"+msg[i]+msg[i+1])
        if(str(package[7])=='0x00'):
            return False
        elif str(package[7])=='0x01':
            return True

def openDoor():
    actuador = 7
    GPIO.setmode(GPIO.BOARD)    
    GPIO.setup(actuador,GPIO.OUT) 
    
    GPIO.output(actuador,True)
    print('Abriendo puerta')    
    sleep(5)
    print('A quedado abierta')       
    GPIO.output(actuador,False)

    


