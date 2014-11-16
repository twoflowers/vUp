# Built-in
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from endpoints.setup import app

app.run(host='0.0.0.0')
# Don't call app.run()
# app.run() will be called by uwsgi
