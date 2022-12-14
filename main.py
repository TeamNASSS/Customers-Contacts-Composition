from flask import Flask, Response, request
from datetime import datetime
import json
from gevent import monkey
from ApiResources.CustomerContactCompose import CustomerContactCompose
from flask_cors import CORS
from Utils.Validations import is_valid_address
from datetime import date

# Create the Flask application object.

# needed to fix a grequests issue - https://github.com/miguelgrinberg/Flask-SocketIO/issues/65#issuecomment-60697013
monkey.patch_all()

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

@app.route("/api/customercontactcompose/", methods=["POST"])
def add_user():
    """
        This Method is called only once per user, when a new user is joining this EP will initialize their
        Contact, user info.
    :return: TBD
    """
    data = request.get_json()
    data["cid"] = request.headers['authCID']
    data["email"] = request.headers['email']
    data["doj"] = str(date.today())
    print(data["cid"], data["email"], "?Headers!!")

    # Todo: check if user is already initialized. if yes return 400 bad request
    current_user = CustomerContactCompose.get_info(data['cid'])
    if current_user is not None:
        print("current_user is not None")
        return Response("User already exists!", status=400, content_type="text/plain")

    print("current_user is ", current_user)

    if not is_valid_address(data):
        return Response(json.dumps("Invalid address was provided", default=str),
                        status=400, content_type="application/json")

    result = CustomerContactCompose.add_info(data)
    print("Added Customer!!")
    return result

@app.route("/api/customercontactcompose/", methods=["PUT"])
def update_user():
    """
        PUT for customercontactcompose
    """
    data = request.get_json()
    data["cid"] = request.headers['authCID']
    data["email"] = request.headers['email']

    result = CustomerContactCompose.update_info(data)

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5012)
