import config
import os
import json
import logging

from flask import current_app as app

from logging.handlers import RotatingFileHandler
from app.lib.auth import hash_password

logger = logging.getLogger(__name__)

# paths to sql schemas and data
SCHEMAS_DIR =  os.path.join(os.path.dirname(os.path.dirname(__file__)), "schemas")
DATA_DIR =  os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# tables
TABLES = ["users", "questions", "users_questions"]

# regex for email validation
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


LOGGING_LEVEL = {
    "DEBUG"     : logging.DEBUG,
    "INFO"      : logging.INFO,
    "WARNING"   : logging.WARNING,
    "ERROR"     :logging.ERROR,
    "CRITICAL"  :logging.CRITICAL,
    "FATAL"     :logging.FATAL
}

# dictionary factory for cursor
def dict_factory(cursor, row):
    """ convert all cursor output to dict """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_questions_data():
    ret = []
    seen = set() # for duplicates
    for file in os.listdir(DATA_DIR):
        data = json.load(open(os.path.join(DATA_DIR, file), 'r'))
        for v in data['questions']:
            if v['question'] not in seen:
                ret.append(
                    (
                        data["difficulty"], 
                        str(v['type']), 
                        str(list(str(i) for i in v['question'])), 
                        str(v['options']), 
                        str(v['answer'])
                ))
            seen.add(v["question"]) 

    return ret 

    

def db_health_check(cur, conn):
    """ confirm all tables and data exists within table"""
    for table in TABLES:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table,))
        result = cur.fetchone()

        # Check table existance
        if not result:
            cur.execute( open(os.path.join(SCHEMAS_DIR, f"{table}.sql")).read() )
            conn.commit()
            logger.warn("Table %s not found within database - generated empty table with no data.", table)
        
        # check data exsistance
        cur.execute(f"SELECT * FROM {table};")
        if not cur.fetchall():
            # insert question data
            if table == "questions":
                data = get_questions_data()
                conn.executemany(
                    "INSERT INTO questions (level, operation, problem, options, answer) " + \
                    "VALUES (?, ?, ?, ?, ?)",
                    data,
                    )
                conn.commit()

                cur.execute("select * from questions;")
                total = len(cur.fetchall())
                cur.execute("select distinct level, count() from questions group by level;")
                lvl_questions = cur.fetchall()

                logger.warning("Table %s empty - auto-populated with %s questions: %s", table, total, lvl_questions)

            # insert test user
            elif table == "users":
                cur.execute("INSERT INTO users (firstName,lastName,email,password,active) " + \
                            "VALUES (?,?,?,?,?);",
                            ( "foo", "bar","foo.bar@email.com", hash_password("Test123!"), True, )
                            )
                conn.commit()
                logger.warning("Table %s empty - auto-populated with user=foo.bar@email.com, pw=Test123!")




# Init logger for flask_app, depending on debug mode
def setup_logging():
    app.logger.handlers.clear()
    formatter = logging.Formatter(
            "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler( config.LOGFILE_LOCATION , maxBytes=10000000, backupCount=5)
    file_handler.setLevel(LOGGING_LEVEL[config.LOG_LEVEL])
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOGGING_LEVEL[config.LOG_LEVEL])
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    app.logger.setLevel(LOGGING_LEVEL[config.LOG_LEVEL])
    return app.logger
