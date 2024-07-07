from flask import Flask, render_template, url_for, request, redirect, url_for, flash, session,jsonify, make_response
from werkzeug.utils import secure_filename
import os
import json
import sys

# from cart import cart
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField, FileField
# from wtforms.validators import DataRequired
import sqlite3


print("Flask app is starting", flush=True)
sys.stdout.flush()


app = Flask(__name__,static_folder='static')
app.secret_key = 'your_secret_key_here' 
app.config['UPLOAD_DIRECTORY'] = 'static/media/'
# app.register_blueprint(shop_blueprint, url_prefix="")
# cart=cart()
print("Flask app is starting")
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
 

@app.route("/delete_product/<int:id>", methods=['GET','POST'], endpoint='delete_product')
def delete_product(id):
    product_id = int(id)
    with sqlite3.connect("db.db") as con:
      cur = con.cursor()
      cur.execute("DELETE FROM products WHERE id =?", (id,))
      con.commit()
      flash('Book Deleted','warning')
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

#//////CART CHECKOUT ORDERS////
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


@app.route('/checkout', methods=['GET', 'POST'])
# @loginrequired
def checkout():
    print(f"Request method: {request.method}")
    
    if request.method == 'POST':
        print("POST request received")
        print(f"Form data: {request.form}")
        
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        address = request.form["address"]
        phone = request.form["phone"]
        email = request.form["email"]
        
        with sqlite3.connect("db.db") as con:
                cur = con.cursor()
                cur.execute("SELECT id FROM user WHERE email=?", (email,))
                result = cur.fetchone()
                if result:
                    user_id = result[0]
                else:
                    flash("User not found. Please log in.", "error")
                    return redirect(url_for('login'))
                
                cart_items = request.cookies.get('cart_items', '[]')
                cart_items_list = json.loads(cart_items)
                
                print(f"Cart items: {cart_items_list}")
                
                total = 0
                for item in cart_items_list:
                    cur.execute("SELECT price FROM products WHERE id =?", (item['id'],))
                    product_price = cur.fetchone()[0]
                    total += product_price * item['quantity']
                
                print(f"Total order amount: {total}")
                
                cur.execute("INSERT INTO orders (user_id, total_amount) VALUES (?,?)",
                            (user_id, total))
                order_id = cur.lastrowid
                
                for item in cart_items_list:
                    cur.execute("INSERT INTO order_item (order_id, product_id, quantity) VALUES (?,?,?)",
                                (order_id, item['id'], item['quantity']))

                    con.commit() 
                    print(f"Order {order_id} inserted successfully")
        
        response = make_response(redirect(url_for('thankyou', order_id=order_id)))
        response.set_cookie('cart_items', '[]', expires=0)
        print("Redirecting to thank you page")
        return response
    
    else: 
        print("GET request received")
        cart_items = request.cookies.get('cart_items', '[]')
        cart_items_list = json.loads(cart_items)
        
        total = 0
        with sqlite3.connect("db.db") as con:
            cur = con.cursor()
            for item in cart_items_list:
                cur.execute("SELECT price FROM products WHERE id =?", (item['id'],))
                product_price = cur.fetchone()[0]
                total += product_price * item['quantity']
        
        print(f"Rendering checkout template with total: {total}")
        return render_template("checkout.html", total=total, cart_items=cart_items_list)
    
    

@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/thankyou/<int:order_id>')
def thankyou(order_id):
    customer = "Customer" 
    with sqlite3.connect("db.db") as con:
        cur = con.cursor()
        cur.execute("SELECT user_id FROM orders WHERE order_id = ?", (order_id,))
        result = cur.fetchone()
        
        if result:
            user_id = result[0]
            cur.execute("SELECT firstname FROM user WHERE id = ?", (user_id,))
            user_result = cur.fetchone()
            if user_result:
                customer = user_result[0]  
    
    return render_template('thankyou.html', order_id=order_id, customer=customer)


@app.route('/yourorders')
def yourorders():
    with sqlite3.connect("db.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        
       
        cur.execute("""
            SELECT o.order_id, o.user_id, o.total_amount, 
                   u.email, u.firstname, u.lastname
            FROM orders o
            JOIN user u ON o.user_id = u.id
        """)
        orders = [dict(order) for order in cur.fetchall()]
   
        for order in orders:
        
            cur.execute("""
                SELECT oi.order_item_id, oi.product_id, oi.quantity, 
                       p.image, p.name as product_name, p.price
                FROM order_item oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = ?
            """, (order['order_id'],))
            order['order_items'] = [dict(item) for item in cur.fetchall()]

    return render_template("yourorders.html", orders=orders)
@app.route('/orders')
def orders():
    with sqlite3.connect("db.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT  o.order_id, o.user_id, o.total_amount, 
                   u.email, u.firstname, u.lastname
            FROM orders o
            JOIN user u ON o.user_id = u.id
            ORDER BY o.order_id DESC
        """)
        orders = [dict(order) for order in cur.fetchall()]
   
        for order in orders:
            cur.execute("""
                SELECT oi.order_item_id, oi.product_id, oi.quantity, 
                       p.image, p.name as product_name, p.price
                FROM order_item oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = ?
            """, (order['order_id'],))
            order['order_items'] = [dict(item) for item in cur.fetchall()]

    return render_template("orders.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)
    