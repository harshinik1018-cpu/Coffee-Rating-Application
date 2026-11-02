
from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("coffee.db")

@app.route("/")
def home():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY,
            name TEXT,
            votes INTEGER DEFAULT 0
        )
    """)
    count = db.execute("SELECT COUNT(*) FROM coffee").fetchone()[0]

    if count == 0:
        db.executemany(
            "INSERT INTO coffee (name) VALUES (?)",
            [("Espresso",), ("Cappuccino",), ("Latte",)]
        )
        db.commit()

    coffees = db.execute("SELECT * FROM coffee").fetchall()
    db.close()
    return render_template("index.html", coffees=coffees)

@app.route("/vote/<int:coffee_id>")
def vote(coffee_id):
    db = get_db()
    db.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id = ?",
        (coffee_id,)
    )
    db.commit()
    db.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
