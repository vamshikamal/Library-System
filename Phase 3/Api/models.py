from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


from Api import app

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(80), nullable=False, unique = True,)
    User_name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(80), nullable=False,  primary_key=True)
    Password = db.Column(db.String(80), nullable=False)
    borrowed = db.relationship('Book_Borrowed', backref = 'user', cascade = 'all, delete-orphan', lazy = 'dynamic')
    
    def __init__(self, id, User_name, Email, Password):
        self.id = id
        self.User_name = User_name
        self.Email = Email
        self.Password = Password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'User_name', 'Email', 'Password' ) 
    
        
        
class Book(db.Model):
    __tablename__ = 'book'
    Genre_name = db.Column(db.String(120), nullable=False)
    ISBN = db.Column(db.String(80), nullable=False, primary_key=True)
    Book_title = db.Column(db.String(120), nullable=False)
    Book_author = db.Column(db.String(120), nullable=False)
    Book_copies = db.Column(db.Integer(), nullable=False, default=1)
    borrowed = db.relationship('Book_Borrowed', backref = 'book', cascade = 'all, delete-orphan', lazy = 'dynamic')

    
    def __init__(self,  Genre_name, ISBN, Book_title, Book_author, Book_copies):
        self.Genre_name = Genre_name
        self.ISBN = ISBN
        self.Book_title = Book_title
        self.Book_author = Book_author
        self.Book_copies = Book_copies
        
class BookSchema(ma.Schema):
    class Meta:
        fields = ('ISBN','Book_title','Book_author', 'Genre_name', 'Book_copies' )
        
   
class Book_Borrowed(db.Model):
    __tablename__ = 'book_borrowed'
    id = db.Column(db.Integer(), primary_key=True)
    userID = db.Column(db.String(80), db.ForeignKey('user.Email'), nullable = False)
    bookID = db.Column(db.String(80), db.ForeignKey('book.ISBN'), nullable = False)
    Issue_date = db.Column(db.DateTime(), nullable=False)
         

class  Book_BorrowedSchema(ma.Schema):
    class Meta:
        fields = ('id','userID','bookID','Issue_date')
        
db.create_all()