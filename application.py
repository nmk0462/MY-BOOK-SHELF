import os
import requests
from flask import Flask,render_template,request,jsonify, make_response,session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
app=Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
@app.route("/")
def index():
 
    return render_template("layout.html")
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    name=request.form.get("uname")
    pass1=request.form.get("pass")
    

    pp=db.execute("SELECT username,password FROM users WHERE username=:n",{"n":name}).fetchone()
    if pp==None:
        db.execute("INSERT INTO users (username,password) VALUES (:username, :password)",
                  {"username":name, "password": pass1})
        db.commit()
    else:
        rr="USERNAME EXISTS CHOOSE OTHER NAME ): OR SIGN IN IF YOU HAVE ALREADY REGISTERED"
        return render_template("layout.html",rr=rr)
      
    
    
    return render_template("login.html")
@app.route("/aaa",methods=["POST","GET"])
def aaa():
    name1=request.form.get("username")
    passw=request.form.get("password")
      
  
    session['username'] = request.form['username']
    
    rr=db.execute("SELECT username,password FROM users WHERE username=:n and password=:p",{"n":name1,"p":passw}).fetchone()
    if rr==None:
        return render_template("error.html")
    else:
       
        us=request.cookies.get('username')
        return render_template("store.html",user=name1)

@app.route("/sto",methods=["POST","GET"])
def sto():
    us=session['username'] 
    srh=request.form.get("books1")
    li = "%" +srh+ "%"
    bk=db.execute("SELECT * FROM books WHERE isbn ILIKE :i OR title ILIKE :i OR author ILIKE :i",{"i":li}).fetchall()
    rv=db.execute("SELECT * FROM books WHERE isbn ILIKE :i OR title ILIKE :i OR author ILIKE :i",{"i":li}).rowcount
    if rv==0:
        hj="NO RESULT FOUND"
        return render_template("store.html",bk=bk,user=us,hj=hj)
    else:
        return render_template("store.html",bk=bk,user=us)
@app.route("/go/<isbn>",methods=["POST","GET"])
def go(isbn):
    us=session['username']
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "nJvnFqsiGB6NdayIBoAznA", "isbns": isbn })
    op=(res.json())
    er=op['books']
    reviews_count = er[0]["work_ratings_count"]
    average_rating = er[0]["average_rating"]
    
    b=db.execute("SELECT * FROM books WHERE isbn=:i",{"i":isbn}).fetchone()
    bh=db.execute("SELECT userid,review,rating FROM reviews WHERE isbn=:i",{"i":isbn}).fetchall()
    return render_template("final.html",isbn=isbn,rc=reviews_count,ar=average_rating,bh=bh,b=b)
 
@app.route("/oo/<isbn>",methods=["POST","GET"])
def oo(isbn):
   
    ww=request.form.get("revie")
    r=request.form.get("ratin")
    us=session['username']
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "nJvnFqsiGB6NdayIBoAznA", "isbns": isbn })
    op=(res.json())
    er=op['books']
    reviews_count = er[0]["work_ratings_count"]
    average_rating = er[0]["average_rating"]
    b=db.execute("SELECT * FROM books WHERE isbn=:i",{"i":isbn}).fetchone()

    jj=db.execute("SELECT * FROM reviews WHERE userid=:u1 AND isbn=:i",{"i":isbn,"u1":us}).rowcount
    ip=jj
    if ip==0:
        db.execute("INSERT INTO reviews (isbn,review,rating,userid) VALUES (:isbn,:review,:rating,:userid)",
                  {"isbn":isbn, "review": ww,"rating":r,"userid":us})
        db.commit()
        bh=db.execute("SELECT userid,review,rating FROM reviews WHERE isbn=:i",{"i":isbn}).fetchall()
        return render_template("final.html",rev=ww,rat=r,isbn=isbn,rc=reviews_count,ar=average_rating,b=b,bh=bh,)
    if ip!=0:
        ip="YOU HAVE ALREADY SUBMITTED YOUR REVIEW FOR THIS BOOK"
        bh=db.execute("SELECT userid,review,rating FROM reviews WHERE isbn=:i",{"i":isbn}).fetchall()
        return render_template("final.html",isbn=isbn,rc=reviews_count,ar=average_rating,b=b,bh=bh,ip=ip)
@app.route("/logout")
def logout():
    res=make_response(render_template("logout.html"))
    session.pop('username', None)
    return res 

@app.route("/api/<isbn>",methods=['GET'])
def api(isbn):
    books=db.execute("SELECT * FROM books WHERE isbn= :i",{"i":isbn}).fetchone()
    if books :
    
        r= requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "nJvnFqsiGB6NdayIBoAznA", "isbns": isbn})
        if r:
            print(r.json())
            goodinfo = r.json()
            scratch = goodinfo["books"]
            reviews_count = scratch[0]["work_ratings_count"]
            average_rating = scratch[0]["average_rating"]
            bjson = [
                {
                    "title": books['title'],
                    "author": books['author'],
                    "year": books['year'],
                    "isbn": books['isbn'],
                    "review_count": reviews_count,
                    "average_score": average_rating
                }
             ]
            return jsonify(bjson)
        else :
            return render_template("error.html")
    else :
         return render_template("error.html")
       
 
   
