from flask import Flask, abort, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_here"

class User(UserMixin):
    def __init__(self, id, firstname, lastname, email, password, role):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.role = role

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect("db.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user_data = cur.fetchone()
        if user_data:
            return User(*user_data)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            flash("Please provide both email and password", "danger")
            return redirect(url_for("login"))
        with sqlite3.connect("db.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE email=?", (email,))
            user_data = cur.fetchone()
            if user_data:
                user = User(*user_data)
                if user.password == password:
                    login_user(user)
                    flash("Logged in successfully!", "success")
                    if user.role == "admin":
                        return redirect(url_for("accountadmin"))
                    elif user.role == "client":
                        return redirect(url_for("accountclient"))
                else:
                    flash("Invalid email or password", "danger")
                    return render_template("login.html")
            else:
                flash("Invalid email or password", "danger")
                return render_template("login.html")
    else:
        return render_template("login.html", user=current_user)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        if firstname and lastname and email and password:
            with sqlite3.connect("db.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE email=?", (email,))
                if cur.fetchone():
                    flash("Email already exists.", "danger")
                else:
                    cur.execute("INSERT INTO users (firstname, lastname, email, password, role) VALUES (?, ?, ?, ?, ?)",
                                (firstname, lastname, email, password, "client"))
                    con.commit()
                    flash("Account created successfully!", "success")
                    return redirect(url_for("accountclient"))
        else:
            flash("Please fill in all the fields", "danger")
    return render_template("signup.html")

@app.route('/update_data/<string:id>', methods=['POST', 'GET'])
@login_required
def update_data(id):
    with sqlite3.connect("db.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id=?", (id,))
        user_data = cur.fetchone()
        if user_data:
            user = User(*user_data)
            if user.role == 'client':
                if request.method == 'POST':
                    firstname = request.form['firstname']
                    lastname = request.form['lastname']
                    email = request.form['email']

                    if not firstname or not lastname or not email:
                        flash('Please fill in all fields')
                        return render_template("accountclient.html", user=current_user)
                    cur.execute("UPDATE users SET firstname=?, lastname=?, email=? WHERE id=?",
                                (firstname, lastname, email, id))
                    con.commit()
                    flash('User Updated', 'success')
                    return redirect(url_for("accountclient"))
                return render_template("accountclient.html", user=current_user)
            elif user.role == 'admin':
                if request.method == 'POST':
                    firstname = request.form['firstname']
                    lastname = request.form['lastname']
                    email = request.form['email']

                    if not firstname or not lastname or not email:
                        flash('Please fill in all fields')
                        return render_template("accountadmin.html", user=current_user)
                    cur.execute("UPDATE users SET firstname=?, lastname=?, email=? WHERE id=?",
                                (firstname, lastname, email, id))
                    con.commit()
                    flash('User Updated', 'success')
                    return redirect(url_for("accountadmin"))
                return render_template("accountadmin.html", user=current_user)
        else:
            flash('User not found', 'danger')
            return redirect(url_for("login"))  # or any other route you want to redirect to
        
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/account')
@login_required
def account():
    return render_template('accountclient.html', user=current_user)

@app.route('/accountadmin')
@login_required
def accountadmin():
    return render_template("accountadmin.html", user=current_user)

@app.route('/accountclient')
@login_required
def accountclient():
    return render_template("accountclient.html", user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)