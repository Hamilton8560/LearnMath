import config
import json
import re
import logging
import hashlib

from json.decoder       import JSONDecodeError
from app                import app, conn, cur
from flask              import Blueprint, request, make_response, jsonify
from flask_cors         import cross_origin
from app.lib.auth       import hash_password, validate_pw_complexity, admin_token_required
from app.lib.errors     import HTTPError, UnAuthError, MathFlexOperationError
from app.lib.helper     import EMAIL_REGEX

logger = logging.getLogger(__name__)

# set up blue prints for backend calls
url_prefix = "{}{}".format(config.CONTEXT_PATH, '/users')
users = Blueprint('users', __name__, url_prefix=url_prefix)

#error handlers
@users.app_errorhandler(404)
def handle_404(err):
    return make_response(
            jsonify({"status": "error", "response" : "Not found"}), 404
        )
@users.app_errorhandler(405)
def handle_405(err):
    return make_response(
            jsonify({"status": "error", "response" : "Method not allowed"}), 405
        )

# route for confirming user exists
@users.route("/exists", methods=["GET"])
@cross_origin()
def email_exists():
    """
    Endpoint to confirm if a email exists with database. Accepts email address within body.
    Accepts/returns content-type application/json; charset=utf-8. 

    Body:
        :email (str): valid email address

    Returns:
        :JSON - returns jsons body with status, response
    
    Responses:
        : 200 - successful request, email address exists
        : 400 - invalid request, request is malformed or email syntax is invalid
        : 401 - unauthorized, email address does not exist
        : 500 - server error, failure due to unknown reason
    
    """
    logger.info("/api/users/exists - attempting to verify user...")
    try:
        email = str(json.loads(request.data)["email"]).lower()
        if not re.match(EMAIL_REGEX, email):
            raise ValueError("Invalid email addess syntax")
        
        cur.execute("SELECT email FROM users WHERE email = ?;", (email,))
        result = cur.fetchone()

        # if user exists
        if not result:
            raise UnAuthError("Invalid email address, please sign up to continue.")
        
        # validation passed
        logger.info("User email %s exists within database.")
        return make_response(jsonify({
            "status": "error",
            "exists": True,
            "response": "Email address exists within database"
        }), 200 )
    except UnAuthError as err:
        logger.warn(err)
        return make_response( jsonify({
            "status": "error",
            "auth": False,
            "response": err.args[0]
        }),
        401)
    
    except JSONDecodeError as err:
        logger.error("Invalid json format from request")
        return make_response( jsonify({
            "status": "error",
            "response": "Invalid request, request.body must be json format."
        }),
        400)
    except (KeyError, ValueError) as err:
        logger.error(err)
        return make_response( jsonify({
            "status": "error",
            "response": "Invalid request, email value not found or email address syntax is invalid."
        }),
        400)
    except Exception as err:
        # fallback
        logger.exception(err)
        return make_response( jsonify({
            "status": "error",
            "response": "iternal service error, please contact an administrator."
        }),
        500)
    
@users.route("/auth", methods=["GET"])
@cross_origin()
def auth():
    """
    Endpoint for authorization. Requires a valid email address and password within body.
    Accepts/returns content-type application/json; charset=utf-8. 

    Body:
        :email (str): valid email address
        :password (str): valid password

    Returns:
        :JSON - returns jsons body with status, response
    
    Responses:
        : 200 - successful request, email and password exists
        : 400 - invalid request, request is malformed or email syntax is invalid
        : 401 - unauthorized, email address does not exist or incorrect password
        : 500 - server error, failure due to unknown reason
    
    """
    logger.info("/api/users/auth - performing authorization")
    try:
        # extract data
        data = json.loads(request.data)

        #validate body
        if "email" not in data or "password" not in data:
            raise HTTPError("Missing email and password values with body.")
        
        if not re.match(EMAIL_REGEX, data["email"].lower()):
            raise UnAuthError("Invalid email address format.")
        
        # get users credentials from database
        cur.execute("SELECT email, password FROM users WHERE email = ?;", (str(data["email"]).lower(),))
        result = cur.fetchone()
        if not result:
            raise UnAuthError("Invalid email address or password.")
        
        # compare hashed passwords
        if result["password"] != hash_password(data["password"]):
            raise UnAuthError("Invalid email address or password.")
        
        # validate user account is not locked
        if not result["active"]: 
            raise UnAuthError("User account is locked.")
        
        # validation passed
        logger.info("Email address %s successfull authenticed!", data["email"])
        return make_response( jsonify({
            "status": "success",
            "auth": True,
            "response": "Successfully authenticated."
        }),
        200)
    
    except UnAuthError as err:
        logger.error(err)
        return make_response( jsonify({
            "status": "error",
            "auth": False,
            "response": err.args[0]
        }),
        401)
    except JSONDecodeError as err:
        logger.error("Invalid json format from request")
        return make_response( jsonify({
            "status": "error",
            "auth": False,
            "response": "Invalid request, must be json format."
        }),
        400)
    except (KeyError, ValueError, HTTPError) as err:
        logger.error(err)
        return make_response( jsonify({
            "status": "error",
            "auth": False,
            "response": "Invalid request, issing email and password values with body."
        }),
        400)
    except Exception as err:
        # fallback
        logger.exception(err)
        return make_response( jsonify({
            "status": "error",
            "auth": False,
            "response": "iternal service error, please contact an administrator."
        }),
        500)
    
