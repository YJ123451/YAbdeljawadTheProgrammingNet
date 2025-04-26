from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__,
            template_folder='templates',
            static_url_path='/static',
            )

DB_FILE = "login.db"
    
sqliteConnection = sqlite3.connect(DB_FILE)
cursor = sqliteConnection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL)
''')
sqliteConnection.commit()
sqliteConnection.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods =['GET','POST'])
def login():
    conn = sqlite3.connect('login.db')
    c = conn.cursor
    error = None
    if request.method == 'POST':
        username = request.form['username']

    return render_template('login.html')
    















if __name__ == '__main__': 
    app.run(debug = True)