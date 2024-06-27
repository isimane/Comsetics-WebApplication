from flask import Flask, render_template, url_for,request,redirect,url_for,flash,session
# from flask_sqlalchemy import SQLAlchemy'
import sqlite3

# import os

app=Flask(__name__)


if __name__ == "__main__":
    # db.create_all
    app.run(debug=True)