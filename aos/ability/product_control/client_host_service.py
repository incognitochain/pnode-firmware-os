import zmq
import sys
port = "5055"
context = zmq.Context()
print "Connecting to server..."
socket = context.socket(zmq.REQ)
socket.connect ("tcp://*:%s" % port)
data_send = '{"type":"incognito","source": "_PHONE","data":{"action":"start","chain":"incognito","type":"","privateKey":"112t8rnXHdfcY71iDpEb7MKsGaDLQrp7jwuJpDZjZBCy1vaZbSYZ9NpwdXB4KQp6PTe8dfCgxMEbTWWyssYGD7zSV6T3mA23k81h7ZCq4vcr" },"protocal":"firebase" }'
socket.send(data_send) 
re = socket.recv()
print re
