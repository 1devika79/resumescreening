from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError , NumberRange
from flaskblog.models import Company, Employee,User
from wtforms import widgets, SelectMultipleField

class RegistrationFormE(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Employee.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginFormE(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Company.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Company.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountFormE(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            print(current_user)
            user = Employee.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Employee.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Company.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Company.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(FlaskForm):
    Lang = ['Hindi,English,Bengali,Marathi,Telugu,Tamil,Gujarati,Kannada,Odia, Malayalam']
    Programming=['C/C++,C#,Java,JavaScript,Perl,PHP,Python,Swift,Go,SQL,R,Ruby']
    softdev=['Coding,Debugging,Implementation,Testing,Design,Configuration,Applications,IOS/Android,Languages,Security,Algorithms,Modeling,Documentation']
    Design=['Adobe creative apps,HTML,Interactive media,Wireframing,UX research,Prototyping,Color theory,Responsive design,Photoshop,Sketch,User modeling']
    Marketing=['Search Engine Optimization (SEO),Digital media,Social media platforms,Automated marketing software,Content Management Systems (CMS),Copywriting,Content creation,Google Analytics,Marketing analytics tools']
    langfiles = Lang[0].split(',')
    profiles=Programming[0].split(',')
    softfiles=softdev[0].split(',')
    desfiles=Design[0].split(',')
    marketfiles=Marketing[0].split(',')
    # create a list of value/description tuples
    lan = [(x, x) for x in langfiles]
    pro=[(x, x) for x in profiles]
    soft=[(x, x) for x in softfiles]
    des=[(x, x) for x in desfiles]
    market=[(x, x) for x in marketfiles]
    examplelan = MultiCheckboxField('Label', choices=lan)
    examplepro = MultiCheckboxField('Label', choices=pro)
    examplesoft = MultiCheckboxField('Label', choices=soft)
    exampledes = MultiCheckboxField('Label', choices=des)
    examplemarket = MultiCheckboxField('Label', choices=market)
    name= StringField('Name',
                           validators=[DataRequired()])
    email= StringField('Email',
                        validators=[DataRequired(), Email()])
    phn_no=StringField('phn_no',validators=[DataRequired()])
    age=StringField('age',validators=[DataRequired()])
    spec=TextAreaField('Achievements',validators=[DataRequired()])
    exp=TextAreaField('Communities',validators=[DataRequired()])
    gitid=StringField('Voluntary',validators=[DataRequired()])
    linkedin=StringField('Qualifications',validators=[DataRequired()])
    address=TextAreaField('Interests',validators=[DataRequired()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    Programming=['C/C++,C#,Java,JavaScript,Perl,PHP,Python,Swift,Go,SQL,R,Ruby']
    softdev=['Coding,Debugging,Implementation,Testing,Design,Configuration,Applications,IOS/Android,Languages,Security,Algorithms,Modeling,Documentation']
    Design=['Adobe creative apps,HTML,Interactive media,Wireframing,UX research,Prototyping,Color theory,Responsive design,Photoshop,Sketch,User modeling']
    Marketing=['Search Engine Optimization (SEO),Digital media,Social media platforms,Automated marketing software,Content Management Systems (CMS),Copywriting,Content creation,Google Analytics,Marketing analytics tools']
    
    profiles=Programming[0].split(',')
    softfiles=softdev[0].split(',')
    desfiles=Design[0].split(',')
    marketfiles=Marketing[0].split(',')
    # create a list of value/description tuples
    
    pro=[(x, x) for x in profiles]
    soft=[(x, x) for x in softfiles]
    des=[(x, x) for x in desfiles]
    market=[(x, x) for x in marketfiles]
    
    minpro = MultiCheckboxField('Label', choices=pro)
    minsoft = MultiCheckboxField('Label', choices=soft)
    mindes = MultiCheckboxField('Label', choices=des)
    minmarket = MultiCheckboxField('Label', choices=market)

    maxpro = MultiCheckboxField('Label', choices=pro)
    maxsoft = MultiCheckboxField('Label', choices=soft)
    maxdes = MultiCheckboxField('Label', choices=des)
    maxmarket = MultiCheckboxField('Label', choices=market)

    title = StringField('Title', validators=[DataRequired()])
    Category = StringField('Category', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    salary = StringField('salary', validators=[DataRequired()])

    submit = SubmitField('Post')

