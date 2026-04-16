from flask import Flask, render_template, request, jsonify
import psycopg2
import psycopg2.extras
import os
import random

app = Flask(__name__)

CATEGORIES = {
    "faghto": "🍽️ Φαγητό",
    "poto": "🥤 Ποτό",
    "volta": "🚶 Βόλτα",
    "drasthriothta": "🎯 Δραστηριότητα",
    "meros": "📍 Μέρος",
    "syntages": "📖 Συνταγές"
}

def get_conn():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set!")
    return psycopg2.connect(url)

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ideas (
                    id SERIAL PRIMARY KEY,
                    category TEXT NOT NULL,
                    idea TEXT NOT NULL,
                    done BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
        conn.commit()

@app.route("/")
def index():
    return render_template("index.html", categories=CATEGORIES)

@app.route("/api/ideas", methods=["GET"])
def get_ideas():
    category = request.args.get("category")
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if category:
                cur.execute("SELECT * FROM ideas WHERE category=%s ORDER BY created_at DESC", (category,))
            else:
                cur.execute("SELECT * FROM ideas ORDER BY created_at DESC")
            return jsonify(list(cur.fetchall()))

@app.route("/api/ideas", methods=["POST"])
def add_idea():
    data = request.json
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO ideas (category, idea) VALUES (%s, %s) RETURNING *",
                (data["category"], data["idea"])
            )
            conn.commit()
            return jsonify(cur.fetchone())

@app.route("/api/random", methods=["GET"])
def random_idea():
    category = request.args.get("category")
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM ideas WHERE category=%s AND done=FALSE",
                (category,)
            )
            ideas = cur.fetchall()
            if not ideas:
                return jsonify({"error": "Δεν υπάρχουν διαθέσιμες ιδέες!"}), 404
            return jsonify(random.choice(ideas))

@app.route("/api/ideas/<int:idea_id>/done", methods=["PATCH"])
def mark_done(idea_id):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "UPDATE ideas SET done=TRUE WHERE id=%s RETURNING *",
                (idea_id,)
            )
            conn.commit()
            return jsonify(cur.fetchone())

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
