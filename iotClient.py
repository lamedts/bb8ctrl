
# Creates a connection to IBM IOT Foundation as a device.
# Class intended to be imported and passed a path to the device config
#  during instantiation.


import ibmiotf.device
import json

class iotClient(object):
  
  def __init__(self, config):
    self.client = ibmiotf.device.Client(config)

  def connect(self):
    try:
      self.client.connect()
    except ibmiotf.ConnectionException as e:
      self.client.disconnect()
      print e  

  def send(self, eventData, jsonData):
    print "Sending JSON Payload"
    #self.client.publishEvent("status", json.dumps(jsonData))
    self.client.publishEvent(event=eventData, msgFormat="json", data=jsonData)
    print json.dumps(jsonData)

