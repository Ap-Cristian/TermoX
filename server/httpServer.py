from flask import Flask, render_template, redirect, url_for, request

import gpiozero as gp
from enum import Enum

import sqlite3 as sql

import datetime

httpServ = Flask(__name__)

class State(Enum):
    IDLE = 1
    HEATING = 2

curentState = State.IDLE
relay_pin = 18
#rel = gp.OutputDevice(relay_pin);

@httpServ.route("/dbCmdAdd/<cmd>")
def dbCmdAdd(cmd):
    dbCmdInsertQ = '''INSERT INTO CMD VALUES(?,?,?,?);'''
    
    connection = sql.connect("TERMOXdatabase.db")
    cursor = connection.cursor()
    cursor.execute(dbCmdInsertQ,(None,datetime.datetime.now(),request.remote_addr,cmd))
    connection.commit()

    return redirect(url_for("base"))

@httpServ.route("/clearLog")
def clearLog():
    connection = sql.connect("TERMOXdatabase.db")
    cursor = connection.cursor()

    dbCmdClearQ = '''DROP TABLE IF EXISTS CMD'''
    dbCmdCreateQ = '''CREATE TABLE IF NOT EXISTS CMD(Cmd_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     Time TIMESTAMP,
                     Ip VARCHAR(20),
                     String VARCHAR(100)
                     );'''

    cursor.execute(dbCmdClearQ)
    cursor.execute(dbCmdCreateQ)
    
    connection.commit()
    return redirect(url_for("dbCmdAdd",cmd="clear log"))

@httpServ.route("/index")
@httpServ.route("/mainpage")
@httpServ.route("/")
def landing():
    return redirect(url_for("base"))


@httpServ.route("/base")
def base():
    dbConn = sql.connect("TERMOXdatabase.db")
    cursor = dbConn.cursor()
    dbCmdSelectQ = '''SELECT * FROM CMD'''
    response = cursor.execute(dbCmdSelectQ)

    responseArr = response.fetchall()
    print(responseArr)

    return render_template("base.html",w_state = curentState.name, w_cmds = responseArr)

@httpServ.route("/toggleHeating")
def toggleHeating():
    global curentState
    #global rel

    if(curentState == State.IDLE):
        curentState = State.HEATING
        # rel.on();

    else:
        curentState = State.IDLE
        # rel.off();

    return redirect(url_for("dbCmdAdd",cmd="toggle heating"))

@httpServ.route("/heatingOn")
def heatingOn():
    global curentState
    #global rel

    if(curentState == State.IDLE):
        curentState = State.HEATING
        return redirect(url_for("dbCmdAdd",cmd="heating on"))
        # rel.on();

    if(curentState == State.HEATING):
        print("heating already on")
        return "heating already on dumb fuck"

@httpServ.route("/heatingOff")
def heatingOff():
    global curentState
    #global rel

    if(curentState == State.HEATING):
        curentState = State.IDLE
        return redirect(url_for("dbCmdAdd",cmd="heating off"))
        # rel.on();

    if(curentState == State.IDLE):
        print("heating already off")
        return "heating already off dumb fuck"
    

@httpServ.route("/submit", methods=["POST"])
def submit():
    command = format(request.form.get("command"))

    if(command == "toggle heating"):
        return redirect(url_for("toggleHeating"))

    if(command == "heating on"):
        return redirect(url_for("heatingOn"))
    
    if(command == "heating off"):
        return redirect(url_for("heatingOff"))
    
    if(command == "clear log"):
        return redirect(url_for("clearLog"))
    
    else:
        return "invalid"


    return '{}'.format(request.form.get("command"))
