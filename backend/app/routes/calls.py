import config
import json
import re
import random

from app                import app, conn, cur
from flask              import Blueprint, request, make_response, jsonify
from flask_cors         import cross_origin
from json.decoder       import JSONDecodeError
from sqlite3            import IntegrityError
from app.lib.errors     import HTTPError, UnAuthError, MathFlexOperationError
from app.lib.helper     import EMAIL_REGEX

import logging

logger = logging.getLogger(__name__)

# limitations for questions
QUESTIONS_MIN = 1
QUESTIONS_MAX = 20

# set up blue prints for backend calls
url_prefix = "{}{}".format(config.CONTEXT_PATH, '/calls')
calls = Blueprint('calls', __name__, url_prefix=url_prefix)
#error handlers
@calls.app_errorhandler(404)
def handle_404(err):
    return make_response(
            jsonify({"status": "error", "response" : "Not found"}), 404
        )
@calls.app_errorhandler(405)
def handle_405(err):
    return make_response(
            jsonify({"status": "error", "response" : "Method not allowed"}), 405
        )

#/api/calls/questions
@calls.route("/questions", methods=["GET", "POST"])
@cross_origin()
def get_questions():
    """
    Endpoint: /api/calls/questions

    Description: 
    Endpoint for retrieving questions and submitting. Requires email, difficulty, and limit within body. See constants for limitations.
    Accepts/returns content-type application/json; charset=utf-8.

    Method: GET
    Query Params:
        :email (str): REQUIRED, valid email address of user.
        :limit (int): REQUIRED, Amount of questions to return.
        :difficulty (int): optional difficulty level, random if not specified.

    Returns (200):
        :status (str): success or error
        :response (str): response reflecting success or error of the request.
        :length (int): number of questions returned
        :questions (array[objects | null]): array of question objects or empty.
            *level(int): level of difficulty 
            *operation (str): type of math operation
            *problem (str): question for user
            *options(array[str]): array of string options for user
            *answer(str): the correct answer to the question
    
    Method: POST
    Body:
        :email (str): valid email address of user,
        :question (str): question that the user answered
        :answer (bool): True if the user answered correctly, else false
    
    Returns(201):
        :status (str): success or error
        :response (str): response reflecting success or error of the request.
        :updated(bool | null): True if the database was updated or null
            
    
    Responses:
        : 200 - successful request
        : 201 - successful request
        : 400 - invalid request
        : 405 - method not allowqed
        : 401 - unauthorized
        : 500 - server error
    
    """
    
    logger.info("[%s] /api/calls/questions - performing questions operations..", str(request.method))
    logger.info("Test %s %s", str(request.view_args), str(request.args))
    try:
        # if method POST, get requestions
        if request.method == "GET":
            # extract data, validate email
            if "email" not in request.args:
                raise HTTPError("Invalid request, missing email value with request.args.")
            
            if not isinstance(request.args["email"], str):
                raise HTTPError("Invalid request, email must be type string.")
            
            if not re.match(EMAIL_REGEX, request.args["email"].lower()):
                raise HTTPError("Invalid request, invalid email address format.")
            
            # get user from database, validate
            cur.execute("SELECT email, password FROM users WHERE email = ?;", (str(request.args["email"]).lower(),))
            user = cur.fetchone()
            if not user:
                raise UnAuthError("Email address does not exist.")
            
            # validate difficulty, limit
            if "difficulty" in request.args:
                if not str(request.args['difficulty']).isdigit():
                    raise HTTPError("Invalid request, difficulty must be type integer.")
                
                if 0 >= int(request.args["difficulty"]) < 8:
                    raise HTTPError("Invalid request, difficulty value must be between 1-8.")
                
            if "limit" not in request.args:
                raise HTTPError("Invalid request, missing limit value within request.body.")
            
            if not str(request.args["limit"]).isdigit():
                raise HTTPError("Invalid request, limit must be type integer.")
            
            if QUESTIONS_MIN >= int(request.args["limit"]) < QUESTIONS_MAX:
                raise HTTPError(f"Invalid request, limit must be between {QUESTIONS_MIN} - {QUESTIONS_MAX}.")
            
            # get questions from database user has not answered
            query = (
                "SELECT q.level, q.operation, q.problem, q.options, q.answer "  
                "FROM questions q "
                "LEFT JOIN users_questions uq ON uq.questionID = q.ID "
                "LEFT JOIN users u ON u.ID = uq.userID "
                "WHERE userID IS NULL "
                "AND level = ? "
                "ORDER BY RANDOM() "
                "LIMIT ?;"
            )
            
            # modify query and args depending on parameters
            if "level" not in request.args:
                query = query.replace("AND level = ?", "")
                args = ( int(request.args["limit"]),)
            else:
                args = (( int(request.args["difficulty"]), int(request.args["limit"]),))

            # get questions from databse
            cur.execute(query,args)
            questions = cur.fetchall()
            if not questions:
                raise HTTPError("Unable to collect questions.")
            
            # map options type to list 
            questions = list(
                map( lambda x: x.update({"options": eval(x['options'])}) or x, questions )
            )

            # return questions
            logger.info("Successfully generated questions %s for user %s", len(questions), user["email"])
            return make_response( jsonify({
                "status": "success",
                "response": "successfully generated questions",
                "length": len(questions),
                "questions": questions
            }),
            200)
        
        # POST operations
        elif request.method == "POST":
            # extract data, validate email
            data = json.loads(request.data)

            if "email" not in data["email"]:
                raise HTTPError("Invalid request, missing email value with request.body.")
            
            if not isinstance(data["email"], str):
                raise HTTPError("Invalid request, email must be type string.")
            
            if not re.match(EMAIL_REGEX, str(data["email"]).lower()):
                raise HTTPError("Invalid request, invalid email address format.")
            
            # get user from database, validate
            cur.execute("SELECT ID FROM users WHERE email = ?;", (str(data["email"]).lower(),))
            user = cur.fetchone()
            if not user:
                raise UnAuthError("Email address does not exist.")
            
            # validations
            if "question" not in data:
                raise HTTPError("Invalid request, question must be within request.body.")
            
            if not isinstance(data["question"], str):
                raise HTTPError("Invalid request, question value must be type string.")
            
            if "answer" not in data:
                raise HTTPError("Invalid request, answer must be within request.body.")
            
            if not isinstance(data["answer"], bool):
                raise HTTPError("Invalid request, answer value must be type boolean.")
            
            # get answers ID
            cur.execute("SELECT ID FROM questions WHERE LOWER(problem) LIKE LOWER(?);",
                ("%{}%".format(data["question"]),))
            question = cur.fetchone()
            if not question:
                raise MathFlexOperationError("Unable to locate question within database")
            
            # update users_questions table
            cur.execute("INSERT INTO users_questions (userID, questionID, correct) VALUES (?, ?, ?);",
                (user["ID"], question["ID"], data["answer"],))
            conn.commit()
            logger.info("Successfully inserted userID %s and %s questionsID into users_questions table.")
            return make_response( jsonify({
                "status": "success",
                "response": "successfully updated database with users answer",
                "updated": True
            }),
            201)
            
        else:
            return make_response(
            jsonify({"status": "error", "response" : "Method not allowed"}), 405
        )

    except HTTPError as err:
        logger.error(err)
        return make_response( jsonify({
            "status": "error",
            "response": err.args[0]
        }),
        400)
    except JSONDecodeError as err:
        logger.error("Invalid json format from request")
        return make_response( jsonify({
            "status": "error",
            "response": "Invalid request, request.body must be json format."
        }),
        400)
    except IntegrityError as err:
        logger.exception(err)
        return make_response( jsonify({
            "status": "error",
            "response": "Operations error, question already has been answer by user."
        }),
        400)
    except UnAuthError as err:
        logger.error(err)
        return make_response( jsonify({
            "status": "error",
            "response": err.args[0]
        }),
        401)
    except MathFlexOperationError as err:
        # fallback
        logger.exception(err)
        return make_response( jsonify({
            "status": "error",
            "response": err.args[0]
        }),
        500)

    except Exception as err:
        # fallback
        logger.exception(err)
        return make_response( jsonify({
            "status": "error",
            "response": "iternal service error, please contact an administrator."
        }),
        500)

