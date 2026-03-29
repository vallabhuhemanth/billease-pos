from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# secret key for session
app.secret_key='admin_secret_123'

# mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '970056'
app.config['MYSQL_DB'] = 'pos_billing'

mysql=MySQL(app)

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (name, email, message)
    )
    mysql.connection.commit()
    cursor.close()

    return render_template('index.html', success=True)

# amdin login route
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin']= True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid Username or Password!'
    return render_template('login.html', error=error)

# Admin dashboard route
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('login.html'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
    messages = cursor.fetchall()
    cursor.close()

    return render_template('admin.html',messages=messages)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)