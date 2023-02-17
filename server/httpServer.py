from flask import Flask, render_template, redirect, url_for, request

import gpiozero as gp
from enum import Enum

httpServ = Flask(__name__)

class State(Enum):
    IDLE = 1
    HEATING = 2

curentState = State.IDLE
relay_pin = 18
rel = gp.OutputDevice(relay_pin);

@httpServ.route("/index")
@httpServ.route("/mainpage")
@httpServ.route("/")
def landing():
    return redirect(url_for("base"))


@httpServ.route("/base")
def base():
    return render_template("base.html",w_state=curentState.name)

@httpServ.route("/toggleHeating")
def toggleHeating():
    global curentState
    global rel

    if(curentState == State.IDLE):
        curentState = State.HEATING
        rel.on();

    else:
        curentState = State.IDLE
        rel.off();

    
    return redirect(url_for("base"))

@httpServ.route("/submit", methods=["POST"])
def submit():
    command = format(request.form.get("command"))

    match command:
        case "toggle heating":
            return redirect(url_for('toggleHeating'))
        case _:
            return "invalid"


    return '{}'.format(request.form.get("command"))