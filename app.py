from flask import Flask, render_template, request, redirect, flash, url_for
import pymysql

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configuración de la base de datos
db = pymysql.connect(
    host="localhost",
    user="root",  # Usuario de MySQL
    password="",  # Contraseña de MySQL
    database="agenda_db"
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    fullname = request.form['fullname'].strip()
    phone = request.form['phone'].strip()
    email = request.form['email'].strip()

    if fullname and phone and email:
        cursor = db.cursor()
        cursor.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)", (fullname, phone, email))
        db.commit()
        flash('Contact Added Successfully')
    else:
        flash('All fields are required!')

    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    cursor = db.cursor()
    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        phone = request.form['phone'].strip()
        email = request.form['email'].strip()

        cursor.execute("""
            UPDATE contacts
            SET fullname = %s, phone = %s, email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        db.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM contacts WHERE id = %s", (id,))
        contact = cursor.fetchone()
        return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete_contact(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
    db.commit()
    flash('Contact Deleted Successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
