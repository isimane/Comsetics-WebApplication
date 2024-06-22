from flask import Flask, render_template, url_for
# from flask_sqlalchemy import SQLAlchemy'
import sqlite3

# import os

app=Flask(__name__,template_folder='templates')
app.secret_key = "super secret key"


@app.route("/")
def home():
  
    return render_template("file.html")

@app.route("/PRODUCTS")
def about():
    return "hellooooo simaneee"

if __name__ == "__main__":
    # db.create_all
    app.run(debug=True)


