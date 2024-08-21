from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_PATH = '/data/guestbook.db'
RESET_PASSWORD = os.getenv('RESET_PASSWORD', 'password')  # Default password

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS entries (name TEXT, message TEXT)')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('INSERT INTO entries (name, message) VALUES (?, ?)', (name, message))

    entries = []
    with sqlite3.connect(DB_PATH) as conn:
        entries = conn.execute('SELECT * FROM entries').fetchall()

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Guestbook</title>
        <style>
            body { background-color: black; color: white; font-family: 'Courier New', monospace; }
            input, textarea, button { background-color: #333; color: white; border: 1px solid #555; padding: 5px; }
            textarea { resize: none; }
            button { cursor: pointer; }
            button:hover { background-color: #555; }
            .entry { margin-bottom: 10px; border-bottom: 1px solid #555; padding-bottom: 5px; }
        </style>
    </head>
    <body>
        <h1>Guestbook</h1>
        <form method="post">
            <label>Name: <input type="text" name="name" required></label><br><br>
            <label>Message:<br><textarea name="message" rows="4" cols="50" required></textarea></label><br><br>
            <button type="submit">Post</button>
        </form>
        <hr>
        <h1>Entries:</h1>
        <div>
            {% for entry in entries %}
                <div class="entry">
                    <strong>{{ entry[0] }}:</strong> {{ entry[1] }}
                </div>
            {% endfor %}
        </div>
        <hr>
        <a href="{{ url_for('reset') }}">Reset Guestbook</a>
    </body>
    </html>
    '''

    return render_template_string(html, entries=entries)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        password = request.form['password']
        if password == RESET_PASSWORD:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute('DELETE FROM entries')
            return redirect(url_for('index'))
        else:
            error = "Incorrect password. Please try again."
            return render_template_string(reset_html, error=error)
    
    reset_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reset Guestbook</title>
        <style>
            body { background-color: black; color: white; font-family: 'Courier New', monospace; }
            input, button { background-color: #333; color: white; border: 1px solid #555; padding: 5px; }
            button { cursor: pointer; }
            button:hover { background-color: #555; }
        </style>
    </head>
    <body>
        <h1>Reset Guestbook</h1>
        <form method="post">
            <label>Password: <input type="password" name="password" required></label><br><br>
            <button type="submit">Delete All Entries</button>
        </form>
        {% if error %}
        <p style="color: red;">{{ error }}</p>
        {% endif %}
    </body>
    </html>
    '''

    return render_template_string(reset_html)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
