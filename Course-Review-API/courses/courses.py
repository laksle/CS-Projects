import sqlite3
import os

from flask import Flask, request, jsonify
import requests

#USER = "http://users:5000"
USER = "http://127.0.0.1:9000"
app = Flask(__name__)

DB = "courses.db"
SQL = "courses.sql"

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


@app.route("/courses", methods=["POST"])
def create_course():

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

    data = request.get_json(silent=True) or {}

    code = data.get("code")
    name = data.get("name")
    professor = data.get("professor")

    if not code or not name or not professor:
        return jsonify({
            "error": "code, name, and professor are required"
        }), 400

    db_conn = db()

    try:
        cursor = db_conn.execute("""
            INSERT INTO courses (code, name, professor)
            VALUES (?, ?, ?)
        """, (code, name, professor))

        db_conn.commit()
        course_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        db_conn.close()

        return jsonify({
            "error": "course already exists"
        }), 409

    db_conn.close()

    return jsonify({
        "id": course_id,
        "code": code,
        "name": name,
        "professor": professor
    }), 201
@app.route("/courses", methods=["GET"])
def get_courses():
    db_conn = db()

    rows = db_conn.execute("""
        SELECT id, code, name, professor
        FROM courses
        ORDER BY code
    """).fetchall()

    db_conn.close()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "code": row[1],
            "name": row[2],
            "professor": row[3]
        })

    return jsonify(result)


@app.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    db_conn = db()

    course = db_conn.execute("""
        SELECT id, code, name, professor
        FROM courses
        WHERE id = ?
    """, (course_id,)).fetchone()

    db_conn.close()

    if course is None:
        return jsonify({
            "error": "course not found"
        }), 404

    return jsonify({
        "id": course[0],
        "code": course[1],
        "name": course[2],
        "professor": course[3]
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
