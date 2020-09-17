
from wsgiref import simple_server

from flask import Flask, request, make_response
import json
import os
import requests



app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/webhook', methods=['POST'])
# @cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req))
    res = processRequest(req)
    res = json.dumps(res)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    state = parameters.get("geo-state")
    print(state)
    if state == "India":
        state = "Total"
    if state == "india":
        state = "Total"
    if state == "total corona cases":
        state = "Total"

    response = requests.get("https://api.covid19india.org/data.json").json()
    print("Length ", len(response["statewise"]))
    noofstate = len(response["statewise"])
    for data in response["statewise"]:
        if data["state"] == state:
            message = "Active: " + data["active"] + " Confirmed: " + data["confirmed"] + " Recovered: " + data[
                "recovered"] + " TotalDeath: " + data["deaths"] + " NewCases: " + data["deltaconfirmed"] + " On " + data[
                          "lastupdatedtime"]  + " \n \n 1.Enter State Name \n 2.Ask Later"

            return {
                "fulfillmentText": message,
                "displayText": message



            }







port = int(os.getenv("PORT"))

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()

# if __name__ == "__main__":
#     app.run(debug=True)



