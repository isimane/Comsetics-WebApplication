from flask import Flask, render_template, url_for,request,redirect,url_for,flash,session
# from flask_sqlalchemy import SQLAlchemy'
import sqlite3

# import os

app=Flask(__name__)



@app.route("/")
def home():
  def home():
    with sqlite3.connect("db.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT p.*, c.name AS category_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
        """)
        data = cur.fetchall()
        return render_template("productstable.html", products=data)
   
if __name__ == "__main__":
    # db.create_all
    app.run(debug=True)


