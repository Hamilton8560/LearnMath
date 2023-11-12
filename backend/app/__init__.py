from flask import Flask, make_response, jsonify, Response
from flask_cors import cross_origin
import sqlite3
import logging

from app.lib.helper import setup_logging, dict_factory, db_health_check

app = Flask(__name__)

with app.app_context():
    # init database connection
    conn = sqlite3.connect("mathflex.db", check_same_thread=False)
    cur = conn.cursor()
    cur.row_factory = dict_factory

    # turn on foreign keys
    cur.execute("PRAGMA foreign_keys = ON")

    # add logging handlers
    logger = setup_logging()
    logger.info("DB and logging setup")

#check db
db_health_check(cur, conn)

# import blue print and register to app
from app.routes.health import health
from app.routes.calls  import calls
from app.routes.users  import users

app.register_blueprint(health)
app.register_blueprint(calls)
app.register_blueprint(users)

# default error handlers
@app.errorhandler(404)
def handle_404(err):
    return make_response(
            jsonify({"status": "error", "response" : "Not found"}), 404
        )
@app.errorhandler(405)
def handle_405(err):
    return make_response(
            jsonify({"status": "error", "response" : "Method not allowed"}), 405
        )

#add headers to outgoing request
@app.after_request
def after_request(response:Response):
    """Automatically format json reponse {status: success/error, response: <str>}"""
    try:
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        
    except Exception as e:
        #fallback
        logger.exception(e)
    
    return response


