
from app.models import *
from wtforms import StringField, DecimalField, TextAreaField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, email_validator
from flask_wtf import FlaskForm
from datetime import date

class PostForm(FlaskForm): 
    job = TextAreaField('Jobs: ', validators=[DataRequired(), Length(min = 1, max = 140)])
    description = TextAreaField('Description of Jobs: ', validators=[DataRequired()]) #, Length(min = 1, max = 140)])
    price = TextAreaField('Price: ', validators=[DataRequired()]) #, Length(min = 1, max = 140)])

    goal = TextAreaField('Goal: ', validators=[
        DataRequired(), Length(min = 1, max = 140)])
    categories = SelectField('Select Job Category:', choices=['Outdoor', 'Indoor', 
        'Spring', 'Summer', 'Fall', 'Winter', 'Lawn Care','Home Care', 'Moving', 'Other' ])
    location = DecimalField('Distance (In Miles) Available In: ', validators=[DataRequired()])
    submit = SubmitField('Post Your Job')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstName = StringField('First Name: ', validators=[DataRequired()])
    lastName = StringField('Last Name: ', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    birthday = DateField('Birthday', validators=[DataRequired()])
    streetAddress = StringField('Street Address', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    privpol = BooleanField('I agree to the terms of the', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Users.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
    def validate_birthday(self, birthday):
        delta = date.today() - birthday.data
        age=delta.days/365
        print(age)
        if age < 14 or age > 19:
            raise ValidationError('You are not in the correct age range to be a user on this website')
        
class SearchForm(FlaskForm):
    searchbar = StringField(('Search'),validators=[DataRequired()])
    find = SubmitField('Find')

class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    avail = StringField('Availability', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
    firstName = StringField('First Name', validators=[Length(min=0, max=20)])
    lastName = StringField('Last Name', validators=[Length(min=0, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    feedback = TextAreaField('Feedback', validators=[Length(min=0, max=140)])
    rating = SelectField('Rating:', coerce = int, choices=[1, 2, 3, 4, 5])
    submit = SubmitField('Submit Review')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete Post')

class EditPostForm(FlaskForm):
    job = TextAreaField('Jobs: ', validators=[
         Length(max = 140)])
    description = TextAreaField('Description of Jobs: ', validators=[
         Length(max = 140)]) #, Length(min = 1, max = 140)])
    #location = TextAreaField('Neighborhoods Available In: ', validators=[
    #    DataRequired(), Length(min = 1, max = 140)])
    contactInfo = TextAreaField('Contact Info: ', validators=[
         Length(max = 140)])
    goal = TextAreaField('Goal: ', validators=[
Length(max = 140)])
    categories = SelectField('Select Job Category:', choices=['Outside', 'Inside'])
    price = TextAreaField('Price: ', validators=[
         Length(max = 140)])
    location = DecimalField('Distance in miles available in: ', validators=[
         Length(max = 10)])

    submit = SubmitField('Post Your Job')

class RequestJobForm(FlaskForm):
  name = StringField("Your Name", validators=[DataRequired()])
  teenName = StringField("Teenager's Name", validators=[DataRequired()])
  email = StringField("Your Email", validators=[DataRequired(), Email()])
  date = StringField("Date of Job", validators=[DataRequired()])
  message = TextAreaField("Additional Info", validators=[Length(min = 0, max = 140)])
  submit = SubmitField("Send") 