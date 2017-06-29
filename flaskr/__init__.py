#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient, DESCENDING
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app, make_response, jsonify
from flask_cors import CORS, cross_origin
from datetime import timedelta
from functools import update_wrapper


def create_app():
    app = Flask(__name__)
    return app

app = create_app()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "genuino"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]
db2 = client.genuino
escuchas = db2.escuchas

''' # Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS
POSTGRESDATABASE = "mydatabase"
POSTGRESUSER = "myuser"
POSTGRESPASS = "mypass"
postgresdb = psycopg2.connect(
    database=POSTGRESDATABASE,
    user=POSTGRESUSER,
    password=POSTGRESPASS)
'''

# Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = '/var/www/flaskr/queries'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    results = eval('mongodb.' + query)
    results = json_util.dumps(results, sort_keys=True, indent=4)

    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"


@app.route("/api/<consulta>/<datos1>")
@cross_origin(origin='*')
def api(consulta, datos1):
    if consulta == '1':
        fecha = datos1
        query = "escuchas.find({'fecha': '" + fecha + "'}, {'numero': 1})"
        resultado = eval('mongodb.' + query)
        return json_util.dumps(resultado, sort_keys=True, indent=4)

    elif consulta == '2':
        separados = datos1.split('_')
        numero = separados[0]
        limite = separados[1]
        consultilla = escuchas.find({'numero': numero}).sort([['fecha', DESCENDING]])
        return json_util.dumps(consultilla, sort_keys=True, indent=4)


    elif consulta == '3':
        clave = datos1
        fecha = clave

    else:
        return 'Not Implemented'
    coso = jsonify({'date': fecha})
    return coso

@app.route("/postgres")
def postgres():
    query = request.args.get("query")
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    print(results)
    return render_template('postgres.html', results=results)


@app.route("/example")
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run()
