from flask import render_template, flash, redirect, request, url_for, Flask
from app.forms import *
from app import db, app
from app.models import *
from flask_login import *
from flask_mail import *
from geopy.geocoders import Nominatim
import math
import geocoder
import requests 
from geopy.distance import distance
import os
from email.message import EmailMessage
import ssl
import smtplib

email_sender = 'KnockKnockEmails@gmail.com'
email_password = ' ----PASSWORD HIDDEN---- '
email_reciever = 'KnockKnockFreelancing@gmail.com'

geolocator = Nominatim(user_agent="my_user_agent")

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location():
    ip_address = get_ip()
    r = requests.get('http://api.ipstack.com/check?access_key= ----API KEY HIDDEN---- ')
    j = r.json()
    latitude = j['latitude']
    longitude = j['longitude']
    location_data = latitude, longitude
    return location_data

def calcLoc(origin, destination) :
    lat1, lon1 = origin
    lat2, lon2 = destination
    #radius = 6371 # km
    radius = 3959 # mi

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

#home page
@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def homePage():
    form = SearchForm()
    loca = get_location()
    if form.validate_on_submit():
        search_string = form.searchbar.data 
        searchResults = []
        searchResults = Posts.query.filter(Posts.job.contains(search_string))
        checker = []
        checker1 = [] 
        for item in searchResults:
            checker.append(item) 
        if not checker:
            flash('No results found!')
        else:
            for item in checker:
                range = item.location 
                dest = item.author.latitude, item.author.longitude
                print(loca)
                print(distance)
                d = calcLoc(loca,dest)
                if (d < range): 
                    checker1.append(item)
                    item.distance = round(d, 2)
                    db.session.commit()
                    print(checker1)
            return render_template('search.html', results = checker1)
    return render_template('home.html', title='search', form=form)

#view posts page
@app.route('/viewposts', methods = ['GET', 'POST'])
def viewPostPage():
    loca = get_location()
    allPosts = Posts.query.all()
    for item in allPosts:
        dest = item.author.latitude, item.author.longitude
        d = calcLoc(loca, dest)
        item.distance = round(d, 2)
        db.session.commit()
    return render_template('viewposts.html', posts=allPosts)

#about us page
@app.route('/aboutus', methods = ['GET', 'POST'])
def aboutUsPage():
    return render_template('aboutus.html')

#post creation page
@app.route('/post', methods = ['GET', 'POST'])
#@login_required
def postPage():
    if not current_user.is_authenticated:
        flash("You must be logged in to see this page.")
        return redirect('/home')
    form = PostForm()

    if form.validate_on_submit():
        print(4)

        post = Posts(author = current_user, 
                     job = form.job.data,
                     location = form.location.data,
                     description = form.description.data,
                     price = form.price.data,
                     goal = form.goal.data,
                     categories = form.categories.data)                                
        db.session.add(post)
        db.session.commit()
        flash('Posted {}'.format(form.job.data))
        return redirect('/home')

    return render_template('post.html', title='Posts', form=form)
    
#account creation page
@app.route('/signup', methods=['GET', 'POST'])
def signupPage():
    if current_user.is_authenticated:
        flash("You are already logged in! ")
        return redirect('/home')
    form = SignupForm()
    if form.validate_on_submit():
        address = (form.streetAddress.data + " " + form.city.data + " " + form.state.data + " " + form.zipcode.data)
        location = geolocator.geocode(address, timeout=None)
        newUser = Users(username = form.username.data,
                        firstName = form.firstName.data,
                        lastName = form.lastName.data,  
                        longitude = location.longitude,
                        latitude = location.latitude,
                        email = form.email.data,
                        totalrating = 0, numratings = 0)
        Users.setPassword(newUser, form.password.data)
        db.session.add(newUser)
        db.session.commit() 
        login_user(newUser)
        flash('Sign Up Complete'.format(
            form.username.data))
        return redirect('/home')
    return render_template('signup.html', title='Sign Up', form=form)

#login page
@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if current_user.is_authenticated:
        flash("You are already logged in! ")
        return redirect('/home')
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.checkPassword(form.password.data) :
            flash("Invalid Username or Password")
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        flash('Login successful for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/home')
    return render_template('login.html', title='Posts', form=form)

#logout page
@app.route('/logout')
def logout():
    logout_user()
    flash("Logout successful")
    return redirect('/home')

#privacy policy page
@app.route('/privacy')
def privacyPage():
    return render_template('privacy.html')

