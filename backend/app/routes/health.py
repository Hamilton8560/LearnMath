import config
from flask import Blueprint, make_response, jsonify

url_prefix = "{}{}".format(config.CONTEXT_PATH, '/health')
health = Blueprint('health', __name__, url_prefix=url_prefix)

# Menu interactions
# The endpoint Slack will provide health check status
@health.route("/status", methods=["GET"])
def health_status():
    return make_response(
            jsonify({"service" : "Running"}), 200
        )