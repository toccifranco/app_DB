from flask import Flask, render_template, request, url_for, redirect, flash
from flask.wrappers import Request  # uso render template para renderzar el html
from flask_mysqldb import MySQL


app = Flask(__name__)

# mysql conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)


#  setting
app.secret_key = 'mysecretkey'

# creando todas las rutas


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')  # selecciono la tabla
    data = cur.fetchall()  # obtengo sus datos
    print(data)
    return render_template('index.html', contacts=data)  # pongo el formulario


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        # usa la funcion cursor de mysql para almacenar los datos
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO contacts (fullname, phone, email) values(%s, %s, %s)', (fullname, phone, email))  # carga el datoen la db
        mysql.connection.commit()
        flash('contacto agregado satisfactoriamente')
        return redirect(url_for('index'))  # redireccionamos al index


@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
      UPDATE contacts
      SET fullname = %s,
          email = %s,
          phone = %s
      WHERE id = %s
    """, (fullname, email, phone, id))
    mysql.connection.commit()
    flash('contacto actualizado de manera correcta')
    return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_cotact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'. format(id))
    mysql.connection.commit()
    flash('contacto removido de manera satisfactoria')
    return redirect(url_for('index'))


# si el nombre es app.py(osea __main__) inicializa el sv
if __name__ == "__main__":
    app.run(port=3000, debug=True)
