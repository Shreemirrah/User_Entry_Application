from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        name TEXT,
        boolean_value INTEGER,
        favorite_number INTEGER,
        UNIQUE (name, boolean_value, favorite_number)
    )
''')
def create_user(conn, user):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, boolean_value, favorite_number) VALUES (?, ?, ?, ?)",
                       (user['name'], user['email'], user['boolean_value'], user['favorite_number']))
        conn.commit()
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e):
            return {"error": "Not a unique user."}
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