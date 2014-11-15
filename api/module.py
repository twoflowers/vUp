import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from endpoints.setup import app

if __name__ == "__main__":
    app.run(host='0.0.0.0')


