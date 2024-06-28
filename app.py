from flask import Flask, render_template, url_for, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, FileField
# from wtforms.validators import DataRequired
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 
app.config['UPLOAD_DIRECTORY'] = 'static/products/'

@app.route("/")
def home():
    with sqlite3.connect("db.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT prod.*, categ.name AS category_name
            FROM products prod
            JOIN categories categ ON prod.category_id = categ.id
            ORDER BY id DESC
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
        
    # with sqlite3.connect("db.db") as con:
    #         cur = con.cursor()
    #         cur.execute("SELECT 1 FROM categories WHERE id =?", (category_id,))
    #         if not cur.fetchone():
    #             flash('Invalid category ID', 'error')
    #             return render_template("addProduct.html")
        
    with sqlite3.connect("db.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products (name, image, description, price, quantity, category_id) VALUES (?,?,?,?,?,?)", 
                        (name, image.filename, description, price, quantity, category_id))
            con.commit()
            flash('Product added', 'success')
            return redirect(url_for("home"))
    return render_template("addProduct.html")


@app.route("/edit_product/<int:id>", methods=['GET','POST'],endpoint='edit_product')
def edit_product(id):
    product_id = int(id)
    with sqlite3.connect("db.db") as con:
      cur = con.cursor()
      cur.execute("SELECT * FROM products WHERE id =?", (id,))
      product=cur.fetchone()
    if request.method == "POST":
        name = request.form["ProductName"]
        description = request.form["ProductDescription"]
        price = request.form["ProductPrice"]
        quantity = request.form["ProductQuantity"]
        category_id = request.form["ProductCategory"]
        image = request.files["ProductImage"]
        if image:
            image.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(image.filename)
            ))
            image_filename = image.filename
        else :
            image_filename = product[1]
        cur.execute("UPDATE products SET name =?, image=?, description=?, price=?, quantity=?, category_id=? WHERE id=?",
                        (name, image.filename, description, price, quantity, category_id, id))
                        #  (name, image.filename if image else product[1], description, price, quantity, category_id, id))
        con.commit()
        flash('Product updated', 'success')
        return redirect(url_for("home"))
    else:
            categories = cur.execute("SELECT * FROM categories").fetchall()
            return render_template("editProduct.html",product_id = product_id, product=product, categories=categories)
 

@app.route("/delete_product/<int:id>", methods=['GET'], endpoint='delete_product')
def delete_product(id):
    product_id = int(id)
    with sqlite3.connect("db.db") as con:
      cur = con.cursor()
      cur.execute("DELETE FROM products WHERE id =?", (id,))
      con.commit()
      return redirect(url_for("home"))
if __name__ == "__main__":
    app.run(debug=True)