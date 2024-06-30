from flask import Flask, render_template, url_for,request,redirect,url_for,flash,session
# from flask_sqlalchemy import SQLAlchemy'
import sqlite3

# import os
# shop_blueprint = Blueprint("shop",__name__,static_folder="static", template_folder="templates" )
app=Flask(__name__)

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
         # get category name from db using the id
           categoryname = "SELECT name FROM categories WHERE id = ?"
           cur.execute(categoryname, (int(category),))
           category_name = cur.fetchone()[0]
           category = category_name

        return render_template("shop.html", products=data, category=category)
    
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
         # get category name from db using the id
           categoryname = "SELECT name FROM categories WHERE id = ?"
           cur.execute(categoryname, (int(category),))
           category_name = cur.fetchone()[0     ]
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
    