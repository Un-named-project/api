__version__ = '1.0.0'

from flask import Flask, request, render_template
from dataclasses import dataclass
import os
import time

# custom library import
import password

os.system("color")

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CBLUE   = '\33[34m'
CREDBG    = '\33[41m'
CYELLOW = '\33[33m'
CBLINK    = '\33[5m'


app = Flask(__name__, template_folder='templates', static_folder='static')

global global_state

machines = {}
global_state = False

CARMED = True #! The program is not armed

@dataclass
class machine:
    name: str
    room: str
  
  
@app.route('/dash', methods=["GET", "POST"])
def dashboard():
    global global_state
    if request.method == "POST":
        if request.form['control'] == 'Start' and (password.check_pass(request.form['password']) and password.check_pass(request.form['password2'])):
            if not CARMED:
                print(CBLUE + "Caution, attempt to run while dissarmed" + CEND)
                return render_template('base.html', result=machines, status=global_state)
            else:
                print(CBLACK + CREDBG + "Warning, in progress!!!!" + CEND)
                global_state = True
                return render_template('base.html', result=machines, status=global_state)
        elif request.form['control'] == 'Abort':
            print(CYELLOW + "Attack aborted" + CEND)
            global_state = False
            return render_template('base.html', result=machines, status=global_state)
        else:
            global_state = False
            return render_template('base.html', result=machines, status=global_state)
        
    elif request.method == 'GET':
        return render_template('base.html', result=machines, status=global_state)

@app.route('/add', methods=["GET", "POST"])
def add():
    name = request.args.get("name")
    room = request.args.get("room")
    #? should the variable names be representative of the data they hold? considering it is a public api

    if room and name is not None:
        machines[name] = room
        print(machines)
        return {"type": "Response", "content": "Success"}, 201 # http response 201 - indicates that the request succeeded and a new resource has been created
    else:
        print(machines)
        return {"type": "Error", "content": "Failure"}, 400 # http response 400 - indicates bad request
    
@app.route('/get')
def get():
    return machines

@app.route('/ping')
def state():
    return [global_state]

if __name__ == '__main__':
    print("Server v" + __version__)
    if CARMED:
        print("Server state: " + CRED + CBOLD + CURL + CBLINK +  "ARMED" + CEND + " \nBe cautious if testing\n")
    else:
        print("Server state: " + CGREEN + "Disarmed\n" + CEND)
    time.sleep(5)
    app.run(host = '0.0.0.0')