from flask import Flask, render_template, url_for, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, FileField
# from wtforms.validators import DataRequired
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 
app.config['UPLOAD_DIRECTORY'] = 'media/'

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
        name = request.form["ProductName"]
        description = request.form["ProductDescription"]
        price = request.form["ProductPrice"]
        quantity = request.form["ProductQuantity"]
        category_id = request.form["ProductCategory"]
        image = request.files["ProductImage"]
    else:
         with sqlite3.connect("db.db") as con:
            cur = con.cursor()
            cur.execute("""SELECT categ.*
               FROM categories categ
               ORDER BY categ.name""")
            categories = cur.fetchall()
            print(categories)
            return render_template("addProduct.html", categories=categories)
    if image:
            image.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(image.filename)
            ))
        
    with sqlite3.connect("db.db") as con:
            cur = con.cursor()
            cur.execute("SELECT 1 FROM categories WHERE id = ?", (category_id,))
            if not cur.fetchone():
                flash('Invalid category ID', 'error')
                return render_template("addProduct.html")
        
    with sqlite3.connect("db.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products (name, image, description, price, quantity, category_id) VALUES (?,?,?,?,?,?)", 
                        (name, image.filename, description, price, quantity, category_id))
            con.commit()
            flash('Product added', 'success')
            return redirect(url_for("home"))
    return render_template("addProduct.html")


@app.route("/shop")
def shop():
    category = request.args.get("category")
    with sqlite3.connect("db.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # cur.execute("""
        #     SELECT prod.*, categ.name AS category_name
        #     FROM products prod
        #     JOIN categories categ ON prod.category_id = categ.id
        #     ORDER BY RANDOM()
        # """)
        sql = """
            SELECT prod.*, categ.name AS category_name
            FROM products prod
            JOIN categories categ ON prod.category_id = categ.id
        """
        if category:
            sql += " WHERE categ.id = " + category
            
        sql += " ORDER BY RANDOM()"
            
        cur.execute(sql)
        
        data = cur.fetchall()
        if category:
            # get category name from db using the id
            category = 'test cat'
        return render_template("shop.html", products=data, category=category)


if __name__ == "__main__":
    app.run(debug=True)