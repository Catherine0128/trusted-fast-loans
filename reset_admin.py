import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("loans.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     username TEXT UNIQUE,
     password TEXT
)
""")

cursor.execute("DELETE FROM admins")

hashed_password = generate_password_hash("admin123")

cursor.execute("INSERT INTO admins (username,password) VALUES (?, ?)",
               ("admin", hashed_password))

conn.commit()
conn.close()

print("Admin resert complete")