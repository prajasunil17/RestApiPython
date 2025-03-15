from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="testdb"
)
cursor = conn.cursor()

# Home Page - Show All Users
@app.route('/')
def index():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

# Add User
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    return redirect('/')

# Edit User Page
@app.route('/edit/<int:user_id>')
def edit_page(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    return render_template('edit.html', user=user)

# Update User
@app.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    name = request.form['name']
    email = request.form['email']
    cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
    conn.commit()
    return redirect('/')

# Delete User
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
