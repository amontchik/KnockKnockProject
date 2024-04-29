from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

@login.user_loader
def load_user(id):
    return Users.query.get(int(id))

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    job = db.Column(db.String, index = True)
    description = db.Column(db.String, index = True)
    price = db.Column(db.String, index = True)
    goal = db.Column(db.String, index = True)
    categories = db.Column(db.String, index = True)
    distance = db.Column(db.Float,index = True)
    location = db.Column(db.Float, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.description) 

class Users(UserMixin, db.Model): #added UserMixin
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, index = True, unique = True)
    firstName = db.Column(db.String, index = True)
    lastName = db.Column(db.String, index = True)
    email = db.Column(db.String, index = True, unique = True)
    password_hash = db.Column(db.String)
    longitude = db.Column(db.Float, index = True)
    latitude = db.Column(db.Float, index = True)
    posts = db.relationship('Posts', backref = 'author', lazy = 'dynamic')
    review = db.relationship('Review', backref = 'target', lazy = 'dynamic')
    numratings = db.Column(db.Integer, index = True)
    totalrating = db.Column(db.Integer, index = True)
    aboutMe = db.Column(db.String)
    availability = db.Column(db.String(140))
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    feedback = db.Column(db.String(200), index = True)
    firstName = db.Column(db.String, index = True)
    lastName = db.Column(db.String, index = True)
    email = db.Column(db.String, index = True)
    rating = db.Column(db.Integer, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Test {}>'.format(self.rating)
    
class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    test = db.Column(db.String, index = True)

    def __repr__(self):
        return '<Test {}>'.format(self.test)