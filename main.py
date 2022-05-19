import paho.mqtt.client as mqtt
import paho.mqtt.client as mqttclient
import sendComand
import json


def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    msg = json.loads(msg.payload)

    if('comando' in list(msg.keys())):
        if(msg['comando']=='openLuck'):
            if(sendComand.sendComando(msg['comando'])):
                mqttc.publish("LuckResult","{\"LuckResult\":\"Open Succesfull\"}",qos = 1)            
        if(msg['comando']=='readStatus'):
            if(sendComand.sendComando(msg['comando'])):
                mqttc.publish("LuckResult","{\"LuckResult\":\"Luck Open\"}",qos = 1)
        if(msg['comando']=='openDoor'):
            sendComand.sendComando(msg['comando'])
            mqttc.publish("LuckResult","{\"LuckResult\":\"Door OPen\"}",qos = 1)
                
def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


clientID = "iotconsole"
broker = "" #EndPoin AWS
port = 8883
topic = "candado"


my_ca_cert = "*.crt"         #CERTIFACTE CA1
my_pri_cert = "*.pem"        #PRIVATE KEY
my_key_cert = "*.pem"        #CERTIFICATE


mqttc = mqtt.Client(clientID)
mqttc.tls_set(my_ca_cert,my_key_cert,my_pri_cert)

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect(broker,port)

mqttc.subscribe(topic,1)
time.sleep(0.1)
rc=0

while True:
    rc = mqttc.loop()



