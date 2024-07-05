from flask import Flask, render_template, url_for, request, redirect, url_for, flash, session,jsonify, make_response
from werkzeug.utils import secure_filename
import os
import json
# from cart import cart
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, FileField
# from wtforms.validators import DataRequired
import sqlite3

app = Flask(__name__,static_folder='static')
app.secret_key = 'your_secret_key_here' 
app.config['UPLOAD_DIRECTORY'] = 'static/media/'
# app.register_blueprint(shop_blueprint, url_prefix="")
# cart=cart()
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
        products = [dict(row) for row in data]
        featured = products[12] if products else None
        three = products[:3] if products else []
        two = products[3:5] if len(products) >= 5 else products[3:] if products else []
        
    return render_template("index.html", featured=featured, threeprod=three, twoprod=two)


@app.route("/about_us")
def about():
    return render_template('about.html')

@app.route("/contact_us")
def contact():
    return render_template('contactus.html')



@app.route("/shop")
def shop():   
    category = request.args.get("category")
    with sqlite3.connect("db.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        sql = """
            SELECT prod.*, categ.name AS category_name
            FROM products prod
            JOIN categories categ ON prod.category_id = categ.id
        """
        if category:
            sql += " WHERE categ.id = ?"
            
        sql += " ORDER BY RANDOM()"
        
        if category:
            cur.execute(sql, (int(category),))
        else:
            cur.execute(sql)
            
        data = cur.fetchall()
            
        if category:
           categoryname = "SELECT name FROM categories WHERE id = ?"
           cur.execute(categoryname, (int(category),))
           category_name = cur.fetchone()[0]
           category = category_name

        return render_template("shop.html", products=data, category=category)
    
    
@app.route('/product/<int:id>')
def product(id):
    with sqlite3.connect("db.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM products WHERE id =?", (id,))
        product = cur.fetchone()
        return render_template("product.html", product=product)


#CRUD:
@app.route("/product_table")
def productTable():
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
        if image:
                image.save(os.path.join(
                    app.config['UPLOAD_DIRECTORY'],
                    secure_filename(image.filename)
                ))
            
        with sqlite3.connect("db.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO products (name, image, description, price, quantity, category_id) VALUES (?,?,?,?,?,?)", 
                            (name, image.filename, description, price, quantity, category_id))
                con.commit()
                flash('Your product was added succesfully', 'success')
                
        return redirect(url_for("productTable"))
    else:
        with sqlite3.connect("db.db") as con:
            cur = con.cursor()
            cur.execute("""SELECT categ.*
               FROM categories categ
               ORDER BY categ.name""")
            categories = cur.fetchall()
            print(categories)
            return render_template("addProduct.html", categories=categories)


@app.route("/edit_product/<int:id>", methods=['GET','POST'], endpoint='edit_product')
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
            
        image = image.filename if image else product[1]
        cur.execute("UPDATE products SET name =?, image=?, description=?, price=?, quantity=?, category_id=? WHERE id=?",
                        # (name, image.filename, description, price, quantity, category_id, id))
                         (name, image, description, price, quantity, category_id, id))
        con.commit()
        flash('Your product was edited succesfully', 'success')
        return redirect(url_for("productTable"))
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
      return redirect(url_for("productTable"))
  




@app.route("/add_to_cart", methods=['POST'])
def add_cart():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400
    
    cart_items = request.cookies.get('cart_items')
    if not cart_items:
        cart_items = '[]'
        
    cart_items_list = json.loads(cart_items)
    product_id = data['id']
    # check if cart contains element eith that id
    alreadyExists = False
    for item in cart_items_list:
        if item['id'] == product_id:
            item['quantity'] += data['quantity']
            alreadyExists = True
        
    if not alreadyExists:
        cart_items_list.append(data)

    response = jsonify({"success": True})
    response.set_cookie('cart_items', json.dumps(cart_items_list))  # Update cart_items cookie
    return response
    
    # cart_items.append({
    #     'id': data['id'],
    #     'quantity': data['quantity'],
    # })
    
    return jsonify({"success": False, "message": "Item added to cart"}), 200
@app.route('/cart', methods=['GET'])
def cart():
    cart_items = request.cookies.get('cart_items', '[]')
    cart_items_list = json.loads(cart_items)
    
    cart_details = []
    total = 0
    
    with sqlite3.connect("db.db") as con:
        cur = con.cursor()
        for item in cart_items_list:
            cur.execute("SELECT name, price, image FROM products WHERE id = ?", (item['id'],))
            product = cur.fetchone()
            if product:
                name, price, image = product
                subtotal = price * item['quantity']
                cart_details.append({
                    'id': item['id'],
                    'name': name,
                    'price': price,
                    'image': url_for('static', filename=f'media/{image}'),
                    'quantity': item['quantity'],
                    'subtotal': subtotal
                })
                total += subtotal
    
    return render_template("cart.html", cart_items=cart_details, total=total)

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")
if __name__ == "__main__":
    app.run(debug=True)