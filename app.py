from dotenv import load_dotenv
load_dotenv()

from db import connect, migrate, connection

if connect() is False:
    print('Database failed to connect')
else:
    migrate()

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def create_user():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def store_user():
    sql = """
        INSERT INTO users (firstname, lastname, email, age, location, date)
        VALUES('{}', '{}', '{}', {}, '{}', '{}')
        RETURNING *
    """.format(
        request.form['firstname'],
        request.form['lastname'],
        request.form['email'],
        int(request.form['age']),
        request.form['location'],
        request.form['date']
    )
    conn = connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return render_template("index.html", user=result)

@app.route('/users', methods=['GET'])
def list_users():
    sql = """
        SELECT * FROM users
    """
    conn = connection()
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("users.html", users=result)

if __name__ == "__main__":
    app.run(debug=True)