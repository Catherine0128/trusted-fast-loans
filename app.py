

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "loans.db")

print("USING DATABASE:", DB_PATH)

app = Flask(__name__)
app.secret_key = "trusted_fast_loans_secret_2026"

def init_db():

    conn = sqlite3.connect(DB_PATH)

    conn = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loan_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        amount REAL,
        loan_type TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/apply-loan", methods=["POST"])
def apply_loan():
    name = request.form.get("name")
    phone = request.form.get("phone")
    amount = request.form.get("amount")
    loan_type = request.form.get("loan_type")
    print("LOAN TYPE RECEIVED:", loan_type)
   
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO loan_applications (name, phone, amount, loan_type, status)
        VALUES(?, ?, ?, ?, ?)
    """, (name, phone, amount, loan_type, "Pending"))

    conn.commit()
    conn.close()

    return f"Application received from {name}")

@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, phone, amount, loan_type, status 
    FROM loan_applications 
    ORDER BY id DESC
    """)

    loans = cursor.fetchall()

    conn.close()
    
    print("LOANS FOUND:", len(loans))

    return render_template("admin.html",loans=loans)

@app.route("/approve/<int:loan_id>")
def approve_loan(loan_id):

    print("APPROVE CLICKED:", loan_id)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE loan_applications 
    SET status=? 
    WHERE id=?
    """, ("Approved", loan_id))

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/reject/<int:loan_id>")
def reject_loan(loan_id):

    print("REJECT CLICKED:", loan_id)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
 
    cursor.execute("""
    UPDATE loan_applications
    SET status=? 
    WHERE id=?
    """, ("Rejected", loan_id))

    conn.commit()
    conn.close()

    return redirect ("/admin")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM admins WHERE username=?",
             (username,)
        )

        admin = cursor.fetchone()
        conn.close()

        if admin and check_password_hash(admin[2], password):
                session["admin_logged_in"] = True
                return redirect("/admin")

        flash("invalid username or password", "danger")

    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/admin/login")

if __name__ == "__main__":
     app.run(debug=True)
