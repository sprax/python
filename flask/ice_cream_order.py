
from __future__ import print_function
from datetime import datetime
import pdb;
from pdb import set_trace
import time
from flask import Flask, flash, redirect, render_template, request, session, abort

ORDER=0

app = Flask(__name__)

@app.route("/")
def index():
    return "Flask App!"


@app.route("/order/<string:bin_name>/<int:num_scoops>", methods=['GET', 'POST'])
def order(bin_name=None, num_scoops=None):
    # do something to process order
    global ORDER
    print("Got order at time %d seconds." % time.time())
    date = datetime.now()
    tstm = date.timetuple()
    print(tstm)
    dstr = time.strftime('%Y.%m.%d_%M_%S', tstm)
    ORDER += 1
    file_name = "order_%2d_%s.txt" % (ORDER, dstr)
    contents = "%s" % (file_name)
    set_trace()
    with open("log/" + file_name, "w") as log_file:
        print(contents, file=log_file)
        print(contents)
    # return render_template('test.html', message="Thanks,", name=name)
    return render_template('ice_cream.html', name="Thanks!")


@app.route("/hello/<string:name>/")
def hello(name):
    return render_template('ice_cream.html', name=name)

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', port=8000)
