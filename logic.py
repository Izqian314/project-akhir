import sqlite3

conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

#tabel1 Pesawat

cursor.execute("""
CREATE TABLE IF NOT EXISTS aircraft (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    type TEXT,
    manufacturer TEXT,
    description TEXT
);
""")
# Tabel2 QnA
cursor.execute("""CREATE TABLE IF NOT EXISTS qa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT,
    category TEXT
);
""")
# tabel3 Feedback
cursor.execute("""CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    message TEXT,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);     
""")

#tabel4 quiz
cursor.execute("""CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    correct_answer TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT
);
""")
#tabel5 Quiz score
cursor.execute("""CREATE TABLE IF NOT EXISTS quiz_score (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    score INTEGER
);
""")
conn.commit()
conn.close()


# fungsi def

def get_connection():
    return sqlite3.connect("db.sqlite")

'''print("hello world")'''
def add_qa(question, answer, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO qa(question,answer,category) VALUES (?,?,?)""",(question,answer,category))
    conn.commit()
    conn.close()
    pass
def get_question(question):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM qa WHERE LOWER(question) LIKE ?",
        (f"%{question.lower()}%",)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return "Pertanyaan tidak ditemukan di data"
    pass
def add_feedback(username, message, rating):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO feedback (username, message, rating)
    VALUES (?, ?, ?)
    """, (username, message, rating))
    conn.commit()
    conn.close()
    pass

def get_quiz():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz")
    quiz_list = cursor.fetchall()
    conn.close()
    return quiz_list
    pass
