from flask import Flask, Response, request
from datetime import datetime
import json
from ApiResources.CustomerContactCompose import CustomerContactCompose
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "Customers-Contacts-Microservice",
        "health": "Good",
        "at time": t
    }
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    return result


@app.route("/api/customercontactcompose/", methods=["GET"])
def get_info():

    result = CustomerContactCompose.get_info()
    rsp = Response(json.dumps(result), status=200, content_type='application/json')
    return rsp


@app.route("/api/customercontactcompose/<id>", methods=["GET"])
def get_info_by_id(id):
    rsp = CustomerContactCompose.get_info(id)
    if rsp is None or len(rsp) == 0:
        rsp = Response("Info not found!", status=404, content_type="text/plain")
    else:
        rsp = Response(json.dumps(rsp, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5012)