#profile page
@app.route('/profile/<username>')
def profilePage(username):
    theuser = Users.query.filter_by(username=username).first()
    try:
        theuser.posts
    except AttributeError:
        hasposts = False
        posts = 0
    else:
        posts = theuser.posts
        hasposts = True
        try: 
            theuser.review
            reviewsss = theuser.review
        except AttributeError: 
            reviewsss = None 
    if theuser.posts is  None:
        hasposts = False
        posts = 0
    reviewResults = Review.query.all()
    
    total = 0
    num = 0
    if(reviewResults):
        for review in reviewResults:
            if review.target == theuser:
                num = num + 1
                total = total + review.rating
    theuser.totalrating = total
    theuser.numratings = num
    try:
        av = total/num
    except ZeroDivisionError:
        average = 'No Rating'
    else:   
        average = round(av, 2)
    db.session.commit()

    return render_template('profile.html', user = theuser, average = average, posts = posts, haspost = hasposts, reviews = reviewsss)

#edit profile page
@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def editProfile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.aboutMe = form.about_me.data
        current_user.availability = form.avail.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profilePage', username=current_user.username))
    return render_template('editprofile.html', title='Edit Profile', form=form)

#edit a post page
@app.route('/editpost/<id>', methods=['GET', 'POST'])
@login_required
def editPost(id):
    post1 = Posts.query.get(id)
    if current_user != post1.author:
        flash("You do not have permission to edit other people's posts! ")
        return redirect('/home')
    form = EditPostForm()
    
    if form.is_submitted():
        print("Hello")
        if form.job.data == "":
            j = post1.job
        else:
            j = form.job.data
        if form.description.data == "":
            d = post1.description 
        else:
            d = form.description.data
        if form.goal.data == "":
            g = post1.goal
        else:
            g = form.goal.data
        if form.price.data == "":
            p = post1.price 
        else:
            p = form.price.data
        post = Posts(author = current_user, 
                     job = j,
                     description = d,
                     goal = g,
                     price = p,
                     categories = form.categories.data,
                     id = post1.id
                     )                                
        db.session.add(post)
        db.session.delete(post1)
        db.session.commit()
        flash('Post Edited {}'.format(form.job.data))
        return redirect(url_for('profilePage', username=post.author.username))
    return render_template('editpost.html', title='Edit Post', form=form, post = post1)

#delete a post page
@app.route('/deletepost/<id>', methods=['GET', 'POST','DELETE'])
@login_required
def deletePost(id):
    post1 = Posts.query.get(id)
    if current_user != post1.author:
        flash("You do not have permission to delete other people's posts! ")
        return redirect('/home')
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(post1)
        db.session.commit()
        flash("Your post was successfully deleted")
        return redirect(url_for('profilePage', username=post1.author.username))
    return render_template('deletepost.html', title='Edit Post', form=form, post = post1)

#review page
@app.route('/<username>/review', methods=['GET', 'POST','DELETE'])
def review(username):
    targetuser = Users.query.filter_by(username=username).first()

    if current_user == targetuser:
        flash("You do not have permission to leave a review! ")
        return redirect('/home')
    form = ReviewForm()

    if form.validate_on_submit():
        targetuser.totalrating = targetuser.totalrating + form.rating.data 
        targetuser.numratings = targetuser.numratings + 1 
        review = Review(target = targetuser,
                    firstName = form.firstName.data, 
                     lastName = form.lastName.data,
                     email = form.email.data,
                     feedback = form.feedback.data,
                     rating = form.rating.data)                                
        db.session.add(review)
        db.session.commit()
        flash("Your review was successfully posted")
        return redirect(url_for('profilePage', username=targetuser.username, reviews = targetuser.review))
    return render_template('review.html', title='Edit Post', form=form)

#request a job page
@app.route('/requestjob', methods = ['GET','POST'])
def requestJob():
  form = RequestJobForm()
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('request.html', form=form)
    else:
      subject = "Request From: " + form.name.data
      body = "Name: " + form.name.data + "\nEmail: " + form.email.data + "\n\nTeenager Wanted: " + form.teenName.data + "\nDate: " + form.date.data + "\n\nInfo:\n" + form.message.data
      email = EmailMessage()
      email['From'] = email_sender
      email['To'] = email_reciever
      email['Subject'] = subject
      email.set_content(body)
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
          smtp.login(email_sender, email_password)
          smtp.sendmail(email_sender, email_reciever, email.as_string())
      flash('Request Sent!')
      return redirect('/home')
  elif request.method == 'GET':
    return render_template('request.html', form=form)
  
#directions page
@app.route('/directions')
def directionsPage():
    return render_template('directions.html')

#contact us page
@app.route('/contactUs')
def contactUsPage(): 
    return render_template('contactus.html')
  
