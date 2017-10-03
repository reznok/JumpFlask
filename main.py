import hashlib
import datetime
import sqlite3
import json

from flask import Flask, request

app = Flask(__name__)

def round_down(num, divisor):
    return num - (num%divisor)


@app.route('/')
def index():
    content = """
    Welcome Back Reznok!<br>
    <br>
    <a href="/admin/29badee7cb2803331016ab554584eccc">Admin Page</a>
    <br>
    <br>
    Last Login: 135420<br><br>
    Hackers Beware: You'll never get into my admin page if it's always moving! 
    """
    return content


@app.route('/admin/<endpoint>')
def word_up(endpoint):
    m = hashlib.md5()

    hour = str(datetime.datetime.now().hour).zfill(2)
    minute = str(datetime.datetime.now().minute).zfill(2)
    seconds = str(round_down(int((datetime.datetime.now().second)), 10)).zfill(2)

    m.update("".join([hour, minute, seconds]))

    ex_endpoint = m.hexdigest()

    print("Time: {}".format("".join([hour, minute, seconds])))
    print("In: {}".format(endpoint))
    print("Expected: {}".format(ex_endpoint))

    if endpoint.lower() == ex_endpoint.lower():
        id_ = request.args.get("id")

        if id_ is not None:
            if "union" in id_.lower():
                return "Stop That!"

            sql = "SELECT * FROM Products WHERE ID = '{}'".format(id_)
            conn = sqlite3.connect("jumpy.db")
            c = conn.cursor()
            c.execute(sql)
            return json.dumps(c.fetchall())

        content = """
        FLAG{jumpy_jumpy_jumpy}<br><br>
        Welcome to the Product Lookup Page!
        <br><br>
        
        <form action="">
        Product Id: <input type="text" name="id">
        <input type="submit" value="Go">
        </form>
        """

        return content

    return "Link Expired <br><br><br>The Current Time Is: {}{}{}".format(hour, minute, seconds)


if __name__ == '__main__':
    m = hashlib.md5()
    hour = str(datetime.datetime.now().hour).zfill(2)
    minute = str(datetime.datetime.now().minute).zfill(2)
    seconds = str(round_down(int((datetime.datetime.now().second)), 10)).zfill(2)

    m.update("".join([hour, minute, seconds]))
    print (m.hexdigest())
    app.debug = True
    app.run("0.0.0.0", port=80)


