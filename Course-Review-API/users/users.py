from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import Jwt

app = Flask(__name__)

DB = "users.db"
SQL = "users.sql"

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


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "username and password are required"
        }), 400

    if len(password) < 6:
        return jsonify({
            "error": "password must be at least 6 characters"
        }), 400

    password_hash = generate_password_hash(password)

    conn = db()

    try:
        cursor = conn.execute("""
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))

        conn.commit()

        user_id = cursor.lastrowid

    except sqlite3.IntegrityError:
        conn.close()

        return jsonify({
            "error": "username already exists"
        }), 409

    conn.close()

    return jsonify({
        "id": user_id,
        "username": username
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "username and password are required"
        }), 400

    conn = db()

    user = conn.execute("""
        SELECT id, username, password_hash
        FROM users
        WHERE username = ?
    """, (username,)).fetchone()

    conn.close()

    if user is None:
        return jsonify({
            "error": "invalid username or password"
        }), 401

    if not check_password_hash(user[2], password):
        return jsonify({
            "error": "invalid username or password"
        }), 401

    token = Jwt.create_jwt(
        user[0],
        user[1]
    )

    return jsonify({
        "token": token
    })


@app.route("/verify", methods=["GET"])
def verify():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({
            "error": "authentication required"
        }), 401

    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return jsonify({
            "error": "invalid authorization header"
        }), 401

    token = parts[1]

    payload = Jwt.decode_jwt(token)

    if payload is None:
        return jsonify({
            "error": "invalid or expired token"
        }), 401

    return jsonify({
        "user_id": payload["user_id"],
        "username": payload["username"]
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
