
from flask import Blueprint,render_template,request, flash, redirect,url_for
from .models import User
from . import db  #significa __init__.py import db
from werkzeug.security import generate_password_hash,check_password_hash ## hashear la pass - esta no tiene hash inverse, ya que al generarla se le pasa un salt que es complicado de adivinar
# lo que hacemos es comparar si la password que ingresamos es igual al hash almacenado

## Para manejar lo que puede ver el usuario logueado - relacionado con UserMixin en models.py - current_user permite acceder a la informacion del usuario logueado
from flask_login import login_user, login_required, logout_user, current_user
import random

auth = Blueprint('auth',__name__)

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

@auth.route("/login", methods=['GET','POST']) # methods que aceptara
def login():
    #data = request.form #obtenemos la data del form -> ImmutableMultiDict([('email', 'h@gmail.com'), ('password', 'h')])
    if request.method=='POST':
        email= request.form.get('email')
        password=request.form.get('password')
        
        # si el usuario es valido
        user=User.query.filter_by(email=email).first() # lo obtenemos filtrando por email y obteniendo el primero que coincida
        
        # si el mail existe
        if user:
            ## chequeamos la password
            #si es la correcta
            if check_password_hash(user.password,password):
                flash('Logged in successfully.', category='success')
                if user:
                    login_user(user, remember=True) # recuerda los datos del usuario que se logueo, se guardara en la flask session
                else:
                    flash('User not found.', category='error')
                return redirect(url_for('views.home'))
            # si NO es correcta
            else:
                flash('Incorrecta password,try again.', category='error')
        # si el mail NO existe
        else:
            flash('Email does not exist.', category='error')
    
    return render_template("login.html",user=current_user) # podemos pasar el valor que queremos

@auth.route("/logout")
@login_required # esto se puede acceder solo si el usuario esta logueado
def logout():
    logout_user() # Desloguea el usuario guardado
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    if request.method == "POST": # Verificamos si se hizo un POST
        email=request.form.get('email') # Obtenemos el email, por eso es importante el name en el HTML
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        
        user=User.query.filter_by(email=email).first()
        # Verificamos que no existe otro usuario con el mismo mail
        if user:
            flash('Email already exists', category='error')
        # verfificamos si la informacion obtenida es valida
        # Los errorres se notifican mediante Message Flashing,
        # category success, error o podemos inventar
        elif len(email)<4:
            flash('Email must be greather than 4 chacracters.', category='error')
        elif len(first_name) <2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #add database a user
            new_user=User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), color=random_color() )
            db.session.add(new_user)
            db.session.commit()#guardar los cambios
            login_user(new_user, remember=True) # recuerda los datos del usuario que se logueo, se guardara en la flask session
            flash('Account created!.', category='success')
            return redirect(url_for('views.home')) # redirigir al home
            
        """
        Los mostramos en el HTML asi:
            <!--Mostrar Flask del error or success-->
            {% with messages = get_flashed_messages(with_categories=true) %} {% if
                messages %} {% for category, message in messages %} {% if category ==
                'error' %}
        """
        
    return render_template("sign_up.html",user=current_user)