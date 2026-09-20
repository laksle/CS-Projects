import sqlite3
import os
import requests

from flask import Flask, request, jsonify


app = Flask(__name__)

DB = "reviews.db"
SQL = "reviews.sql"
USER = "http://127.0.0.1:9000"
COURSES = "http://127.0.0.1:9001"
#USER = "http://users:5000"  #For docker testing
#COURSES = "http://courses:5000"  #For docker testing
#USER = "http://127.0.0.1:9000" For local flask testing
#COURSES = "http://127.0.0.1:9001"  For local flask testing

db_flag = False


def create_db():
    global db_flag

    if os.path.exists(DB):
        db_flag = True
        return

    conn = sqlite3.connect(DB)

    with open(SQL, "r", encoding="utf-8") as sql_startup:
        init_db = sql_startup.read()

    cursor = conn.cursor()
    cursor.executescript(init_db)

    conn.commit()
    conn.close()

    db_flag = True


def db():
    global db_flag

    if not db_flag:
        create_db()

    conn = sqlite3.connect(DB)
    return conn


@app.route("/courses/<int:course_id>/reviews", methods=["POST"])
def create_review(course_id):

    # Check JWT through users service
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({
            "error": "authentication required"
        }), 401

    try:
        response = requests.get(
            USER + "/verify",
            headers={"Authorization": auth_header}
        )
    except requests.RequestException:
        return jsonify({
            "error": "users service unavailable"
        }), 503

    if response.status_code != 200:
        return jsonify({
            "error": "invalid or expired token"
        }), 401

    user = response.json()

    data = request.get_json(silent=True) or {}

    rating = data.get("rating")
    difficulty = data.get("difficulty")
    comment = data.get("comment", "")

    if rating is None or difficulty is None:
        return jsonify({
            "error": "rating and difficulty are required"
        }), 400

    if not isinstance(rating, int) or not isinstance(difficulty, int):
        return jsonify({
            "error": "rating and difficulty must be integers"
        }), 400

    if rating < 1 or rating > 5:
        return jsonify({
            "error": "rating must be between 1 and 5"
        }), 400

    if difficulty < 1 or difficulty > 5:
        return jsonify({
            "error": "difficulty must be between 1 and 5"
        }), 400

    # Check that course exists through courses service
    try:
        response = requests.get(
            COURSES + "/courses/" + str(course_id)
        )
    except requests.RequestException:
        return jsonify({
            "error": "courses service unavailable"
        }), 503

    if response.status_code == 404:
        return jsonify({
            "error": "course not found"
        }), 404

    if response.status_code != 200:
        return jsonify({
            "error": "courses service unavailable"
        }), 503

    db_conn = db()

    try:
        cursor = db_conn.execute("""
            INSERT INTO reviews
            (user_id, course_id, rating, difficulty, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user["user_id"],
            course_id,
            rating,
            difficulty,
            comment
        ))

        db_conn.commit()
        review_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        db_conn.close()

        return jsonify({
            "error": "you have already reviewed this course"
        }), 409

    db_conn.close()

    return jsonify({
        "id": review_id,
        "course_id": course_id,
        "user_id": user["user_id"],
        "rating": rating,
        "difficulty": difficulty,
        "comment": comment
    }), 201


@app.route("/courses/<int:course_id>/reviews", methods=["GET"])
def get_reviews(course_id):

    db_conn = db()

    rows = db_conn.execute("""
        SELECT id, user_id, rating, difficulty, comment
        FROM reviews
        WHERE course_id = ?
        ORDER BY id DESC
    """, (course_id,)).fetchall()

    db_conn.close()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "user_id": row[1],
            "rating": row[2],
            "difficulty": row[3],
            "comment": row[4]
        })

    return jsonify(result)


@app.route("/courses/<int:course_id>/summary", methods=["GET"])
def get_summary(course_id):

    # Get course information from courses service
    try:
        response = requests.get(
            COURSES + "/courses/" + str(course_id)
        )
    except requests.RequestException:
        return jsonify({
            "error": "courses service unavailable"
        }), 503

    if response.status_code == 404:
        return jsonify({
            "error": "course not found"
        }), 404

    if response.status_code != 200:
        return jsonify({
            "error": "courses service unavailable"
        }), 503

    course = response.json()

    db_conn = db()

    summary = db_conn.execute("""
        SELECT
            COUNT(*),
            AVG(rating),
            AVG(difficulty)
        FROM reviews
        WHERE course_id = ?
    """, (course_id,)).fetchone()

    db_conn.close()

    review_count = summary[0]

    if review_count == 0:
        average_rating = None
        average_difficulty = None
    else:
        average_rating = round(summary[1], 2)
        average_difficulty = round(summary[2], 2)

    return jsonify({
        "course": course,
        "review_count": review_count,
        "average_rating": average_rating,
        "average_difficulty": average_difficulty
    })


@app.route("/clear", methods=["GET"])
def clear():
    global db_flag

    if os.path.exists(DB):
        os.remove(DB)

    db_flag = False

    return jsonify({
        "message": "database cleared"
    })
