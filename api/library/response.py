# third party
from flask import jsonify

def jsonified(data, code=None):
    resp = {"data": None, "status": None, "success": None}
    if isinstance(data, Exception):  # give generic exception response
        resp['data'] = "{m} ({t})".format(m=data.message, t=str(type(data))[7:-2])
        resp['status'] = code or 500
        resp['success'] = False

    if isinstance(data, (tuple, dict, list, str, int, long, unicode)):
        resp['data'] = data
        resp['status'] = code or 200
        resp['success'] = True

    return jsonify(data=resp)

