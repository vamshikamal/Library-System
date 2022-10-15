from flask import request, jsonify, session
from flask import redirect, render_template,  url_for
from datetime import datetime
from Api import app

app.secret_key = 'Secret Key'
from .models import db, User,  Book, Book_Borrowed,BookSchema, Book_BorrowedSchema

bookItemSchema = BookSchema()
bookListSchema  = BookSchema(many=True)

book_borrowed_ItemSchema = Book_BorrowedSchema()
book_borrowed_ListSchema  = Book_BorrowedSchema(many=True)

@app.route("/signup-ajax", methods=['POST'])
def Registration():
    print(request.json)
    id = request.json['id']
    uname = request.json['uname']
    email = request.json['email']
    password = request.json['password']
     
    if User.query.filter_by(id=id).first() is not None:
        return jsonify({'error': "ID is already taken"})
    user = User(id = id, User_name = uname, Email = email, Password=password)
    db.session.add(user)
    db.session.commit()
    
    print("Added to table of user in Database")
    return "success"

@app.route("/login-ajax", methods=['POST'])
def user_login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(Email=email).first()
    if user is not None:
        if user.Password == password:
            session['Logged_in'] = True
            session['username'] = user.User_name
            session['id'] = user.Email
            print(session)
            if user.Email == 'admin123@gmail.com':
                return 'admin'
            else:
                return 'user'
    else:
        print('User did not found')
        return 'error'  

@app.route("/userDetails", methods=['GET', 'POST'])
def userDetails():
    session_ID = session['id']
    user = User.query.filter_by(Email=session_ID).first()
    print(user.Email)
    dict = {'userid': user.id, 'username':user.User_name, 'useremail':user.Email}
    print(dict)
    return jsonify(dict)
   
 
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('Logged_in', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route("/addBook-ajax", methods=['POST'])
def addBooks():
    if "Logged_in" in session:
        print(request.json)
        genre = request.json['genre']
        isbn = request.json['isbn']
        title = request.json['title']
        author = request.json['author']
        copies = request.json['copies']
        
        Data = Book.query.filter_by(ISBN=isbn).first()
        if Data is not None:
            if genre == Data.Genre_name and title == Data.Book_title and author == Data.Book_author:
                prev_copies = Data.Book_copies
                Data.Book_copies = int(prev_copies) + int(copies)
                db.session.commit()
                print("Updated to table of Book")
                return "success"
            else:
                return jsonify({'error': "ISBN is already taken"})
        book = Book(Genre_name = genre, ISBN = isbn, Book_title = title, Book_author = author, Book_copies = copies)
        db.session.add(book)
        db.session.commit() 
        
        print("Added to table of Book")
        return "success"
    else:
        return 'logged_out'


@app.route("/deleteBook-ajax", methods=['GET', 'POST'])
def deleteBook():
    if "Logged_in" in session:
        isbn = request.json['isbn']
        book = Book.query.filter_by(ISBN=isbn).first()
        if book is not None:
            db.session.delete(book)
            db.session.commit()
            return 'success'
        else:
            return "Book not Found"
    else:
        return "logged_out"
    

@app.route("/", methods=["GET"])    
def home():
    return render_template('index.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/userView", methods=['GET', 'POST'])
def userView():
    return render_template('userView.html')


@app.route("/AdminProfile", methods=['GET', 'POST'])
def adminprofile():
    return render_template('AdminProfile.html') 

@app.route("/Admin", methods=['GET', 'POST'])
def adminView():
    return render_template('Admin.html')

@app.route("/addBook", methods=['GET', 'POST'])
def addbook():
    return render_template('addBook.html')      

@app.route("/deleteBook", methods=['GET', 'POST'])
def deletebook():
    return render_template('deleteBook.html') 

    
        
