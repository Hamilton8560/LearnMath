# library for hashing passwords
import hashlib
import config
import re
import jwt
import logging
import string

from datetime import datetime
from pytz import timezone
from functools import wraps
from flask import request, jsonify, make_response
from jwt.exceptions import DecodeError as JWTError

logger = logging.getLogger(__name__)

# password salt
SECRET_KEY = config.SECRET_KEY

# token helpers
PREFIX = 'Bearer '
UNLOCK_ENDPOINT = "/api/users/manage"

#password constraints
PW_LEN_MIN = 8
PW_LEN_MAX = 16

def hash_password(password):
    """ Return hashed password with salt"""
    return hashlib.sha256((SECRET_KEY + password).encode()).hexdigest()

def validate_pw_complexity(password):
    """ Validate password complexity based upon restraints"""
    if not PW_LEN_MIN <= len(password) <= PW_LEN_MAX:
        return False, f"Password range must be between ({PW_LEN_MIN}-{PW_LEN_MAX}) characters."
    elif not re.search(r"[A-Z]", password):
        return False, "Password must contain 1 uppercase character."
    elif not re.search(r"[a-z]", password):
        return False, "Password must container 1 lowercase chatacter."
    elif not re.search(r"[0-9]", password):
        return False, "Password must contain 1 numeric character."
    elif not any(chars in string.punctuation for chars in password):
        return False, "Password must contain 1 special character."
    else:
        return True, "success"
    
def admin_token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            token = request.headers["authorization"]
        except KeyError as e:
            return make_response(
                jsonify({
                    "status" : "error",
                    "response": "Authorization missing"
            }), 
            401)
        
        try:
            if not token.startswith(PREFIX):
                raise UnAuthError("Authorization must be a Bearer Token")
            
            token = token[len(PREFIX):]
            logger.info(SECRET_KEY)

            decoded_token = jwt.decode(
                token, SECRET_KEY, algorithms=["HS256"]
            )

            if decoded_token["type"] != "admin":
                raise UnAuthError("Invalid token for endpoint")
            
            if datetime.now(timezone('UTC')) > datetime.fromisoformat(decoded_token["expires"]):
                raise UnAuthError("Bearer token has expired, please generate a new one")
            
            logger.info("Admin token verified")
            return f(*args, **kwargs)
        
        except JWTError as err:
            logger.exception(err)
            return make_response(
                jsonify({
                    "status" : "error",
                    "response": "Invalid JWT token"
            }), 
            401)
        except UnAuthError as err:
            logger.error(err)
            return make_response(
                jsonify({
                    "status" : "error",
                    "response": err.args[0]
            }), 
            401)
        except Exception as err:
            logger.exception(err)
            return make_response(
                jsonify({
                    "status" : "error",
                    "response": "Unable to authentication token due to unknown error"
            }), 
            500)
    return wrap

class UnAuthError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "UnAuthError - {}".format(*self.args)