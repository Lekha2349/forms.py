import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("forms.db", check_same_thread=False)
cursor = conn.cursor()

# Table creation
cursor.execute("""
CREATE TABLE IF NOT EXISTS fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS forms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS form_fields (
    form_id INTEGER,
    field_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_id INTEGER,
    response_data TEXT
)
""")
conn.commit()

# ----------------- Backend Functions -----------------

def create_field(name, ftype):
    cursor.execute("INSERT INTO fields (name, type) VALUES (?, ?)", (name, ftype))
    conn.commit()

def list_fields():
    cursor.execute("SELECT * FROM fields")
    return cursor.fetchall()

def create_form(name):
    cursor.execute("INSERT INTO forms (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid

def list_forms():
    cursor.execute("SELECT * FROM forms")
    return cursor.fetchall()

def link_field_to_form(form_id, field_id):
    cursor.execute("INSERT INTO form_fields (form_id, field_id) VALUES (?, ?)", (form_id, field_id))
    conn.commit()

def get_form(form_id):
    cursor.execute("SELECT * FROM forms WHERE id = ?", (form_id,))
    return cursor.fetchone()

def get_fields_for_form(form_id):
    cursor.execute("""
        SELECT fields.id, fields.name, fields.type
        FROM fields
        JOIN form_fields ON fields.id = form_fields.field_id
        WHERE form_fields.form_id = ?
    """, (form_id,))
    return cursor.fetchall()

def start_response(form_id):
    return {"form_id": form_id, "answers": {}}

def save_answer(response, field_name, value):
    response["answers"][field_name] = value

def get_responses_for_form(form_id):
    cursor.execute("SELECT response_data FROM responses WHERE form_id = ?", (form_id,))
    return cursor.fetchall()

def submit_response(response):
    form_id = response["form_id"]
    response_data = str(response["answers"])
    cursor.execute("INSERT INTO responses (form_id, response_data) VALUES (?, ?)", (form_id, response_data))
    conn.commit()
