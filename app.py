from flask import Flask, render_template, url_for,request,redirect,url_for,flash,session
import os
# from flask_sqlalchemy import SQLAlchemy'
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired
import sqlite3


app=Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey'
app.config['UPLOAD_FOLDER'] = 'static/products'


@app.route("/productTable")
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
    



class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    image = FileField('Product Image', validators=[DataRequired()])
    description = StringField('Product Description', validators=[DataRequired()])
    price = StringField('Product Price', validators=[DataRequired()])
    quantity = StringField('Product Quantity', validators=[DataRequired()])
    
    submit = SubmitField('Submit')
    
@app.route("/add_product", methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        quantity = form.quantity.data
        image = form.image.data
        
        # Create a directory to store the uploaded images if it doesn't exist
        upload_dir = os.path.join(app.root_path, 'static/products')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Save the uploaded image
        if image:
            image_filename = image.filename
            image_path = os.path.join(upload_dir, image_filename)
            image.save(image_path)
        else:
            image_filename = None
        
        with sqlite3.connect("db.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products(name, image, description, price, quantity) VALUES (?,?,?,?,?)",
                        (name, image_filename, description, price, quantity))
            con.commit()
            flash('Product added successfully', 'success')
        return redirect(url_for("home"))
    return render_template("addProduct.html", form=form)

if __name__ == "__main__":
    # db.create_all
    app.run(debug=True)



