
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

@app.route('/order', methods=['GET', 'POST'])
def foo(x=None, y=None):
    # do something to process order
    print("Got order at time %d seconds." % time.time())
    return render_template(
        'test.html',name="Thanks!")


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
        print(dstr)
    return render_template(
        'test.html',name=name)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', port=5000)
