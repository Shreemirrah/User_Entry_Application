import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def create_users_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        name TEXT,
                        email TEXT UNIQUE,
                        boolean_value BOOLEAN,
                        favorite_number INTEGER
                    )''')
    conn.commit()

def create_user(conn, user):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE name=? AND boolean_value=? AND favorite_number=?",
                       (user['name'], user['boolean_value'], user['favorite_number']))
        existing_users = cursor.fetchone()[0]
        if existing_users > 0:
            return {"error": "User with the same name, boolean value, and favorite number already exists."}
        cursor.execute("INSERT INTO users (name, email, boolean_value, favorite_number) VALUES (?, ?, ?, ?)",
                       (user['name'], user['email'], user['boolean_value'], user['favorite_number']))
        conn.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e):
            return {"error": "Email address already exists."}
        else:
            return {"error": str(e)}
    return {"message": "User created successfully."}

@app.route('/users', methods=['POST'])
def create_user_endpoint():
    conn = sqlite3.connect('users.db')
    create_users_table(conn)
    user = request.get_json()
    result = create_user(conn, user)
    conn.close()
    return jsonify(result)

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    create_users_table(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [{'name': row[0], 'email': row[1], 'boolean_value': row[2], 'favorite_number': row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)






















"""
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def create_user(conn, user):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, boolean_value, favorite_number) VALUES (?, ?, ?, ?)",
                       (user['name'], user['email'], user['boolean_value'], user['favorite_number']))
        conn.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e):
            return {"error": "Email address already exists."}
        else:
            return {"error": str(e)}
    return {"message": "User created successfully."}

@app.route('/users', methods=['POST'])
def create_user_endpoint():
    conn = sqlite3.connect('users.db')
    user = request.get_json()
    result = create_user(conn, user)
    conn.close()
    return jsonify(result)

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = [{'name': row[0], 'email': row[1], 'boolean_value': row[2], 'favorite_number': row[3]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)




from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        boolean_value INTEGER,
        favorite_number INTEGER
    )
''')
conn.commit()

@app.route('/users', methods=['POST'])
def create_user():
    email = request.json['email']
    boolean_value = request.json['booleanValue']
    favorite_number = request.json['favoriteNumber']
    cursor.execute('''
        INSERT INTO users (email, boolean_value, favorite_number)
        VALUES (?, ?, ?)
    ''', (email, boolean_value, favorite_number))
    conn.commit()
    return jsonify({'message': 'User created successfully'})

@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return jsonify([{'email': user[0], 'booleanValue': user[1], 'favoriteNumber': user[2]} for user in users])

if __name__ == '__main__':
    app.run(debug=True)
"""