from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#mysql connection

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = 'data'

mysql = MySQL(app)

#Settings
app.secret_key = b'test_x44'

@app.route('/')
def index(): 
    create_table()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Contacts')
    data = cur.fetchall()
    print(data)
    return render_template("index.html", contacts = data)

def create_table():

    try:
        cur = mysql.connection.cursor()

    #Creating table as per requirement
        sql='''CREATE TABLE Contacts(
        Username varchar(255) NOT NULL,
        FavoriteColor varchar(255) NOT NULL,
        Pets varchar(255),
        PRIMARY KEY(`Username`)
        )'''
        cur.execute(sql)
    except Exception as e:
        if "already exists" in str(e):
            return "Contacts table is already created"
        else:
            mysql.connection.commit()

@app.route('/add_contact', methods=["POST"])
def add_contact():
    if request.method == 'POST':
        Username = request.form['Username']
        FavoriteColor = request.form['FavoriteColor']
        Pets = request.form['Pets']
        print(Username, FavoriteColor, Pets)
        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO Contacts (Username, FavoriteColor, Pets) VALUES (%s, %s, %s)', (Username, FavoriteColor, Pets))
            mysql.connection.commit()
            flash('Contact add successfully')
            return redirect(url_for('index'))
        except Exception as e:
            if "Duplicate entry" in str(e):
                flash("The Username already exists in the DB. Please try with another one")
            return redirect(url_for('index'))


@app.route('/edit/<Username>')
def get_contact(Username):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Contacts WHERE Username = "{}"'.format(Username))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<Username>', methods = ['POST'])
def update_contact(Username):
    if request.method == 'POST':
        username = (request.form['Username'])
        favoriteColor = (request.form['FavoriteColor'])
        pets = (request.form['Pets'])
        cur = mysql.connection.cursor()
        cur.execute('UPDATE Contacts SET Username = %s, FavoriteColor = %s, Pets = %s WHERE Username = %s', (username, favoriteColor, pets, Username))
        mysql.connection.commit()
        print(cur._last_executed)
        flash("Contact updated correctly")
        return redirect(url_for('index'))

@app.route('/delete/<string:Username>')
def delete_contact(Username):
# return id
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Contacts where Username = "{0}"'.format(Username))
    mysql.connection.commit()
    print("Test")
    flash("Contact removed successfully")
    return redirect(url_for('index'))
#    return "edit contact"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)
