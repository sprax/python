
from __future__ import print_function
from datetime import datetime
import re
import time
from flask import Flask, flash, redirect, render_template, request, session, abort

ORDER=0

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask App!"

@app.route("/hello/<string:name>/")
def hello(name):
    # side effect:
    global ORDER
    date = datetime.now()
    tstm = date.timetuple()
    print(tstm)
    dstr = time.strftime('%Y.%m.%d_%M_%S', tstm)
    ORDER += 1
    with open("ord%2d__%s.txt" % (ORDER, dstr), "w") as logf:
        print(dstr, file=logf)
    return render_template(
        'test.html',name=name)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', port=5000)
