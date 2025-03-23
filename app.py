from flask import Flask, render_template, url_for, request, redirect
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt



app = Flask(__name__)
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app) # Initializes database (app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(20), nullable=False, unique=True)
    password= db.Column(db.String(80), nullable=False)
    tasks=db.relationship('Todo', backref='author', lazy=True) # This will put unique input per account

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),
                                       Length(min=4, max=30)],
                                       render_kw={'placeholder': 'Username'})
    password = PasswordField(validators=[InputRequired(),
                                       Length(min=4, max=30)],
                                       render_kw={'placeholder': 'Password'})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username = username.data).first()
        
        if existing_user_username:
            raise ValidationError('That username alreadyt exists. Please choose a different one.')
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),
                                       Length(min=4, max=30)],
                                       render_kw={'placeholder': 'Username'})
    password = PasswordField(validators=[InputRequired(),
                                       Length(min=4, max=30)],
                                       render_kw={'placeholder': 'Password'})
    submit = SubmitField('Login')
    

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String, default='-')
    date_created = db.Column(db.DateTime,default=datetime.utcnow )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # This will put unique input per account

    def __repr__(self):
        return '<Task %r>' % self.id
       
                                    
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)
    
@app.route('/register', methods=['POST', 'GET'])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user=User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    

@app.route('/dashboard', methods=['POST', 'GET']) 
@login_required
def dashboard():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, user_id=current_user.id) # This will put unique input per account

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/dashboard')
        except:
            return 'There was an issue adding your task.'
    else:
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created).all()
        return render_template('dashboard.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/dashboard')
    except:
        return 'There was an problem deleting this task.'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    task_to_prio=Todo.query.get_or_404(id)
    
    if request.method=='POST':
        
        new_priority = request.form.get('priority')
        try:
            task_to_prio.priority =str(new_priority)
            db.session.commit()
            return redirect('/dashboard')

        except:
            return 'There was an problem updating this task.' 
        
    else:
        return render_template('update.html', task=task)
    
    '''if request.method=='POST':
            new_priority = request.form.get('priority')
            try:
                task_to_prio.priority =int(new_priority)
    
                db.session.commit()
                return redirect('/dashboard')
            except:
                return 'There was an problem prioritizing this task.'
        return render_template('dashboard.html', task=task_to_prio)'''

@app.route('/priority/<int:id>', methods=['GET', 'POST'])
def priority(id):
    task_to_prio=Todo.query.get_or_404(id)
    
    if request.method=='POST':
        new_priority = request.form.get('priority')
        try:
            task_to_prio.priority =int(new_priority)

            db.session.commit()
            return redirect('/dashboard')
        except:
            return 'There was an problem prioritizing this task.'
    return render_template('dashboard.html', task=task_to_prio)


if __name__ == '__main__':
    app.run(debug=True)
