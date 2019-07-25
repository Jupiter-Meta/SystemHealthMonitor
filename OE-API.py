#!/usr/bin/python3
import datetime,sys,os,io
from flask import Flask, jsonify,request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
urls=("/favicon.ico","dummy")

@app.route('/')
def API1():
	data = {'EnergyAvailability':10,'CostPerUnit':5.6}
  return jsonify({'Recent power availability' : r})
if __name__ == '__main__':
  app.run(host='0.0.0.0',port=2020,debug=1)
