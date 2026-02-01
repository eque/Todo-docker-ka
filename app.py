from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
import psycopg2
import os

app = Flask(__name__)
CORS(app)
def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'todos'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password')
    )

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, task, completed FROM todos')
    todos = [{'id': row[0], 'task': row[1], 'completed': row[2]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    task = request.json.get('task')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (task, completed) VALUES (%s, %s) RETURNING id', (task, False))
    todo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': todo_id, 'task': task, 'completed': False}), 201

@app.route('/init-db', methods=['POST'])
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Database initialized'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
