from flask import Flask, render_template, url_for,request,redirect,url_for,flash,session
# from flask_sqlalchemy import SQLAlchemy'
import sqlite3

# import os

app=Flask(__name__)



@app.route("/")

def home():
    with sqlite3.connect("db.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT prod.*, categ.name AS category_name
            FROM products prod
            JOIN categories categ ON prod.category_id = categ.id
            ORDER BY RANDOM()
        """)
       
        data = cur.fetchall()
        return render_template("productstable.html", products=data)
    

@app.route("/add_product", methods=["GET", "POST"]) 
def add_product():
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        image = request.form["image"]
        quantity = request.form["quantity"]
        with sqlite3.connect("db.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products (name, description, price, image, quantity) VALUES (?, ?, ?, ?, ?)",(name, description, price, image,quantity))
            con.commit()
            flash('Product added','success')
            return redirect(url_for("home"))
    return render_template("addProduct.html")



if __name__ == "__main__":
    # db.create_all
    app.run(debug=True)