@users.route("/create", methods=["POST"])
@cross_origin()
def create_user():
    """
    Endpoint for adding user into the databse. Requires email and password within request body. Email must not already exist.
    Accepts/returns content-type application/json; charset=utf-8.

    Body:
        :email (str): valid email address
        :password (str): valid password

    Returns:
        :status (str): success or error
        :created (bool): True if create, else False
        :response (str): response reflecting success or error of the request.
    
    Responses:
        : 201 - successful request, user created
        : 400 - invalid request, request is malformed or email syntax is invalid
        : 401 - unauthorized
        : 500 - server error, failure due to unknown reason
    
    """
    logger.info("/api/users/create - performing account creation")
    try:
        # extract data, validate
        data = json.loads(request.data)

        if "email" not in data or "password" not in data:
            raise HTTPError("Missing email and password values with body.")
        
        if not re.match(EMAIL_REGEX, data["email"].lower()):
            raise UnAuthError("Invalid email address format.")

        

        #validate body
        required_vals = ["firstName", "lastName", "email", "password"]
        if any(val not in data for val in required_vals):
            err_str = "Missing {} values within body.".format(
                ', '.join([val for val in required_vals if val not in data]))
            raise HTTPError(err_str)
        
        if not re.match(EMAIL_REGEX, str(data["email"]).lower()):
            raise HTTPError("Invalid email address format.")
        
        # see if user already exists within databse
        cur.execute("SELECT email, password FROM users WHERE email = ?;", (str(data["email"]).lower(),))
        result = cur.fetchone()
        if result:
            raise UnAuthError("Email address already exists, please sign in.")
        
        # validate password
        status, resp = validate_pw_complexity(data["password"])
        if not status:
            raise HTTPError(resp)
        
        # hash password, insert into database
        cur.execute("SELECT COUNT() FROM users;")
        user_id = cur.fetchone()['COUNT()']

        cur.execute(
            "INSERT INTO users VALUES(?, ?, ?, ?, ?);",
            (
                str(data["firstName"]).lower(),
                str(data["lastName"]).lower(),
                str(data["email"]).lower(),
                hash_password( data["password"] ),
                True,
            ))
        conn.commit()
        
        # validation passed
        logger.info("Successfully created account: ID(%s) %s, %s, %s", user_id, data["firstName"], data["lastName"], data["email"])
        return make_response( jsonify({
            "status": "success",
            "created": True,
            "response": f"Account successfully created!"
        }),
        201)
    
    except UnAuthError as err:
        logger.error(err)
        return make_response( jsonify({
            "status": "error",
            "created": False,
            "response": err.args[0]
        }),
        401)
    except HTTPError as err:
        logger.error(err)
        return make_response( jsonify({
            "status": "error",
            "created": False,
            "response": err.args[0]
        }),
        400)
    except JSONDecodeError as err:
        logger.error("Invalid json format from request")
        return make_response( jsonify({
            "status": "error",
            "created": False,
            "response": "Invalid request, request.body must be json format."
        }),
        400)

    except Exception as err:
        # fallback
        logger.exception(err)
        return make_response( jsonify({
            "status": "error",
            "created": False,
            "response": "iternal service error, please contact an administrator."
        }),
        500)
    
@users.route("/manage", methods=["POST"])
@cross_origin()
@admin_token_required
def unlock_user():
    """
    Endpoint for unlocking/locking a user account, required JWT token within header. 
    Accepts/returns content-type application/json; charset=utf-8.

    Body:
        :email (str): valid email address
        :active (bool): True to unlock account, else False

    Returns:
        :status (str): success or error
        :active (bool | null): True if account is unlocked, else False or null if unknown
        :response (str): response reflecting success or error of the request.
    
    Responses:
        : 201 - successful request, user created
        : 400 - invalid request, request is malformed or email syntax is invalid
        : 401 - unauthorized
        : 500 - server error, failure due to unknown reason
    
    """
    logger.info("/api/users/manage - performing admin unlock..")
    try:
        # extract data and validate
        data = json.loads(request.data)

        if "email" not in data or "active" not in data:
            raise HTTPError("Missing email or active value with request.body.")
        
        if not re.match(EMAIL_REGEX, data["email"].lower()):
            raise HTTPError("Invalid email address format.")
        
        if not isinstance(data['active'], bool):
            raise HTTPError("Invalid request, body.value active must be type boolean")
        
        # get user from database, validate
        cur.execute("SELECT email, password FROM users WHERE email = ?;", (str(data["email"]).lower(),))
        result = cur.fetchone()
        if not result:
            raise UnAuthError("Email address does not exist.")
        
        # unlock account
        cur.execute("UPDATE users SET active = ? WHERE email = ?;", (bool(data["active"]), str(data["email"]).lower(),))
        conn.commit()

        logger.info("Successfully set account %s, active = %s", data["email"], data["active"])
        return make_response( jsonify({
            "status": "success",
            "active": bool(data["active"]),
            "response": f"Set {data['email']}, active = {data['active']}"
        }),
        200)
    
    except UnAuthError as err:
        logger.error(err)
        return make_response( jsonify({
            "status": "error",
            "active": None,
            "response": err.args[0]
        }),
        401)
    except HTTPError as err:
        logger.error(err)
        return make_response( jsonify({
            "status": "error",
            "active": None,
            "response": err.args[0]
        }),
        400)
    except JSONDecodeError as err:
        logger.error("Invalid json format from request")
        return make_response( jsonify({
            "status": "error",
            "active": None,
            "response": "Invalid request, request.body must be json format."
        }),
        400)

    except Exception as err:
        # fallback
        logger.exception(err)
        return make_response( jsonify({
            "status": "error",
            "active": None,
            "response": "iternal service error, please contact an administrator."
        }),
        500)

