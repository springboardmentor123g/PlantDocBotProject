import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Users table created")
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT OR IGNORE INTO users (email, password, role)
VALUES ('admin@gmail.com', 'admin123', 'admin')
""")

conn.commit()
conn.close()

print("Admin user inserted")
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT OR IGNORE INTO users (email, password, role)
VALUES ('farmer@gmail.com', 'farmer123', 'farmer')
""")

conn.commit()
conn.close()

print("Farmer user inserted")

import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS diseases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease TEXT NOT NULL,
    symptoms TEXT,
    prevention TEXT
)
""")

conn.commit()
conn.close()

print("✅ diseases table created successfully")
