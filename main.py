import os

import requests
from flask import Flask
from flask import request
from flask import redirect
from flask import abort

import base62
import database


app = Flask(__name__)
database.verify_db()

HOST = os.getenv('OOMPA_HOSTNAME', '0.0.0.0')
DEBUG = os.getenv('OOMPA_DEBUG', False)
REDIRECT_ON_ERROR = os.getenv('OOMPA_REDIRECT_ON_ERROR', None)


def as_url(pk):
    code = base62.dehydrate(pk + 9999)
    print pk, code
    return "http://" + request.host + "/" + code


@app.route('/_/shorten')
def api_shorten():
    long_url = request.args.get('url')
    verify = bool(request.args.get('verify', True))
    if verify:
        try:
            response = requests.get(long_url)
        except:
            return "Cannot access url"
        else:
            if response.status_code != 200:
                return "Cannot access url"

    exists = database.get_by_url(long_url)
    if exists:
        return as_url(exists[0])

    pk = database.save(long_url)
    return as_url(pk)


@app.route('/<path:code>')
def redirect_code(code):
    try:
        pk = base62.saturate(code) - 9999
        url = database.get_by_id(pk)
    except:
        if REDIRECT_ON_ERROR is not None:
            return redirect(REDIRECT_ON_ERROR)
        else:
            return abort(400)
    if url is None:
        if REDIRECT_ON_ERROR is not None:
            return redirect(REDIRECT_ON_ERROR)
        else:
            return abort(404)
    else:
        return redirect(url[0])


if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST)
