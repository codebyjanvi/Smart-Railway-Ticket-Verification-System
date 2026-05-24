import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# ---------------- TICKETS ----------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS tickets(

    ticket_id TEXT,
    name TEXT,
    phone TEXT,
    source TEXT,
    destination TEXT,
    date TEXT,
    seat TEXT,
    bogie TEXT,
    pnr TEXT,
    face_image TEXT
    status TEXT DEFAULT 'unused'
)

""")

# ---------------- VERIFIED ----------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS verified_tickets(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    ticket_id TEXT,
    name TEXT,
    phone TEXT,
    source TEXT,
    destination TEXT,
    date TEXT,
    seat TEXT,
    bogie TEXT,
    pnr TEXT,
    face_image TEXT,
    verified_time TEXT

)

""")

# ---------------- USERS ----------------

cursor.execute("""

CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,
    password TEXT,
    role TEXT

)

""")

# ---------------- USERS INSERT ----------------

cursor.execute("DELETE FROM users")

cursor.execute("""

INSERT INTO users(username,password,role)
VALUES('admin','123','admin')

""")

cursor.execute("""

INSERT INTO users(username,password,role)
VALUES('tte','123','tte')

""")

conn.commit()

conn.close()

print("✅ Database Created Successfully")