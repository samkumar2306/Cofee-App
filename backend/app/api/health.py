from flask import Blueprint, jsonify
from app.extensions import db

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "CoFee API is running",
        "version": "1.0.0"
    }), 200


@health_bp.route("/db-test", methods=["GET"])
def db_test():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {
            "status": "success",
            "message": "Database Connected Successfully"
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }, 500