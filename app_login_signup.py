from flask import Flask, abort, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default="client")




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
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
        return render_template("login.html", user=current_user)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        if firstname and lastname and email and password:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already exists.", "danger")
            else:
                user = User(firstname=firstname, lastname=lastname, email=email, password=password, role="client")
                db.session.add(user)
                db.session.commit()
                flash("Account created successfully!", "success")
                return redirect(url_for("accountclient"))
        else:
            flash("Please fill in all the fields", "danger")
    return render_template("signup.html")








@app.route('/update_data/<string:id>', methods=['POST', 'GET'])
@login_required
def update_data(id):
    user = User.query.get(id)
    if user:
        if user.role == 'client':
            if request.method == 'POST':
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                email = request.form['email']

                if not firstname or not lastname or not email:
                    flash('Please fill in all fields')
                    return render_template("accountclient.html", user=current_user)
                user.firstname = firstname
                user.lastname = lastname
                user.email = email
                db.session.commit()
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
                user.firstname = firstname
                user.lastname = lastname
                user.email = email
                db.session.commit()
                flash('User Updated', 'success')
                return redirect(url_for("accountadmin"))
            return render_template("accountadmin.html", user=current_user)
    else:
        flash('User not found', 'danger')
        return redirect(url_for("login"))  # or any other route you want to redirect to




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
