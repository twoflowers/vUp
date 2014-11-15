# third party
from flask import jsonify

def jsonified(item):
    return jsonify(data=[item] if isinstance(item, dict) else item)

