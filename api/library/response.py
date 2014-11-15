# third party
from flask import jsonify

def jsonified(data):
    resp = {"data": None, "status": 200, "success": True}
    if isinstance(data, Exception):  # give generic exception response
        resp['data'] = "{m} ({t})".format(m=data.message, t=str(type(data))[7:-2])
        resp['status'] = 500
        resp['success'] = False

    if isinstance(data, (tuple, dict, list, str, int, long, unicode)):
        resp['data'] = data

    return jsonify(data=resp)

