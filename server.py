
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
#from flask.ext.cors import CORS
import os
from time import sleep
import time
import signal
import sys
import logging
from iotClient import iotClient
import traceback
import random

from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
#CORS(app)

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)

try:
  options = {
    "org": os.environ.get('ORG'),
    "type": os.environ.get('TYPE'),
    "id": os.environ.get('ID'),
    "auth-method": os.environ.get('AUTH_M'),
    "auth-token": os.environ.get('AUTH_T'),
  }
  table = iotClient(options)
  table.connect()
except:
  print(traceback.format_exc())

@app.route("/")
def index():
  return app.send_static_file("index.html")


@app.route("/api/change_color")
def send1():
  rgb = {'r': random.randrange(0, 256), 'g': random.randrange(0, 256), 'b': random.randrange(0, 256)}
  if(request.args.get('r') != None):
    rgb = {'r': int(request.args.get('r')), 'g': int(request.args.get('g')), 'b': int(request.args.get('b'))}
  table.send("rgb", rgb)
  return jsonify(result={"status": 200})

@app.route("/api/defmove")
def send2():
  movement = {'speed': random.randrange(0, 256), 'direction': random.randrange(0, 360)}
  #movement = {'speed': random.randrange(0, 256), 'direction': random.randrange(0, 360)}
  if(request.args.get('direction') != None):
    movement = {'speed': 70, 'direction': int(request.args.get('direction'))}
    if(int(time.time())% 2 == 0):
      print int(time.time())
      table.send("direction", movement)
  return jsonify(result={"status": 200})

@app.route("/api/key")
def sendReset():
  if(request.args.get('btn') != None):
    table.send("key", {"btn": request.args.get('btn')})
  return jsonify(result={"status": 200})


port = os.environ.get('VCAP_APP_PORT')
if __name__ == "__main__":
      app.run(host='0.0.0.0', port=int(port))



