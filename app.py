from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__,
            template_folder='templates',
            static_url_path='/static',
            )

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')
















if __name__ == '__main__': 
    app.run(debug = True)